from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from reference.tsev_family.bridge import FamilyBridge, TARGET
from reference.tsev_pilot.contracts import Rejected
from reference.tsev_pilot.fixtures import FixtureClock, add_observation, fill_evidence, seed
from vendor.engineering.reference.tse_pilot.runtime import Denied, SimulatedCrash
from vendor.management.reference.tsm_pilot.runtime import Conflict


class FamilyTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix="tun-family-test-")
        self.directory = Path(self.temp.name)
        self.clock = FixtureClock()
        self.bridge = FamilyBridge(self.directory, clock=self.clock)
        self.baseline, self.candidate, self.experiment = seed(self.bridge.evolution)
        fill_evidence(self.bridge.evolution, self.experiment)
        self.evaluation = self.bridge.evolution.evaluate(self.experiment["id"])
        self.bridge.engineering.set_permission(self.bridge.principal, TARGET, True)
        self.bridge.engineering.set_dispatch_budget(self.bridge.principal, 2)
        self.case = self.bridge.prepare(self.experiment["id"], self.evaluation["id"])

    def tearDown(self):
        self.bridge.close()
        self.temp.cleanup()

    def adopted(self):
        self.case = self.bridge.approve_adoption(self.case["id"], "Approve the synthetic bounded candidate.")
        return self.case

    def authorized(self):
        self.adopted()
        self.case = self.bridge.authorize_publication(self.case["id"], self.case["proposal"]["id"], self.case["proposal"]["version"])
        return self.case

    def test_management_import_preserves_gain_thresholds_and_typed_references(self):
        initiative = self.bridge.management.get(self.case["initiativeRef"])
        thresholds = {c["id"]: c["threshold"] for c in initiative["data"]["criteria"]}
        self.assertEqual(thresholds, {"quality": 85, "human_detection": 85, "review_minutes": 5})
        self.assertIs(type(self.case["mandateRef"]["version"]), int)
        self.adopted()
        self.assertIs(type(self.case["proposal"]["version"]), str)
        self.assertEqual(self.bridge.evolution.state()["active"], self.baseline["id"])

    def test_manifest_binds_management_decision_candidate_and_evaluation(self):
        self.adopted()
        manifest = self.case["manifest"]
        self.assertEqual(manifest["candidateDigest"], self.candidate["artifactDigest"])
        self.assertEqual(manifest["evaluationRef"], self.evaluation["id"])
        self.assertEqual(manifest["managementDecisionRef"], self.case["managementDecisionRef"])
        decision = self.bridge.management.get(manifest["managementDecisionRef"])
        self.assertEqual(decision["data"]["subjectRef"], self.case["mandateRef"])
        mandate = self.bridge.management.get(self.case["mandateRef"])
        self.assertIn(self.case["binding"], mandate["data"]["purpose"])

    def test_agent_cannot_make_the_management_adoption_decision(self):
        with self.assertRaises(Rejected):
            self.bridge.approve_adoption(self.case["id"], "AI approves itself.", actor="agent-a")

    def test_evidence_changed_between_prepare_and_approval_blocks_adoption(self):
        add_observation(self.bridge.evolution, self.experiment, self.candidate["id"], "quality", 50)
        with self.assertRaises(Rejected):
            self.adopted()
        self.assertEqual(self.bridge.management.mandate_state(self.case["mandateRef"]), "proposed")
        report = self.bridge.report(self.case["id"])
        self.assertTrue(report["evolution"]["evidenceChanged"])
        self.assertEqual(report["evolution"]["assessment"], "insufficient")

    def test_stale_publication_approval_is_rejected(self):
        self.adopted()
        with self.assertRaises(Rejected):
            self.bridge.authorize_publication(self.case["id"], self.case["proposal"]["id"], "2")
        self.assertEqual(self.bridge.management.budget(self.case["initiativeRef"])["reservedMinor"], 0)

    def test_paused_mandate_blocks_dispatch_after_reservation(self):
        self.authorized()
        self.bridge.management.decide(self.case["mandateRef"], "pause", "Stop new effects.", ["Continue"], "2026-10-03T12:00:00Z")
        with self.assertRaises(Rejected):
            self.bridge.dispatch(self.case["id"])
        self.assertEqual(self.bridge.provider.count(), 0)
        self.assertEqual(self.bridge.management.budget(self.case["initiativeRef"])["reservedMinor"], 100)

    def test_engineering_revocation_blocks_dispatch_despite_management_approval(self):
        self.authorized()
        self.bridge.engineering.set_permission(self.bridge.principal, TARGET, False)
        with self.assertRaises(Denied):
            self.bridge.dispatch(self.case["id"])
        self.assertEqual(self.bridge.provider.count(), 0)
        self.assertIsNone(self.bridge.report(self.case["id"])["design"]["receipt"])

    def test_changed_management_mandate_blocks_and_remains_reportable(self):
        self.authorized()
        data = deepcopy(self.bridge.management.get(self.case["mandateRef"])["data"])
        data["purpose"] = "Different purpose requires a new decision."
        self.bridge.management.propose_mandate(data, previous=self.case["mandateRef"])
        with self.assertRaises(Conflict):
            self.bridge.dispatch(self.case["id"])
        self.assertEqual(self.bridge.report(self.case["id"])["management"]["state"], "superseded")

    def test_lost_response_and_unavailable_readback_preserve_baseline(self):
        self.authorized()
        receipt = self.bridge.dispatch(self.case["id"], fault="lost-response")
        self.assertEqual(receipt["effectKnowledge"], "unknown")
        self.bridge.provider.lookup_available = False
        with self.assertRaises(Rejected):
            self.bridge.activate(self.case["id"])
        self.assertEqual(self.bridge.evolution.state()["active"], self.baseline["id"])
        report = self.bridge.report(self.case["id"])
        self.assertEqual(report["design"]["receipt"]["status"], "pending-verification")
        self.assertEqual(report["design"]["receipt"]["verification"]["state"], "unavailable")

    def test_restart_reconciles_original_operation_without_duplicate_effect_or_reservation(self):
        self.authorized()
        self.bridge.dispatch(self.case["id"], fault="lost-response")
        operation = self.case["operationId"]
        self.bridge.close()
        self.bridge = FamilyBridge(self.directory, clock=self.clock)
        receipt = self.bridge.reconcile(self.case["id"])
        self.assertEqual(receipt["operationId"], operation)
        self.assertEqual(receipt["status"], "completed")
        activation = self.bridge.activate(self.case["id"])
        self.assertEqual(self.bridge.activate(self.case["id"])["id"], activation["id"])
        self.assertEqual(self.bridge.provider.count(), 1)
        self.assertEqual(self.bridge.management.budget(self.case["initiativeRef"])["reservedMinor"], 100)
        self.assertEqual(len(self.bridge.evolution.records("activation")), 1)

    def test_provider_commit_crash_can_be_reconciled_after_restart(self):
        self.authorized()
        with self.assertRaises(SimulatedCrash):
            self.bridge.dispatch(self.case["id"], fault="after-provider")
        self.bridge.close()
        self.bridge = FamilyBridge(self.directory, clock=self.clock)
        self.assertEqual(self.bridge.reconcile(self.case["id"])["status"], "completed")
        self.bridge.activate(self.case["id"])
        self.assertEqual(self.bridge.provider.count(), 1)

    def test_activation_acknowledgement_gap_recovers_existing_record(self):
        self.authorized()
        self.bridge.dispatch(self.case["id"])
        with self.assertRaises(InterruptedError):
            self.bridge.activate(self.case["id"], fault="after-evolution-commit")
        self.assertEqual(len(self.bridge.evolution.records("activation")), 1)
        self.assertNotIn("activationRef", self.bridge.case(self.case["id"]))
        self.bridge.close()
        self.bridge = FamilyBridge(self.directory, clock=self.clock)
        self.bridge.activate(self.case["id"])
        self.assertEqual(len(self.bridge.evolution.records("activation")), 1)
        self.assertIn("activationRef", self.bridge.case(self.case["id"]))

    def test_new_adverse_evidence_after_publication_blocks_activation_but_retains_effect(self):
        self.authorized()
        self.bridge.dispatch(self.case["id"])
        self.bridge.reconcile(self.case["id"])
        self.bridge.evolution.flag_concern(self.experiment["id"], "New material human concern.")
        with self.assertRaises(Rejected):
            self.bridge.activate(self.case["id"])
        self.assertEqual(self.bridge.provider.count(), 1)
        self.assertEqual(self.bridge.evolution.state()["active"], self.baseline["id"])

    def test_historical_publication_receipt_does_not_prove_current_manifest(self):
        self.authorized()
        self.bridge.dispatch(self.case["id"])
        self.bridge.reconcile(self.case["id"])
        self.bridge.engineering.set_permission(self.bridge.principal, TARGET, True, action="withdraw")
        proposal = self.bridge.engineering.propose_recovery(self.bridge.principal, self.case["operationId"], "withdraw")
        reference = {"id": proposal["id"], "version": proposal["version"]}
        decision = self.bridge.engineering.decide(self.bridge.principal, reference, "approve", "test-withdrawal")
        operation = self.bridge.engineering.reserve(self.bridge.principal, reference, decision["id"])
        self.bridge.engineering.dispatch(self.bridge.principal, operation)
        with self.assertRaisesRegex(Rejected, "current publication"):
            self.bridge.activate(self.case["id"])
        self.assertEqual(self.bridge.evolution.state()["active"], self.baseline["id"])

    def test_reconciliation_is_allowed_after_pause_but_activation_is_not(self):
        self.authorized()
        self.bridge.dispatch(self.case["id"], fault="lost-response")
        self.bridge.management.decide(self.case["mandateRef"], "pause", "Pause.", ["Continue"], "2026-10-03T12:00:00Z")
        self.assertEqual(self.bridge.reconcile(self.case["id"])["status"], "completed")
        with self.assertRaises(Rejected):
            self.bridge.activate(self.case["id"])

    def test_duplicate_case_cannot_replace_unresolved_operation(self):
        self.authorized()
        self.bridge.dispatch(self.case["id"], fault="lost-response")
        with self.assertRaises(Rejected):
            self.bridge.prepare(self.experiment["id"], self.evaluation["id"])
        self.assertEqual(self.bridge.provider.count(), 1)


if __name__ == "__main__":
    unittest.main()
