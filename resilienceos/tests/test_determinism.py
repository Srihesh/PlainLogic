from __future__ import annotations

from resilienceos.baseline import run_task


def test_same_seed_reproducible() -> None:
    tasks = ["easy", "medium", "hard"]
    a = [run_task(task=t, seed=7) for t in tasks]
    b = [run_task(task=t, seed=7) for t in tasks]
    assert a == b
