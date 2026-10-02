from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Barrier
import unittest

from reference.tsev_pilot.contracts import Rejected, validate_experiment
from reference.tsev_pilot.fixtures import (
    FAST_UNSAFE_VALUES, FixtureClock, add_observation, experiment_spec, fill_evidence, seed,
)
from reference.tsev_pilot.runtime import Pilot


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix="tsev-test-")
        self.path = Path(self.temp.name) / "pilot.sqlite3"
        self.clock = FixtureClock()
        self.pilot = Pilot(self.path, clock=self.clock)
        self.baseline, self.candidate, self.experiment = seed(self.pilot)

    def tearDown(self):
        self.pilot.close()
        self.temp.cleanup()

    def evaluation(self):
        fill_evidence(self.pilot, self.experiment)
        return self.pilot.evaluate(self.experiment["id"])

    def decision(self):
        evaluation = self.evaluation()
        return self.pilot.decide(self.experiment["id"], evaluation["id"], "adopt", "Synthetic sandbox only.")

    def activation_and_monitor(self):
        activation = self.pilot.activate(self.decision()["id"])
        monitoring = self.pilot.monitor(activation["id"], {"quality": 90, "human_detection": 70, "review_minutes": 4},
                                       "synthetic-test", "Synthetic regression.")
        return activation, monitoring

    def test_supported_decision_does_not_activate_until_separate_command(self):
        decision = self.decision()
        self.assertEqual(self.pilot.state()["active"], self.baseline["id"])
        activation = self.pilot.activate(decision["id"])
        self.assertEqual(activation["after"]["active"], self.candidate["id"])
        self.assertEqual(len(self.pilot.records("activation")), 1)

    def test_faster_candidate_with_human_regression_cannot_be_adopted(self):
        fill_evidence(self.pilot, self.experiment, FAST_UNSAFE_VALUES)
        evaluation = self.pilot.evaluate(self.experiment["id"])
        self.assertEqual(evaluation["result"], "contradicted")
        self.assertTrue(any("human_detection" in value for value in evaluation["failures"]))
        with self.assertRaises(Rejected):
            self.pilot.decide(self.experiment["id"], evaluation["id"], "adopt", "Speed alone.")
        rejection = self.pilot.decide(self.experiment["id"], evaluation["id"], "reject", "Human regression.")
        self.assertEqual(rejection["decision"], "reject")

    def test_lower_is_better_criterion_rejects_increased_review_time(self):
        fill_evidence(self.pilot, self.experiment, {"quality": 90, "human_detection": 90, "review_minutes": 7})
        self.assertEqual(self.pilot.evaluate(self.experiment["id"])["result"], "contradicted")

    def test_missing_evidence_is_insufficient(self):
        self.assertEqual(self.pilot.evaluate(self.experiment["id"])["result"], "insufficient")

    def test_missing_value_and_small_sample_are_insufficient(self):
        fill_evidence(self.pilot, self.experiment, {"quality": None, "human_detection": 90, "review_minutes": 4},
                      {"cases": 19})
        self.assertEqual(self.pilot.evaluate(self.experiment["id"])["result"], "insufficient")

    def test_population_method_unit_and_window_mismatch_are_not_accepted(self):
        for field, value in (("population", "other-population"), ("method", "other-method"),
                             ("unit", "other-unit"), ("window_start", "2026-10-02T08:00:00Z")):
            with self.subTest(field=field):
                experiment = self.pilot.add_experiment(self.experiment["spec"])
                fill_evidence(self.pilot, experiment, overrides={field: value})
                result = self.pilot.evaluate(experiment["id"])
                self.assertEqual(result["result"], "insufficient")
                self.assertTrue(any("mismatch" in item for item in result["issues"]))

    def test_conflicting_observations_remain_visible(self):
        self.evaluation()
        add_observation(self.pilot, self.experiment, self.candidate["id"], "quality", 60)
        result = self.pilot.evaluate(self.experiment["id"])
        self.assertEqual(result["result"], "insufficient")
        self.assertEqual(len(result["evidenceRefs"]), 7)
        self.assertTrue(any("conflicting" in issue for issue in result["issues"]))

    def test_known_failure_is_not_hidden_by_missing_other_evidence(self):
        for ref, value in ((self.baseline["id"], 85), (self.candidate["id"], 70)):
            add_observation(self.pilot, self.experiment, ref, "human_detection", value)
        result = self.pilot.evaluate(self.experiment["id"])
        self.assertEqual(result["result"], "contradicted")
        self.assertTrue(result["issues"])
        self.assertTrue(result["failures"])

    def test_stale_evidence_invalidates_previous_approval(self):
        decision = self.decision()
        self.clock.advance(7201)
        with self.assertRaises(Rejected):
            self.pilot.activate(decision["id"])
        self.assertEqual(self.pilot.state()["active"], self.baseline["id"])

    def test_expired_experiment_cannot_activate(self):
        decision = self.decision()
        self.clock.advance(86401)
        with self.assertRaises(Rejected):
            self.pilot.activate(decision["id"])

    def test_new_evidence_requires_a_new_evaluation(self):
        decision = self.decision()
        add_observation(self.pilot, self.experiment, self.candidate["id"], "quality", 92)
        with self.assertRaisesRegex(Rejected, "evidence changed"):
            self.pilot.activate(decision["id"])

    def test_unstructured_concern_blocks_adoption_even_with_passing_metrics(self):
        self.evaluation()
        self.pilot.flag_concern(self.experiment["id"], "Participant reports a material adverse effect.")
        result = self.pilot.evaluate(self.experiment["id"])
        self.assertEqual(result["result"], "insufficient")
        self.assertTrue(any("adverse" in issue for issue in result["issues"]))

    def test_agent_cannot_approve_activate_or_restore(self):
        evaluation = self.evaluation()
        with self.assertRaises(Rejected):
            self.pilot.decide(self.experiment["id"], evaluation["id"], "adopt", "I approve.", actor="agent-fixture")
        decision = self.pilot.decide(self.experiment["id"], evaluation["id"], "adopt", "Owner review.")
        with self.assertRaises(Rejected):
            self.pilot.activate(decision["id"], actor="agent-fixture")
        with self.assertRaises(Rejected):
            self.pilot.rollback("any", "any", "Restore.", actor="agent-fixture")

    def test_permission_revocation_and_renewal_invalidate_prior_decision(self):
        decision = self.decision()
        self.pilot.set_policy_enabled(False)
        with self.assertRaises(Rejected):
            self.pilot.activate(decision["id"])
        self.pilot.set_policy_enabled(True)
        with self.assertRaises(Rejected):
            self.pilot.activate(decision["id"])
        new_decision = self.pilot.decide(self.experiment["id"], decision["evaluationRef"], "adopt", "Review renewed policy.")
        self.pilot.activate(new_decision["id"])

    def test_later_rejection_supersedes_earlier_adoption(self):
        decision = self.decision()
        self.pilot.decide(self.experiment["id"], decision["evaluationRef"], "reject", "Do not proceed.")
        with self.assertRaisesRegex(Rejected, "superseded"):
            self.pilot.activate(decision["id"])

    def test_changed_experiment_cannot_reuse_evaluation(self):
        evaluation = self.evaluation()
        changed = deepcopy(self.experiment["spec"])
        changed["criteria"][0]["candidateLimit"] = 99
        new_experiment = self.pilot.add_experiment(changed)
        with self.assertRaises(Rejected):
            self.pilot.decide(new_experiment["id"], evaluation["id"], "adopt", "Reuse old evidence.")
        self.assertEqual(self.pilot.get(self.experiment["id"])["spec"]["criteria"][0]["candidateLimit"], 85)

    def test_capability_and_data_scope_expansion_are_blocked(self):
        for args in ({"capabilities": ["draft", "publish"]}, {"data_scope": "customer-data"}, {"scope": "another-team"}):
            with self.subTest(args=args):
                candidate = self.pilot.add_config("Expanded", "Expanded fixture.", **args)
                with self.assertRaises(Rejected):
                    self.pilot.add_experiment(experiment_spec(self.baseline["id"], candidate["id"]))

    def test_unrelated_configuration_evidence_is_rejected(self):
        unrelated = self.pilot.add_config("Unrelated", "Unrelated fixture.")
        before = len(self.pilot.records())
        with self.assertRaises(Rejected):
            add_observation(self.pilot, self.experiment, unrelated["id"], "quality", 99)
        self.assertEqual(len(self.pilot.records()), before)

    def test_non_finite_boolean_and_future_values_are_rejected(self):
        for bad in (float("nan"), float("inf"), True):
            with self.subTest(bad=str(bad)), self.assertRaises(Rejected):
                add_observation(self.pilot, self.experiment, self.candidate["id"], "quality", bad)
        with self.assertRaises(Rejected):
            add_observation(self.pilot, self.experiment, self.candidate["id"], "quality", 90,
                            observed_at="2026-10-02T13:00:00Z")

    def test_profile_rejects_ambiguous_versions_fields_and_timestamps(self):
        changes = [{"schemaVersion": "future"}, {"extra": "unsupported"}, {"minCases": True},
                   {"windowStart": "2026-10-02T09:00:00"}, {"windowEnd": "2026-10-01T09:00:00Z"}]
        for change in changes:
            spec = dict(self.experiment["spec"], **change)
            with self.subTest(change=change), self.assertRaises(Rejected):
                validate_experiment(spec)
        spec = deepcopy(self.experiment["spec"])
        spec["criteria"].append(spec["criteria"][0])
        with self.assertRaises(Rejected):
            validate_experiment(spec)

    def test_restart_preserves_activation_monitoring_and_recovery_history(self):
        activation, monitoring = self.activation_and_monitor()
        self.assertEqual(monitoring["result"], "concerning")
        self.assertEqual(self.pilot.state()["active"], self.candidate["id"])
        recovery = self.pilot.rollback(activation["id"], monitoring["id"], "Synthetic regression.")
        ids_before = [r["id"] for r in self.pilot.records()]
        self.pilot.close()
        self.pilot = Pilot(self.path, clock=self.clock)
        self.assertEqual(self.pilot.state()["active"], self.baseline["id"])
        self.assertEqual([r["id"] for r in self.pilot.records()], ids_before)
        self.assertEqual(self.pilot.get(recovery["id"])["activationRef"], activation["id"])

    def test_rollback_cannot_overwrite_intervening_activation_even_same_artifact(self):
        activation, monitoring = self.activation_and_monitor()
        self.pilot.rollback(activation["id"], monitoring["id"], "First restoration.")
        original_decision = self.pilot.get(activation["decisionRef"])
        new_decision = self.pilot.decide(self.experiment["id"], original_decision["evaluationRef"], "adopt", "Another local trial.")
        self.pilot.activate(new_decision["id"])
        with self.assertRaisesRegex(Rejected, "intervening"):
            self.pilot.rollback(activation["id"], monitoring["id"], "Stale rollback request.")

    def test_repeated_activation_is_blocked(self):
        decision = self.decision()
        self.pilot.activate(decision["id"])
        with self.assertRaises(Rejected):
            self.pilot.activate(decision["id"])
        self.assertEqual(len(self.pilot.records("activation")), 1)

    def test_concurrent_activation_commits_only_one_local_change(self):
        decision = self.decision()
        barrier = Barrier(2)

        def activate():
            other = Pilot(self.path, clock=self.clock)
            try:
                barrier.wait(timeout=10)
                try:
                    other.activate(decision["id"])
                    return "activated"
                except Rejected:
                    return "rejected"
            finally:
                other.close()

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(lambda _: activate(), range(2)))
        self.assertCountEqual(outcomes, ["activated", "rejected"])
        self.assertEqual(len(self.pilot.records("activation")), 1)
        self.assertEqual(self.pilot.state()["generation"], 2)

    def test_missing_monitoring_is_visible_and_does_not_auto_restore(self):
        activation = self.pilot.activate(self.decision()["id"])
        review = self.pilot.monitor(activation["id"], {"quality": None, "human_detection": 90, "review_minutes": 4},
                                   "synthetic-test", "Missing fixture value.")
        self.assertEqual(review["result"], "unavailable")
        self.assertEqual(self.pilot.state()["active"], self.candidate["id"])

    def test_rollback_requires_current_permission_and_fresh_review(self):
        activation, monitoring = self.activation_and_monitor()
        self.pilot.set_policy_enabled(False)
        with self.assertRaises(Rejected):
            self.pilot.rollback(activation["id"], monitoring["id"], "Revoked policy.")
        self.pilot.set_policy_enabled(True)
        self.clock.advance(7201)
        with self.assertRaises(Rejected):
            self.pilot.rollback(activation["id"], monitoring["id"], "Old monitoring.")

    def test_monitoring_from_another_activation_cannot_justify_rollback(self):
        activation, monitoring = self.activation_and_monitor()
        self.pilot.rollback(activation["id"], monitoring["id"], "Restore.")
        original = self.pilot.get(activation["decisionRef"])
        decision = self.pilot.decide(self.experiment["id"], original["evaluationRef"], "adopt", "New trial.")
        newer = self.pilot.activate(decision["id"])
        with self.assertRaises(Rejected):
            self.pilot.rollback(newer["id"], monitoring["id"], "Wrong monitoring record.")


if __name__ == "__main__":
    unittest.main()
