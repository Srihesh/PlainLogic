from __future__ import annotations

import json

import _bootstrap
from resilienceos.baseline import run_task


def main() -> None:
    seed = 7
    tasks = ["easy", "medium", "hard"]
    run_a = [run_task(task=t, seed=seed) for t in tasks]
    run_b = [run_task(task=t, seed=seed) for t in tasks]
    same = run_a == run_b
    result = {
        "seed": seed,
        "run_a": run_a,
        "run_b": run_b,
        "deterministic": same,
    }
    print(json.dumps(result, indent=2))
    if not same:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
