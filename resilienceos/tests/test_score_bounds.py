from __future__ import annotations

from resilienceos.environment import ResilienceOSEnvironment
from resilienceos.baseline import choose_action


def test_scores_are_bounded() -> None:
    for task in ["easy", "medium", "hard"]:
        env = ResilienceOSEnvironment()
        observation = env.reset(task=task, seed=7)
        done = False
        score = 0.0
        while not done:
            action = choose_action(task=task, observation=observation)
            result = env.step(action)
            observation = result.observation
            done = result.done
            score = result.score
        assert 0.0 <= score <= 1.0
