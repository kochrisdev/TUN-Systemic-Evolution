"""Run a synthetic example across actual pinned TUN companion implementations."""

import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from reference.tsev_pilot.contracts import Rejected
from reference.tsev_pilot.fixtures import FixtureClock, fill_evidence, seed
from .bridge import FamilyBridge, TARGET


def run(directory):
    clock = FixtureClock()
    bridge = FamilyBridge(directory, clock=clock)
    try:
        baseline, candidate, experiment = seed(bridge.evolution)
        fill_evidence(bridge.evolution, experiment)
        evaluation = bridge.evolution.evaluate(experiment["id"])
        bridge.engineering.set_permission(bridge.principal, TARGET, True)
        bridge.engineering.set_dispatch_budget(bridge.principal, 2)
        case = bridge.prepare(experiment["id"], evaluation["id"])
        case = bridge.approve_adoption(case["id"], "Approve this exact synthetic candidate within its bounded mandate.")
        case = bridge.authorize_publication(case["id"], case["proposal"]["id"], case["proposal"]["version"])
        unknown = bridge.dispatch(case["id"], fault="lost-response")
        assert unknown["status"] == "pending-verification"
        bridge.provider.lookup_available = False
        try:
            bridge.activate(case["id"])
        except Rejected:
            pass
        else:
            raise AssertionError("unavailable readback allowed activation")
        before = bridge.report(case["id"])
        assert bridge.evolution.state()["active"] == baseline["id"]
    finally:
        bridge.close()
    reopened = FamilyBridge(directory, clock=clock)
    try:
        verified = reopened.reconcile(case["id"])
        assert verified["status"] == "completed"
        activation = reopened.activate(case["id"])
        assert activation["after"]["active"] == candidate["id"]
        assert reopened.provider.count() == 1
        assert reopened.management.budget(case["initiativeRef"])["reservedMinor"] == 100
        after = reopened.report(case["id"])
        assert reopened.activate(case["id"])["id"] == activation["id"]
        return {"schemaVersion": "tun-family-demo/0.1", "before": before, "after": after,
                "checks": {"activationBlockedWithoutReadback": True, "restartRecoveredOriginalOperation": True,
                           "oneProviderEffect": True, "oneManagementReservation": True, "repeatActivationRecoveredSameRecord": True}}
    finally:
        reopened.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, help="new directory for the five local stores")
    parser.add_argument("--report", type=Path, help="new JSON report file for the optional Design renderer")
    args = parser.parse_args()
    if args.report and args.report.exists():
        parser.error("choose a new report path")
    if args.directory:
        args.directory.mkdir(parents=True, exist_ok=False)
        result = run(args.directory)
    else:
        with TemporaryDirectory(prefix="tun-family-") as directory:
            result = run(directory)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        with args.report.open("x", encoding="utf-8") as output:
            json.dump(result, output, indent=2, allow_nan=False)
            output.write("\n")
    print("Synthetic companion integration: no model or real participants.")
    print("Management: imported evidence reviewed; exact mandate approved; one USD 1.00 fixture reservation.")
    print("Engineering: publication response lost; unavailable readback blocked Evolution activation.")
    print("Restart: original publication reconciled; one provider effect verified.")
    print("Evolution: exact candidate activated locally; repeated activation returns its original record.")
    print("Design: actual proposal and receipt projections exported for the read-only React report.")
    if args.report:
        print("Report:", args.report)


if __name__ == "__main__":
    main()
