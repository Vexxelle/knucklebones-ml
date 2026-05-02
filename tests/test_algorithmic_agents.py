import numpy as np

from knucklebones_ml.agents import AggressiveAgent


def test_aggressive_agent():
    agent = AggressiveAgent()

    # fmt: off
    b = np.array([[[0, 0, 3],
                   [0, 6, 3],
                   [0, 2, 3]],
                  [[0, 0, 4],
                   [0, 4, 4],
                   [4, 4, 4]]])
    # fmt: on

    obs = {
        "board": b,
        "die": 4,
        "action_mask": np.array([1, 1, 0]),
    }
    action = agent.select_action(obs)
    assert action == 1

    obs["action_mask"] = np.array([1, 1, 1])
    action = agent.select_action(obs)
    assert action == 2
