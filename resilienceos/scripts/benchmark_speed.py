from __future__ import annotations

import time

import _bootstrap
from resilienceos.baseline import run_task


def main() -> None:
    seed = 7
    tasks = ["easy", "medium", "hard"]
    iterations = 200

    t0 = time.perf_counter()
    total_runs = 0
    agg = 0.0
    for _ in range(iterations):
        for task in tasks:
            report = run_task(task=task, seed=seed)
            total_runs += 1
            agg += report["final_score"]
    dt = time.perf_counter() - t0

    print(
        {
            "iterations": iterations,
            "total_task_runs": total_runs,
            "avg_task_run_ms": round((dt / total_runs) * 1000, 4),
            "task_runs_per_sec": round(total_runs / dt, 2),
            "avg_score": round(agg / total_runs, 6),
        }
    )


if __name__ == "__main__":
    main()
