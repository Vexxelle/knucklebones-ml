from typing import Any
from unittest.mock import patch

import numpy as np
from pettingzoo import test

import knucklebones_ml


def test_pettingzoo_api():
    env = knucklebones_ml.env()
    test.api_test(env, verbose_progress=True)


def test_api_step(sample_board_empty):
    env = knucklebones_ml.env()
    env.reset(69)  # Seed chosen to roll a 2 on first two turns
    die_value = 2

    agent_iter = iter(env.agent_iter())
    obs: dict[str, Any] = env.last()[0]  # ty:ignore[invalid-assignment]

    assert obs["die"] == die_value
    assert np.array_equal(obs["board"], sample_board_empty)

    next(agent_iter)

    action = 0
    env.step(action)

    obs: dict[str, Any] = env.last()[0]  # ty:ignore[invalid-assignment]
    assert obs["die"] == die_value
    assert not np.array_equal(obs["board"], sample_board_empty)

    action = 0
    env.step(action)

    obs: dict[str, Any] = env.last()[0]  # ty:ignore[invalid-assignment]

    # fmt: off
    expected_board = np.array([[[0, 0, 0],
                                [0, 0, 0],
                                [0, 0, 0]],
                               [[0, 0, 0],
                                [0, 0, 0],
                                [2, 0, 0]]])
    # fmt: on
    assert np.array_equal(obs["board"], expected_board)


def test_api_render():
    env = knucklebones_ml.env("human")
    env.reset(69)  # Seed chosen to roll a 2 on first turn
    output = env.render()
    expected_output = """Current Agent: player_0
Current Die: 2
Board State:
[[[0 0 0]
  [0 0 0]
  [0 0 0]]

 [[0 0 0]
  [0 0 0]
  [0 0 0]]]
"""
    assert output == expected_output


def test_api_render_no_mode():
    env = knucklebones_ml.env()
    env.reset()
    with patch("gymnasium.logger.warn") as mock_warn:
        env.render()
        mock_warn.assert_called_once_with(
            "You are calling render method without specifying any render mode."
        )


def test_api_truncation():
    env = knucklebones_ml.env()
    options = {"max_steps": 5}
    env.reset(options=options)
    for i in range(4):
        env.step(i % 3)
    truncation = env.last()[3]
    assert not truncation  # truncated flag should be False before 5 steps
    env.step(0)
    truncation = env.last()[3]
    assert truncation  # truncated flag should be True after 5 steps
