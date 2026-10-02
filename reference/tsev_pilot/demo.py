"""Run with: python -m reference.tsev_pilot.demo"""

import argparse
from pathlib import Path
from tempfile import TemporaryDirectory

from .contracts import Rejected
from .fixtures import (
    FAST_UNSAFE_VALUES, FixtureClock, experiment_spec, fill_evidence, seed,
)
from .runtime import Pilot


def run(path):
    clock = FixtureClock()
    pilot = Pilot(path, clock=clock)
    try:
        baseline, candidate, experiment = seed(pilot)
        fast = pilot.add_config("Fast candidate", "Fixture: shorten the explanation to reduce review time.")
        fast_experiment = pilot.add_experiment(experiment_spec(baseline["id"], fast["id"]))
        fill_evidence(pilot, fast_experiment, FAST_UNSAFE_VALUES)
        fast_evaluation = pilot.evaluate(fast_experiment["id"])
        pilot.decide(fast_experiment["id"], fast_evaluation["id"], "reject",
                     "Human error detection regressed despite faster review.")
        print("All measurements below are synthetic; no model or person was evaluated.")
        print("Fast candidate:", fast_evaluation["result"], "(human detection 85 -> 70).")

        fill_evidence(pilot, experiment)
        evaluation = pilot.evaluate(experiment["id"])
        print("Evidence-first candidate:", evaluation["result"], "(quality 80 -> 90; human detection 85 -> 90).")
        try:
            pilot.decide(experiment["id"], evaluation["id"], "adopt", "AI recommends adoption.", actor="agent-fixture")
        except Rejected:
            print("Agent self-approval: blocked.")
        decision = pilot.decide(experiment["id"], evaluation["id"], "adopt",
                                "Adopt only in the synthetic local configuration sandbox.")
        activation = pilot.activate(decision["id"])
        print("Owner adoption: recorded; local configuration activation: verified.")
        monitoring = pilot.monitor(activation["id"], {"quality": 90, "human_detection": 70, "review_minutes": 4},
                                   "synthetic-monitor", "Fabricated regression; no production monitoring.")
        print("Post-activation monitoring:", monitoring["result"], "(human detection falls to 70).")
        recovery = pilot.rollback(activation["id"], monitoring["id"], "Restore baseline after the synthetic regression.")
        print("Owner-requested rollback:", "verified" if recovery["after"]["active"] == baseline["id"] else "unresolved")
        expected_count = len(pilot.records())
    finally:
        pilot.close()
    reopened = Pilot(path, clock=clock)
    try:
        if reopened.state()["active"] != baseline["id"] or len(reopened.records()) != expected_count:
            raise RuntimeError("restart verification failed")
        print(f"Restart: baseline restored and all {expected_count} journal records retained.")
        print("Verified scope: local record decisions and configuration pointer only.")
    finally:
        reopened.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, help="retain the demonstration in a NEW SQLite file")
    args = parser.parse_args()
    if args.db:
        args.db.parent.mkdir(parents=True, exist_ok=True)
        try:
            with args.db.open("xb"):
                pass
        except FileExistsError:
            parser.error("database path already exists; choose a new path")
        run(args.db)
    else:
        with TemporaryDirectory(prefix="tsev-pilot-") as temp:
            run(Path(temp) / "pilot.sqlite3")


if __name__ == "__main__":
    main()
