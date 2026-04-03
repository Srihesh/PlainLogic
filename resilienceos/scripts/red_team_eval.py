from __future__ import annotations

import json
from pathlib import Path

from resilienceos.red_team import run_bad_resource_case, run_invalid_payload_case, run_loop_case


def main() -> None:
    output_path = Path("outputs/red_team_report.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "env": "resilienceos",
        "red_team_cases": [
            run_invalid_payload_case(),
            run_loop_case(),
            run_bad_resource_case(),
        ],
    }
    report["all_scores_bounded"] = all(
        0.0 <= case["final_score"] <= 1.0 for case in report["red_team_cases"]
    )

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
