"""Trusted local fixture bridge; stores remain separate and are not atomic together.

Management decides a candidate-specific mandate. Evolution records that decision
locally. Engineering independently approves, authorizes, publishes, and verifies
the adoption manifest. Only then may Evolution activate its local pointer.
"""

from contextlib import contextmanager
from pathlib import Path
import json
import sqlite3
import uuid

from reference.tsev_pilot.contracts import canonical, digest, nonempty, require
from reference.tsev_pilot.runtime import Pilot as EvolutionPilot
from vendor.management.reference.tsm_pilot.contracts import ref, timestamp
from vendor.management.reference.tsm_pilot.runtime import Pilot as ManagementPilot, Conflict as ManagementConflict
from vendor.engineering.reference.tse_pilot.runtime import Host, Principal, Provider
from vendor.engineering.reference.tse_pilot.presentation import proposal_view, receipt_view


PINS = {
    "design": "f1cc566c44a04741e51ce642ffaa0feab0bd5b36",
    "engineering": "476f649d41c4a0f659c15276384866908d9b9c01",
    "management": "6959643f4ab0134e20d39ae3112a38d501853d05",
}
TARGET = "evolution-adoption-catalog"


class FamilyBridge:
    def __init__(self, directory, clock=None):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.evolution = EvolutionPilot(self.directory / "evolution.sqlite3", clock=clock)
        self.clock = self.evolution.now
        self.management = ManagementPilot(self.directory / "management.sqlite3", "owner-a", clock=self.clock)
        self.delegate = ManagementPilot(self.directory / "management.sqlite3", "agent-a", clock=self.clock)
        self.provider = Provider(self.directory / "provider.sqlite3")
        self.engineering = Host(self.directory / "engineering.sqlite3", self.provider, clock=self.clock)
        self.principal = Principal("owner-a", "team-a")
        self.db = sqlite3.connect(self.directory / "bridge.sqlite3", timeout=10, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS cases (
                id TEXT PRIMARY KEY, experiment_id TEXT NOT NULL UNIQUE, body TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS events (
                sequence INTEGER PRIMARY KEY AUTOINCREMENT, case_id TEXT NOT NULL,
                phase TEXT NOT NULL, recorded_at TEXT NOT NULL, body TEXT NOT NULL
            );
        """)

    def close(self):
        self.evolution.close()
        self.db.close()

    @staticmethod
    def _owner(actor):
        require(actor == "owner-a", "the bridge requires its human owner fixture")

    @contextmanager
    def _write(self):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise

    def case(self, case_id):
        row = self.db.execute("SELECT body FROM cases WHERE id = ?", (case_id,)).fetchone()
        require(row is not None, "family case not found")
        return json.loads(row["body"])

    def _save(self, case, phase):
        case["phase"] = phase
        self.db.execute("UPDATE cases SET body = ? WHERE id = ?", (canonical(case), case["id"]))
        self.db.execute("INSERT INTO events(case_id, phase, recorded_at, body) VALUES (?, ?, ?, ?)",
                        (case["id"], phase, self.clock().isoformat(), canonical(case)))
        return case

    def _evolution_ready(self, case):
        experiment = self.evolution.get(case["experimentRef"], "experiment")
        evaluation = self.evolution.get(case["evaluationRef"], "evaluation")
        self.evolution._current_evaluation(evaluation, experiment)
        require(self.evolution.state() == case["expectedEvolutionState"], "Evolution baseline or authority changed")
        require(self.evolution.state()["enabled"], "Evolution policy prohibits activation")
        if case.get("evolutionDecisionRef"):
            decisions = [d for d in self.evolution.records("decision") if d["experimentRef"] == experiment["id"]]
            require(decisions and decisions[-1]["id"] == case["evolutionDecisionRef"], "Evolution decision superseded")
            require(decisions[-1]["decision"] == "adopt", "Evolution adoption is unavailable")
        return experiment, evaluation

    def _review(self, case):
        spec = self.evolution.get(case["experimentRef"], "experiment")["spec"]
        review = self.management.review(case["initiativeRef"], spec["windowStart"], spec["windowEnd"],
                                        "change", "Assess the imported synthetic Evolution comparison.", spec["reviewBefore"])
        require(review["data"]["assessment"] == "supported", "Management evidence no longer supports adoption")
        return review

    def _current_authority(self, case):
        self._evolution_ready(case)
        require(case.get("managementDecisionRef"), "Management approval is required")
        mandate = self.management.get(case["mandateRef"])
        decision = self.management.get(case["managementDecisionRef"])
        require(mandate["data"]["purpose"] == case["mandatePurpose"], "Management mandate binding changed")
        require(decision["data"]["subjectRef"] == case["mandateRef"] and decision["data"]["choice"] == "approve",
                "Management decision does not approve this exact mandate")
        require(self.management.mandate_state(case["mandateRef"]) == "active", "Management mandate is not active")
        require(self.clock() < timestamp(decision["data"]["reviewAt"]), "Management decision is due for review")
        self._review(case)

    def prepare(self, experiment_id, evaluation_id, actor="owner-a"):
        self._owner(actor)
        with self._write():
            require(self.db.execute("SELECT 1 FROM cases WHERE experiment_id = ?", (experiment_id,)).fetchone() is None,
                    "this experiment already has a family case; resume it instead")
            case = {"id": "family-" + uuid.uuid4().hex, "experimentRef": experiment_id,
                    "evaluationRef": evaluation_id, "expectedEvolutionState": self.evolution.state()}
            experiment, evaluation = self._evolution_ready(case)
            spec = experiment["spec"]
            case["candidateRef"] = spec["candidateRef"]
            case["candidateDigest"] = self.evolution.get(spec["candidateRef"], "config")["artifactDigest"]
            case["binding"] = digest({"experiment": experiment, "evaluation": evaluation,
                                      "candidateDigest": case["candidateDigest"], "expected": case["expectedEvolutionState"]})
            comparisons = {c["metric"]: c for c in evaluation["comparisons"]}
            criteria = []
            for criterion in spec["criteria"]:
                baseline = comparisons[criterion["metric"]]["baseline"]
                higher = criterion["direction"] == "higher"
                threshold = (max(criterion["candidateLimit"], baseline + criterion["minimumGain"]) if higher
                             else min(criterion["candidateLimit"], baseline - criterion["minimumGain"]))
                criteria.append({"id": criterion["metric"], "claim": "Synthetic candidate comparison: " + criterion["metric"],
                                 "unit": criterion["unit"], "operator": "gte" if higher else "lte", "threshold": threshold,
                                 "maxAgeSeconds": spec["maxAgeSeconds"], "method": spec["method"], "population": spec["population"]})
            initiative = self.management.create_initiative({
                "title": "Bounded Evolution adoption " + case["id"], "outcome": spec["hypothesis"], "owner": "owner-a",
                "beneficiaries": "Synthetic support-team fixture; no real participants", "baseline": spec["baselineRef"],
                "assumptions": ["Synthetic measurements exercise record handling only"], "alternatives": ["Keep the baseline"],
                "criteria": criteria, "budgetMinor": 1000, "currency": "USD", "reviewAt": spec["reviewBefore"],
                "stopConditions": ["Changed evidence, inactive mandate, denied Engineering permission, or unavailable readback"],
                "dependencies": ["Pinned TUN companion source: " + canonical(PINS)],
            })
            case["initiativeRef"] = ref(initiative)
            for observation_id in evaluation["evidenceRefs"]:
                observation = self.evolution.get(observation_id)
                if observation.get("configRef") != spec["candidateRef"]:
                    continue
                self.management.observe({
                    "initiativeRef": ref(initiative), "kind": "outcome", "criterionId": observation["metric"],
                    "status": "measured", "value": observation["value"], "unit": observation["unit"],
                    "source": "evolution:" + observation_id, "method": observation["method"], "population": observation["population"],
                    "windowStart": observation["windowStart"], "windowEnd": observation["windowEnd"],
                    "observedAt": observation["observedAt"], "limitations": [observation["limitations"], evaluation["claimScope"]],
                    "supersedes": None,
                })
            case["managementReviewRef"] = ref(self._review(case))
            case["mandatePurpose"] = canonical({"action": "publish the bound adoption manifest, then activate its local configuration",
                                               "candidateRef": case["candidateRef"], "learningBinding": case["binding"]})
            mandate = self.management.propose_mandate({
                "initiativeRef": ref(initiative), "purpose": case["mandatePurpose"], "delegate": "agent-a",
                "actions": ["publish-manifest"], "targets": [TARGET], "dataScope": "Synthetic evidence and local configuration only",
                "budgetMinor": 1000, "startsAt": self.clock().isoformat(), "expiresAt": spec["reviewBefore"],
                "escalation": "Owner reviews changed evidence and unresolved publication; reservation is not execution authority",
                "furtherDelegation": False,
            })
            case["mandateRef"] = ref(mandate)
            self.db.execute("INSERT INTO cases(id, experiment_id, body) VALUES (?, ?, ?)", (case["id"], experiment_id, canonical(case)))
            return self._save(case, "prepared")

    def approve_adoption(self, case_id, rationale, actor="owner-a"):
        self._owner(actor)
        nonempty(rationale, "rationale")
        with self._write():
            case = self.case(case_id)
            experiment, evaluation = self._evolution_ready(case)
            require(not case.get("managementDecisionRef"), "adoption already recorded; resume the case")
            review = self._review(case)
            decision = self.management.decide(case["mandateRef"], "approve", rationale,
                                              ["Keep the baseline", "Collect more evidence"], experiment["spec"]["reviewBefore"], [ref(review)])
            case["managementDecisionRef"] = ref(decision)
            derived = self.evolution.decide(experiment["id"], evaluation["id"], "adopt",
                                           "Imported Management decision " + canonical(ref(decision)) + ": " + rationale)
            case["evolutionDecisionRef"] = derived["id"]
            case["manifest"] = {
                "schemaVersion": "tun-family-manifest/0.1", "caseRef": case_id, "learningBinding": case["binding"],
                "candidateRef": case["candidateRef"], "candidateDigest": case["candidateDigest"],
                "experimentRef": experiment["id"], "evaluationRef": evaluation["id"], "evidenceDigest": evaluation["evidenceDigest"],
                "managementMandateRef": case["mandateRef"], "managementDecisionRef": ref(decision),
                "evolutionDecisionRef": derived["id"], "sourceRevisions": PINS,
                "claim": "Candidate adoption record for a synthetic local trial; publication does not establish activation or benefit.",
            }
            proposal = self.engineering.propose(self.principal, TARGET, canonical(case["manifest"]))
            case["proposal"] = proposal
            return self._save(case, "adoption-recorded")

    def authorize_publication(self, case_id, proposal_id, proposal_version, actor="owner-a"):
        self._owner(actor)
        with self._write():
            case = self.case(case_id)
            self._current_authority(case)
            proposal = case["proposal"]
            require((proposal_id, proposal_version) == (proposal["id"], proposal["version"]), "publication approval version mismatch")
            decision = self.engineering.decide(self.principal, {"id": proposal_id, "version": proposal_version},
                                               "approve", case_id + "-publication-decision")
            case["publicationDecisionRef"] = {"id": decision["id"], "version": decision["version"]}
            reservation = self.delegate.reserve(case["mandateRef"], case_id + "-reservation", "publish-manifest", TARGET, 100)
            case["managementReservationRef"] = ref(reservation)
            case["operationId"] = self.engineering.reserve(self.principal, {"id": proposal_id, "version": proposal_version}, decision["id"])
            return self._save(case, "publication-authorized")

    def dispatch(self, case_id, actor="owner-a", fault=None):
        self._owner(actor)
        with self._write():
            case = self.case(case_id)
            self._current_authority(case)
            require(case.get("operationId"), "authorize publication before dispatch")
            receipt = self.engineering.dispatch(self.principal, case["operationId"], fault=fault)
            self._save(case, "publication-dispatched")
            return receipt

    def reconcile(self, case_id, actor="owner-a"):
        self._owner(actor)
        # Reconciliation reads historical effects, including after a mandate pause.
        with self._write():
            case = self.case(case_id)
            require(case.get("operationId"), "no publication to reconcile")
            receipt = self.engineering.reconcile(self.principal, case["operationId"])
            self._save(case, "publication-reviewed")
            return receipt

    def activate(self, case_id, actor="owner-a", fault=None):
        self._owner(actor)
        require(fault in (None, "after-evolution-commit"), "unsupported bridge fault")
        with self._write():
            case = self.case(case_id)
            require(case.get("evolutionDecisionRef"), "adoption decision is missing")
            prior = [r for r in self.evolution.records("activation") if r["decisionRef"] == case["evolutionDecisionRef"]]
            if prior:
                # Recover the durable result if the bridge stopped after Evolution committed.
                case["activationRef"] = prior[0]["id"]
                self._save(case, "activation-recorded")
                return prior[0]
            self._current_authority(case)
            require(case.get("operationId"), "publication has not been authorized")
            receipt = self.engineering.reconcile(self.principal, case["operationId"])
            require(receipt["status"] == "completed" and receipt["verificationState"] == "verified",
                    "publication is not verified; keep the baseline and reconcile the original operation")
            resource = self.provider.resource(self.principal.scope, case["operationId"])
            require(resource and resource["target"] == TARGET and resource["content"] == canonical(case["manifest"])
                    and resource["revision"] == 1 and not resource["withdrawn"], "current publication no longer matches the approved manifest")
            activation = self.evolution.activate(case["evolutionDecisionRef"])
            if fault == "after-evolution-commit":
                raise InterruptedError("fixture crash after Evolution committed, before bridge acknowledgement")
            case["activationRef"] = activation["id"]
            self._save(case, "activation-recorded")
            return activation

    def report(self, case_id):
        case = self.case(case_id)
        current_assessment = self.evolution._assess(self.evolution.get(case["experimentRef"]))
        original_assessment = self.evolution.get(case["evaluationRef"])
        try:
            mandate_state = self.management.mandate_state(case["mandateRef"])
        except ManagementConflict:
            mandate_state = "superseded"
        receipt = self.engineering.receipt(self.principal, case["operationId"]) if case.get("operationId") else None
        proposal = case.get("proposal")
        view = receipt_view(receipt, proposal) if receipt and receipt["status"] not in ("queued", "blocked", "cancelled") else None
        if view:
            view["action"] = "Publish adoption manifest"
        projected = proposal_view(proposal) if proposal else None
        if projected:
            projected["action"] = "Publish adoption manifest"
        activations = [r for r in self.evolution.records("activation") if r["decisionRef"] == case.get("evolutionDecisionRef")]
        activation = activations[0] if activations else None
        return {
            "schemaVersion": "tun-family-review/0.1", "caseId": case_id, "sourceRevisions": PINS,
            "scenario": "Synthetic local companion integration; no model or real participants.",
            "phase": case["phase"], "management": {"initiativeRef": case["initiativeRef"], "mandateRef": case["mandateRef"],
                "decisionRef": case.get("managementDecisionRef"), "state": mandate_state,
                "budget": self.management.budget(case["initiativeRef"])},
            "evolution": {"experimentRef": case["experimentRef"], "evaluationRef": case["evaluationRef"],
                "assessment": current_assessment["result"], "reviewAssessment": original_assessment["result"],
                "evidenceChanged": current_assessment["evidenceDigest"] != original_assessment["evidenceDigest"], "activation": activation,
                "currentState": self.evolution.state(), "activationStillCurrent": bool(activation and
                    all(activation["after"][key] == self.evolution.state()[key] for key in ("active", "generation")))},
            "engineering": {"operationId": case.get("operationId"), "receipt": receipt, "providerEffects": self.provider.count()},
            "design": {"proposal": projected, "approvalStatus": "approved" if case.get("publicationDecisionRef") else "awaiting", "receipt": view},
            "limitations": ["Fixture identities and synthetic observations; no production authentication or learning claim.",
                            "The Engineering receipt verifies manifest publication; Evolution activation is reported separately.",
                            "Bridge calls serialize locally; independent store changes are not atomic with provider or activation effects.",
                            "Integrated withdrawal and rollback are not implemented; existing standalone recovery remains separate."],
        }
