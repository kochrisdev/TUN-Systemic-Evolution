"""SQLite management records and local budget reservations.

Fixture identities are selected by the caller: this is not authentication.
Reservations never execute a provider action and are not execution grants.
"""

from contextlib import contextmanager
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from uuid import uuid4

from .contracts import ContractError, loads, ref, timestamp, validate


class AccessDenied(PermissionError):
    pass


class Conflict(ValueError):
    pass


FIXTURES = {
    "owner-a": ("team-a", "owner"), "reviewer-a": ("team-a", "reviewer"),
    "viewer-a": ("team-a", "viewer"), "agent-a": ("team-a", "agent"),
    "owner-b": ("team-b", "owner"), "agent-b": ("team-b", "agent"),
}


class Pilot:
    def __init__(self, path, principal="owner-a", clock=None):
        if principal not in FIXTURES:
            raise AccessDenied("Unknown fixture identity")
        self.path = str(Path(path).resolve())
        self.principal = principal
        self.scope, self.role = FIXTURES[principal]
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        with self._transaction() as db:
            version = db.execute("PRAGMA user_version").fetchone()[0]
            if version not in (0, 1):
                raise Conflict("Unsupported database version; no migration is supplied")
            existing = db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            if version == 0 and existing:
                raise Conflict("Refusing to initialize a database with unrelated tables")
            db.execute("""CREATE TABLE IF NOT EXISTS records (
                scope TEXT NOT NULL, id TEXT NOT NULL, version INTEGER NOT NULL,
                kind TEXT NOT NULL, initiative_id TEXT NOT NULL, visibility TEXT NOT NULL,
                body TEXT NOT NULL, PRIMARY KEY(scope, id, version))""")
            db.execute("""CREATE TABLE IF NOT EXISTS mandates (
                scope TEXT NOT NULL, id TEXT NOT NULL, version INTEGER NOT NULL,
                state TEXT NOT NULL, PRIMARY KEY(scope, id))""")
            db.execute("""CREATE TABLE IF NOT EXISTS reservations (
                scope TEXT NOT NULL, request_id TEXT NOT NULL, initiative_id TEXT NOT NULL,
                mandate_id TEXT NOT NULL, amount INTEGER NOT NULL, record_id TEXT NOT NULL,
                PRIMARY KEY(scope, request_id))""")
            db.execute("PRAGMA user_version = 1")

    @contextmanager
    def _transaction(self):
        db = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        db.row_factory = sqlite3.Row
        try:
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def _now(self):
        now = self.clock()
        if not isinstance(now, datetime) or now.tzinfo is None:
            raise ContractError("The host clock must return an aware datetime")
        return now.astimezone(timezone.utc)

    def _role(self, *allowed):
        if self.role not in allowed:
            raise AccessDenied("Fixture role cannot perform this operation")

    def _visible(self, record):
        return record["visibility"] == "team" or self.role in ("owner", "reviewer")

    def _get(self, db, reference, kind=None):
        if (not isinstance(reference, dict) or set(reference) != {"id", "version"}
                or not isinstance(reference["id"], str)
                or type(reference["version"]) is not int or reference["version"] < 1):
            raise ContractError("Expected an exact {id, version} reference")
        row = db.execute("SELECT body FROM records WHERE scope=? AND id=? AND version=?",
                         (self.scope, reference["id"], reference["version"])).fetchone()
        if row is None:
            raise AccessDenied("Record unavailable in this scope")
        record = loads(row["body"])
        if not self._visible(record):
            raise AccessDenied("Record unavailable to this fixture role")
        if kind is not None and record["recordType"] != kind:
            raise ContractError(f"Expected a {kind} reference")
        return record

    def _records(self, db, kind, initiative_id):
        rows = db.execute("SELECT body FROM records WHERE scope=? AND kind=? AND initiative_id=? ORDER BY rowid",
                          (self.scope, kind, initiative_id)).fetchall()
        return [loads(row["body"]) for row in rows]

    def _make(self, kind, data, visibility="team", identity=None, version=1):
        return validate({"schemaVersion": "0.1", "recordType": kind,
                         "id": identity or f"{kind.lower()}-{uuid4().hex}", "version": version,
                         "scope": self.scope, "actor": self.principal,
                         "recordedAt": self._now().isoformat(), "visibility": visibility, "data": data})

    def _put(self, db, record):
        record = validate(record)
        initiative_id = record["id"] if record["recordType"] == "Initiative" else record["data"]["initiativeRef"]["id"]
        db.execute("INSERT INTO records VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (self.scope, record["id"], record["version"], record["recordType"], initiative_id,
                    record["visibility"], json.dumps(record, allow_nan=False, sort_keys=True)))
        return record

    def _owner(self, initiative):
        self._role("owner")
        if initiative["data"]["owner"] != self.principal:
            raise AccessDenied("Only the initiative's fixture owner can decide")

    def _current(self, db, reference):
        mandate = self._get(db, reference, "Mandate")
        row = db.execute("SELECT version, state FROM mandates WHERE scope=? AND id=?",
                         (self.scope, mandate["id"])).fetchone()
        if row is None or row["version"] != reference["version"]:
            raise Conflict("Stale mandate revision")
        return mandate, row["state"]

    def get(self, reference):
        with self._transaction() as db:
            return self._get(db, reference)

    def history(self, initiative_ref):
        with self._transaction() as db:
            initiative = self._get(db, initiative_ref, "Initiative")
            rows = db.execute("SELECT body FROM records WHERE scope=? AND initiative_id=? ORDER BY rowid",
                              (self.scope, initiative["id"])).fetchall()
            return [record for row in rows if self._visible(record := loads(row["body"]))]

    def create_initiative(self, data):
        self._role("owner")
        record = self._make("Initiative", data)
        data = record["data"]
        self._owner(record)
        ids = [criterion["id"] for criterion in data["criteria"]]
        if len(ids) != len(set(ids)):
            raise ContractError("Criterion IDs must be unique")
        if timestamp(data["reviewAt"]) <= self._now():
            raise ContractError("Initial review must be in the future")
        with self._transaction() as db:
            return self._put(db, record)

    def propose_mandate(self, data, previous=None):
        self._role("owner")
        record = self._make("Mandate", data, identity=previous["id"] if previous else None,
                            version=previous["version"] + 1 if previous else 1)
        data = record["data"]
        with self._transaction() as db:
            initiative = self._get(db, data["initiativeRef"], "Initiative")
            self._owner(initiative)
            if previous:
                old, _ = self._current(db, previous)
                if old["data"]["initiativeRef"] != data["initiativeRef"]:
                    raise Conflict("A mandate cannot move between initiatives")
            if data["delegate"] not in FIXTURES or FIXTURES[data["delegate"]] != (self.scope, "agent"):
                raise ContractError("This pilot delegates reservations only to its scoped fixture agent")
            if not timestamp(data["startsAt"]) < timestamp(data["expiresAt"]):
                raise ContractError("Mandate start must precede expiry")
            if timestamp(data["expiresAt"]) <= self._now():
                raise ContractError("Cannot propose an expired mandate")
            if data["budgetMinor"] > initiative["data"]["budgetMinor"]:
                raise ContractError("Mandate limit exceeds the initiative ceiling")
            self._put(db, record)
            db.execute("INSERT INTO mandates VALUES (?, ?, ?, ?) ON CONFLICT(scope, id) DO UPDATE SET version=excluded.version, state=excluded.state",
                       (self.scope, record["id"], record["version"], "proposed"))
            return record

    def decide(self, mandate_ref, choice, rationale, alternatives, review_at, evidence_refs=()):
        self._role("owner")
        with self._transaction() as db:
            mandate, state = self._current(db, mandate_ref)
            initiative = self._get(db, mandate["data"]["initiativeRef"], "Initiative")
            self._owner(initiative)
            transitions = {("proposed", "approve"): "active", ("proposed", "reject"): "rejected",
                           ("active", "pause"): "paused", ("active", "revoke"): "revoked",
                           ("paused", "revoke"): "revoked"}
            target = transitions.get((state, choice))
            if target is None:
                raise Conflict("Decision is not allowed in the current mandate state")
            if choice == "approve" and timestamp(mandate["data"]["expiresAt"]) <= self._now():
                raise Conflict("Cannot approve expired authority")
            if timestamp(review_at) <= self._now():
                raise ContractError("Next review must be in the future")
            evidence = [self._get(db, item) for item in evidence_refs]
            for item in evidence:
                if item["data"].get("initiativeRef") != ref(initiative):
                    raise ContractError("Decision evidence belongs to another initiative")
            visibility = "reviewers" if any(item["visibility"] == "reviewers" for item in evidence) else "team"
            decision = self._make("Decision", {
                "initiativeRef": ref(initiative), "subjectRef": mandate_ref, "choice": choice,
                "rationale": rationale, "alternatives": alternatives, "evidenceRefs": list(evidence_refs), "reviewAt": review_at,
            }, visibility)
            self._put(db, decision)
            db.execute("UPDATE mandates SET state=? WHERE scope=? AND id=?", (target, self.scope, mandate["id"]))
            return decision

    def mandate_state(self, reference):
        with self._transaction() as db:
            mandate, state = self._current(db, reference)
            if state == "active":
                now = self._now()
                if now >= timestamp(mandate["data"]["expiresAt"]):
                    return "expired"
                if now < timestamp(mandate["data"]["startsAt"]):
                    return "not-yet-valid"
            return state

    def _budget(self, db, initiative):
        reserved = db.execute("SELECT COALESCE(SUM(amount), 0) FROM reservations WHERE scope=? AND initiative_id=?",
                              (self.scope, initiative["id"])).fetchone()[0]
        ceiling = initiative["data"]["budgetMinor"]
        return {"ceilingMinor": ceiling, "reservedMinor": reserved, "availableMinor": ceiling - reserved, "currency": "USD"}

    def budget(self, initiative_ref):
        with self._transaction() as db:
            return self._budget(db, self._get(db, initiative_ref, "Initiative"))

    def reserve(self, mandate_ref, request_id, action, target, amount_minor):
        self._role("agent")
        with self._transaction() as db:
            mandate = self._get(db, mandate_ref, "Mandate")
            data = mandate["data"]
            if data["delegate"] != self.principal:
                raise AccessDenied("Reservation delegate mismatch")
            initiative = self._get(db, data["initiativeRef"], "Initiative")
            reservation = self._make("Reservation", {
                "initiativeRef": ref(initiative), "mandateRef": mandate_ref, "requestId": request_id,
                "action": action, "target": target, "amountMinor": amount_minor,
            })
            prior = db.execute("SELECT record_id FROM reservations WHERE scope=? AND request_id=?",
                               (self.scope, request_id)).fetchone()
            if prior:
                original = self._get(db, {"id": prior[0], "version": 1}, "Reservation")
                if original["data"] != reservation["data"]:
                    raise Conflict("Idempotency identity reused with different reservation parameters")
                return original  # Historical receipt only; never fresh execution authority.
            _, state = self._current(db, mandate_ref)
            now = self._now()
            if state != "active" or not timestamp(data["startsAt"]) <= now < timestamp(data["expiresAt"]):
                raise Conflict("Mandate is not currently usable")
            if action not in data["actions"] or target not in data["targets"]:
                raise AccessDenied("Action or target exceeds delegated scope")
            budget = self._budget(db, initiative)
            mandate_reserved = db.execute("SELECT COALESCE(SUM(amount), 0) FROM reservations WHERE scope=? AND mandate_id=?",
                                          (self.scope, mandate["id"])).fetchone()[0]
            if amount_minor > budget["availableMinor"] or mandate_reserved + amount_minor > data["budgetMinor"]:
                raise Conflict("Shared initiative or mandate budget exhausted")
            self._put(db, reservation)
            db.execute("INSERT INTO reservations VALUES (?, ?, ?, ?, ?, ?)",
                       (self.scope, request_id, initiative["id"], mandate["id"], amount_minor, reservation["id"]))
            return reservation

    def observe(self, data, visibility="team"):
        self._role("owner", "reviewer")
        record = self._make("Observation", data, visibility)
        data = record["data"]
        with self._transaction() as db:
            initiative = self._get(db, data["initiativeRef"], "Initiative")
            if not timestamp(data["windowStart"]) <= timestamp(data["windowEnd"]) <= timestamp(data["observedAt"]) <= self._now():
                raise ContractError("Observation window, observation time, and host time are inconsistent")
            if data["kind"] == "outcome":
                criterion = next((item for item in initiative["data"]["criteria"] if item["id"] == data["criterionId"]), None)
                if criterion is None:
                    raise ContractError("Unknown outcome criterion")
                if data["unit"] != criterion["unit"]:
                    raise ContractError("Observation unit differs from the criterion")
            if data["supersedes"]:
                old = self._get(db, data["supersedes"], "Observation")
                fields = ("initiativeRef", "kind", "criterionId", "windowStart", "windowEnd")
                if any(old["data"][key] != data[key] for key in fields):
                    raise ContractError("Correction must retain the same claim and window")
                if timestamp(data["observedAt"]) < timestamp(old["data"]["observedAt"]):
                    raise ContractError("Correction observation predates its predecessor")
                if old["visibility"] == "reviewers" and visibility != "reviewers":
                    raise AccessDenied("A correction cannot downgrade evidence visibility")
                if any(item["data"]["supersedes"] == data["supersedes"] for item in self._records(db, "Observation", initiative["id"])):
                    raise Conflict("Observation already superseded; correct the latest record")
            return self._put(db, record)

    def review(self, initiative_ref, window_start, window_end, proposed_action, rationale, review_at):
        self._role("owner", "reviewer")
        now = self._now()
        if not timestamp(window_start) <= timestamp(window_end) <= now < timestamp(review_at):
            raise ContractError("Review requires a past window and future review time")
        with self._transaction() as db:
            initiative = self._get(db, initiative_ref, "Initiative")
            observations = self._records(db, "Observation", initiative["id"])
            superseded = {(item["data"]["supersedes"]["id"], item["data"]["supersedes"]["version"])
                          for item in observations if item["data"]["supersedes"]}
            relevant = [item for item in observations
                        if (item["id"], item["version"]) not in superseded
                        and timestamp(item["data"]["windowStart"]) == timestamp(window_start)
                        and timestamp(item["data"]["windowEnd"]) == timestamp(window_end)]
            findings, limitations = [], []
            for criterion in initiative["data"]["criteria"]:
                candidates = [item for item in relevant if item["data"]["kind"] == "outcome"
                              and item["data"]["criterionId"] == criterion["id"]]
                usable = []
                for item in candidates:
                    data = item["data"]
                    if (now - timestamp(data["observedAt"])).total_seconds() > criterion["maxAgeSeconds"]:
                        limitations.append(f"Stale observation excluded: {item['id']}")
                    elif data["method"] != criterion["method"] or data["population"] != criterion["population"]:
                        limitations.append(f"Method or population mismatch excluded: {item['id']}")
                    else:
                        usable.append(item)
                failures = [item for item in usable if item["data"]["status"] == "contradicted" or
                            (item["data"]["status"] == "measured" and
                             ((criterion["operator"] == "gte" and item["data"]["value"] < criterion["threshold"]) or
                              (criterion["operator"] == "lte" and item["data"]["value"] > criterion["threshold"])))]
                if failures:
                    assessment, explanation = "contradicted", "At least one current observation contradicts this criterion."
                elif not usable or any(item["data"]["status"] != "measured" for item in usable):
                    assessment, explanation = "insufficient", "Current matching measurements are missing or unresolved."
                else:
                    assessment, explanation = "supported", "All current matching measurements meet the stated threshold; causality is not established."
                findings.append({"criterionId": criterion["id"], "assessment": assessment,
                                 "explanation": explanation, "evidenceRefs": [ref(item) for item in candidates]})
            for item in relevant:
                limitations.extend(item["data"]["limitations"])
                if item["data"]["kind"] == "operation":
                    limitations.append(f"Operational evidence is not outcome proof: {item['id']} ({item['data']['status']})")
            assessments = [item["assessment"] for item in findings]
            overall = "contradicted" if "contradicted" in assessments else "insufficient" if "insufficient" in assessments else "supported"
            visibility = "reviewers" if any(item["visibility"] == "reviewers" for item in relevant) else "team"
            return self._put(db, self._make("Review", {
                "initiativeRef": initiative_ref, "windowStart": window_start, "windowEnd": window_end,
                "assessment": overall, "findings": findings, "evidenceRefs": [ref(item) for item in relevant],
                "limitations": sorted(set(limitations)), "proposedAction": proposed_action,
                "rationale": rationale, "reviewAt": review_at, "budget": self._budget(db, initiative),
            }, visibility))
