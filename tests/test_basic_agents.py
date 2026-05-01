import numpy as np

from knucklebones_ml.agents import ColumnFillAgent, RandomAgent, SequentialAgent


def test_random_agent():
    agent = RandomAgent(seed=42)
    expected_actions = [0, 2, 1, 1, 1, 2, 0, 2, 0]
    obs = {"action_mask": [1, 1, 1]}  # RandomAgent only cares about the action mask
    for i in range(9):
        action = agent.select_action(obs)
        assert action == expected_actions[i]

    agent = RandomAgent(seed=42)
    obs = {"action_mask": [1, 0, 1]}
    for _ in range(12):  # 99% confidence that 1 is never chosen
        action = agent.select_action(obs)
        assert action != 1


def test_column_fill_agent():
    agent = ColumnFillAgent(seed=42)
    assert np.array_equal(agent.column_order, [2, 1, 0])

    obs = {"action_mask": [0, 1, 1]}  # ColumnFillAgent only cares about the action mask
    for _ in range(3):
        action = agent.select_action(obs)
        assert action == 2

    obs = {"action_mask": [1, 1, 0]}
    for _ in range(3):
        action = agent.select_action(obs)
        assert action == 1

    obs = {"action_mask": [1, 0, 0]}
    for _ in range(3):
        action = agent.select_action(obs)
        assert action == 0


def test_sequential_agent():
    agent = SequentialAgent(seed=42)
    assert np.array_equal(agent.column_order, [2, 1, 0])

    obs = {"action_mask": [1, 1, 1]}  # SequentialAgent only cares about the action mask
    for i in range(9):
        action = agent.select_action(obs)
        assert action == [2, 1, 0][i % 3]
