"""SQLite journal and local configuration pointer; fixture identities only.

All mutating operations use a write transaction. There is no external provider,
authentication service, model inference, metric collection, or training here.
"""

from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
import json
import sqlite3
import uuid

from .contracts import (
    canonical, count, digest, nonempty, number, require, timestamp, validate_experiment,
)


class Pilot:
    def __init__(self, path, clock=None):
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        self.db = sqlite3.connect(str(Path(path)), timeout=5, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        version = self.db.execute("PRAGMA user_version").fetchone()[0]
        require(version in (0, 1), "unsupported database version")
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS records (
                sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                id TEXT NOT NULL UNIQUE,
                kind TEXT NOT NULL,
                body TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS current_state (
                singleton INTEGER PRIMARY KEY CHECK(singleton = 1),
                active TEXT,
                generation INTEGER NOT NULL,
                policy_revision INTEGER NOT NULL,
                enabled INTEGER NOT NULL
            );
            INSERT OR IGNORE INTO current_state VALUES (1, NULL, 0, 1, 1);
            PRAGMA user_version = 1;
        """)

    def close(self):
        self.db.close()

    def now(self):
        value = self.clock()
        require(value.tzinfo is not None, "clock needs timezone")
        return value.astimezone(timezone.utc)

    @staticmethod
    def _role(actor, owner=False):
        allowed = {"owner-fixture"} if owner else {"owner-fixture", "reviewer-fixture"}
        require(actor in allowed, "fixture actor lacks the required role")

    @contextmanager
    def _write(self):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield
            self.db.execute("COMMIT")
        except Exception:
            self.db.execute("ROLLBACK")
            raise

    def _put(self, kind, payload):
        record = dict(payload, id=f"{kind}-{uuid.uuid4().hex}", kind=kind,
                      recordedAt=self.now().isoformat())
        self.db.execute("INSERT INTO records(id, kind, body) VALUES (?, ?, ?)",
                        (record["id"], kind, canonical(record)))
        return record

    def get(self, record_id, kind=None):
        row = self.db.execute("SELECT body FROM records WHERE id = ?", (record_id,)).fetchone()
        require(row is not None, "record not found")
        result = json.loads(row["body"])
        require(kind is None or result["kind"] == kind, "record kind mismatch")
        return result

    def records(self, kind=None):
        if kind is None:
            rows = self.db.execute("SELECT body FROM records ORDER BY sequence").fetchall()
        else:
            rows = self.db.execute("SELECT body FROM records WHERE kind = ? ORDER BY sequence", (kind,)).fetchall()
        return [json.loads(row["body"]) for row in rows]

    def state(self):
        return dict(self.db.execute("SELECT active, generation, policy_revision, enabled FROM current_state").fetchone())

    @staticmethod
    def _allowed_config(config):
        require(config["capabilities"] == ["draft"], "candidate cannot expand or change capabilities")
        require(config["scope"] == "support-drafting" and config["dataScope"] == "synthetic-only",
                "unsupported authority or data scope")

    def add_config(self, label, prompt, actor="reviewer-fixture", capabilities=None,
                   scope="support-drafting", data_scope="synthetic-only"):
        self._role(actor)
        nonempty(label, "label")
        nonempty(prompt, "prompt")
        caps = ["draft"] if capabilities is None else capabilities
        require(isinstance(caps, list) and bool(caps), "capabilities must be a nonempty list")
        for cap in caps:
            nonempty(cap, "capability")
        nonempty(scope, "scope")
        nonempty(data_scope, "data scope")
        payload = {"label": label, "prompt": prompt, "model": "fixture-model-no-inference",
                   "capabilities": caps, "scope": scope, "dataScope": data_scope}
        with self._write():
            return self._put("config", dict(payload, artifactDigest=digest(payload), producer=actor))

    def bootstrap(self, config_id, actor="owner-fixture"):
        self._role(actor, owner=True)
        with self._write():
            require(self.state()["active"] is None, "baseline already initialized")
            config = self.get(config_id, "config")
            self._allowed_config(config)
            self.db.execute("UPDATE current_state SET active = ?, generation = 1 WHERE singleton = 1", (config_id,))
            return self._put("baseline", {"configRef": config_id, "owner": actor, "generation": 1})

    def set_policy_enabled(self, enabled, actor="owner-fixture"):
        self._role(actor, owner=True)
        require(type(enabled) is bool, "enabled must be boolean")
        with self._write():
            self.db.execute("UPDATE current_state SET enabled = ?, policy_revision = policy_revision + 1 WHERE singleton = 1",
                            (int(enabled),))
            return self._put("policy", {"owner": actor, "state": self.state()})

    def add_experiment(self, spec, actor="reviewer-fixture"):
        self._role(actor)
        validate_experiment(spec)
        with self._write():
            baseline = self.get(spec["baselineRef"], "config")
            candidate = self.get(spec["candidateRef"], "config")
            self._allowed_config(baseline)
            self._allowed_config(candidate)
            require(self.state()["active"] == baseline["id"], "baseline is not active")
            return self._put("experiment", {"spec": spec, "specDigest": digest(spec), "owner": actor})

    def observe(self, experiment_id, config_id, metric, value, cases, population, method,
                unit, window_start, window_end, observed_at, source, limitations,
                actor="reviewer-fixture"):
        self._role(actor)
        if value is not None:
            number(value, "value")
        count(cases, "cases", minimum=0)
        for label, val in (("population", population), ("method", method), ("unit", unit),
                           ("source", source), ("limitations", limitations)):
            nonempty(val, label)
        start, end, observed = timestamp(window_start), timestamp(window_end), timestamp(observed_at)
        require(start < end <= observed <= self.now(), "invalid observation period or future observation")
        with self._write():
            spec = self.get(experiment_id, "experiment")["spec"]
            require(config_id in (spec["baselineRef"], spec["candidateRef"]), "unrelated configuration")
            require(metric in {c["metric"] for c in spec["criteria"]}, "metric outside the pilot profile")
            return self._put("observation", {
                "experimentRef": experiment_id, "configRef": config_id, "metric": metric,
                "value": value, "cases": cases, "population": population, "method": method,
                "unit": unit, "windowStart": window_start, "windowEnd": window_end,
                "observedAt": observed_at, "source": source, "limitations": limitations, "producer": actor,
            })

    def flag_concern(self, experiment_id, detail, actor="reviewer-fixture"):
        self._role(actor)
        nonempty(detail, "detail")
        with self._write():
            self.get(experiment_id, "experiment")
            return self._put("concern", {"experimentRef": experiment_id, "detail": detail, "producer": actor})

    def _evidence(self, experiment_id):
        return [r for r in self.records() if r["kind"] in ("observation", "concern")
                and r.get("experimentRef") == experiment_id]

    def _assess(self, experiment):
        spec = experiment["spec"]
        evidence = self._evidence(experiment["id"])
        issues, failures, comparisons = [], [], []
        now = self.now()
        if not timestamp(spec["windowEnd"]) <= now < timestamp(spec["reviewBefore"]):
            issues.append("experiment window incomplete or review expired")
        issues.extend("unresolved concern: " + r["detail"] for r in evidence if r["kind"] == "concern")
        for criterion in spec["criteria"]:
            values = {}
            for ref in (spec["baselineRef"], spec["candidateRef"]):
                rows = [r for r in evidence if r["kind"] == "observation"
                        and r["metric"] == criterion["metric"] and r["configRef"] == ref]
                label = f"{criterion['metric']} / {ref}"
                if len(rows) != 1:
                    issues.append(label + ": missing or conflicting measurements; aggregation not supported")
                    continue
                row = rows[0]
                age = (now - timestamp(row["observedAt"])).total_seconds()
                matching = (row["population"] == spec["population"] and row["method"] == spec["method"]
                            and row["unit"] == criterion["unit"]
                            and timestamp(row["windowStart"]) == timestamp(spec["windowStart"])
                            and timestamp(row["windowEnd"]) == timestamp(spec["windowEnd"]))
                if not matching:
                    issues.append(label + ": population, method, unit, or window mismatch")
                elif not 0 <= age <= spec["maxAgeSeconds"]:
                    issues.append(label + ": stale or future evidence")
                elif row["value"] is None or row["cases"] < spec["minCases"]:
                    issues.append(label + ": missing value or insufficient case count")
                else:
                    values[ref] = row["value"]
            if len(values) != 2:
                continue
            baseline, candidate = values[spec["baselineRef"]], values[spec["candidateRef"]]
            higher = criterion["direction"] == "higher"
            gain = candidate - baseline if higher else baseline - candidate
            limit_ok = candidate >= criterion["candidateLimit"] if higher else candidate <= criterion["candidateLimit"]
            passed = limit_ok and gain >= criterion["minimumGain"]
            comparisons.append({"metric": criterion["metric"], "baseline": baseline, "candidate": candidate,
                                "gain": gain, "passed": passed})
            if not passed:
                failures.append(criterion["metric"] + ": candidate limit or required gain failed")
        result = "contradicted" if failures else "insufficient" if issues else "supported"
        return {"result": result, "issues": issues, "failures": failures, "comparisons": comparisons,
                "evidenceRefs": [r["id"] for r in evidence], "evidenceDigest": digest(evidence),
                "claimScope": "Synthetic threshold comparison only; no causal or human-learning claim."}

    def evaluate(self, experiment_id, actor="reviewer-fixture"):
        self._role(actor)
        with self._write():
            experiment = self.get(experiment_id, "experiment")
            return self._put("evaluation", dict(self._assess(experiment), experimentRef=experiment_id,
                                                specDigest=experiment["specDigest"], producer=actor))

    def _current_evaluation(self, evaluation, experiment, require_supported=True):
        require(evaluation["experimentRef"] == experiment["id"], "evaluation belongs to another experiment")
        require(evaluation["specDigest"] == experiment["specDigest"], "experiment binding mismatch")
        current = self._assess(experiment)
        require(current["evidenceDigest"] == evaluation["evidenceDigest"], "evidence changed; obtain a new evaluation")
        if require_supported:
            require(current["result"] == evaluation["result"] == "supported", "evaluation does not currently support adoption")
        return current

    def decide(self, experiment_id, evaluation_id, decision, rationale, actor="owner-fixture"):
        self._role(actor, owner=True)
        require(decision in ("adopt", "reject", "defer"), "unsupported decision")
        nonempty(rationale, "rationale")
        with self._write():
            experiment = self.get(experiment_id, "experiment")
            evaluation = self.get(evaluation_id, "evaluation")
            self._current_evaluation(evaluation, experiment, require_supported=decision == "adopt")
            state = self.state()
            if decision == "adopt":
                require(state["enabled"], "current fixture policy prohibits activation")
                require(state["active"] == experiment["spec"]["baselineRef"], "active baseline changed")
            return self._put("decision", {
                "experimentRef": experiment_id, "evaluationRef": evaluation_id, "decision": decision,
                "rationale": rationale, "owner": actor, "expectedState": state,
                "candidateRef": experiment["spec"]["candidateRef"], "specDigest": experiment["specDigest"],
            })

    def activate(self, decision_id, actor="owner-fixture"):
        self._role(actor, owner=True)
        with self._write():
            decision = self.get(decision_id, "decision")
            require(decision["decision"] == "adopt", "no adoption decision")
            decisions = [d for d in self.records("decision") if d["experimentRef"] == decision["experimentRef"]]
            require(decisions[-1]["id"] == decision_id, "decision was superseded")
            experiment = self.get(decision["experimentRef"], "experiment")
            evaluation = self.get(decision["evaluationRef"], "evaluation")
            self._current_evaluation(evaluation, experiment)
            state = self.state()
            require(state == decision["expectedState"], "current baseline, generation, or policy changed")
            require(state["enabled"], "current fixture policy prohibits activation")
            candidate = self.get(decision["candidateRef"], "config")
            self._allowed_config(candidate)
            self.db.execute("UPDATE current_state SET active = ?, generation = generation + 1 WHERE singleton = 1",
                            (candidate["id"],))
            verified = self.state()
            require(verified["active"] == candidate["id"], "local readback failed")
            return self._put("activation", {
                "decisionRef": decision_id, "experimentRef": experiment["id"], "before": state,
                "after": verified, "artifactDigest": candidate["artifactDigest"], "owner": actor,
                "verificationScope": "SQLite configuration pointer readback inside the committing transaction",
            })

    def monitor(self, activation_id, values, source, limitations, actor="reviewer-fixture"):
        self._role(actor)
        nonempty(source, "source")
        nonempty(limitations, "limitations")
        require(isinstance(values, dict), "monitoring values must be an object")
        with self._write():
            activation = self.get(activation_id, "activation")
            spec = self.get(activation["experimentRef"], "experiment")["spec"]
            state = self.state()
            require((state["active"], state["generation"]) ==
                    (activation["after"]["active"], activation["after"]["generation"]), "activation no longer current")
            require(set(values) == {c["metric"] for c in spec["criteria"]}, "monitor every declared metric")
            missing, failures = [], []
            for c in spec["criteria"]:
                value = values[c["metric"]]
                if value is None:
                    missing.append(c["metric"])
                    continue
                number(value, c["metric"])
                passed = value >= c["candidateLimit"] if c["direction"] == "higher" else value <= c["candidateLimit"]
                if not passed:
                    failures.append(c["metric"])
            result = "concerning" if failures else "unavailable" if missing else "acceptable"
            return self._put("monitoring", {
                "activationRef": activation_id, "values": values, "result": result,
                "failures": failures, "missing": missing, "source": source, "limitations": limitations,
                "producer": actor, "observedAt": self.now().isoformat(),
            })

    def rollback(self, activation_id, monitoring_id, reason, actor="owner-fixture"):
        self._role(actor, owner=True)
        nonempty(reason, "reason")
        with self._write():
            activation = self.get(activation_id, "activation")
            monitoring = self.get(monitoring_id, "monitoring")
            require(monitoring["activationRef"] == activation_id, "monitoring belongs to another activation")
            reviews = [r for r in self.records("monitoring") if r["activationRef"] == activation_id]
            require(reviews[-1]["id"] == monitoring_id, "monitoring review was superseded")
            require(monitoring["result"] in ("concerning", "unavailable"), "pilot rollback requires a concern or missing monitoring")
            spec = self.get(activation["experimentRef"], "experiment")["spec"]
            age = (self.now() - timestamp(monitoring["observedAt"])).total_seconds()
            require(0 <= age <= spec["maxAgeSeconds"], "monitoring evidence is stale")
            state = self.state()
            require(state["enabled"], "current fixture policy prohibits rollback")
            require((state["active"], state["generation"]) ==
                    (activation["after"]["active"], activation["after"]["generation"]), "intervening activation prevents rollback")
            previous = self.get(activation["before"]["active"], "config")
            self._allowed_config(previous)
            self.db.execute("UPDATE current_state SET active = ?, generation = generation + 1 WHERE singleton = 1", (previous["id"],))
            verified = self.state()
            require(verified["active"] == previous["id"], "local restoration readback failed")
            return self._put("recovery", {
                "activationRef": activation_id, "monitoringRef": monitoring_id, "before": state, "after": verified,
                "owner": actor, "reason": reason, "verificationScope": "Local configuration pointer only; history retained.",
            })
