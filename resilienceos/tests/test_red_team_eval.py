from __future__ import annotations

from resilienceos.red_team import run_bad_resource_case, run_invalid_payload_case, run_loop_case


def test_red_team_cases_bounded_scores() -> None:
    cases = [run_invalid_payload_case(), run_loop_case(), run_bad_resource_case()]
    for case in cases:
        assert 0.0 <= case["final_score"] <= 1.0
