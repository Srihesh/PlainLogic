from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import _bootstrap
from resilienceos.baseline import run_task


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--output", type=str, default="outputs/baseline_report.json")
    args = parser.parse_args()

    tasks = ["easy", "medium", "hard"]
    task_reports = [run_task(task=t, seed=args.seed) for t in tasks]
    aggregate = sum(r["final_score"] for r in task_reports) / len(task_reports)

    report = {
        "env": "resilienceos",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "seed": args.seed,
        "tasks": task_reports,
        "aggregate_score": round(aggregate, 6),
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
