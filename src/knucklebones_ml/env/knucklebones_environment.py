"""
PettingZoo environment for Knucklebones dice game.

This module defines the KnucklebonesEnvironment class,
implementing the PettingZoo AECEnv interface.
"""

import functools
from collections import defaultdict
from copy import copy

import gymnasium as gym
import numpy as np
from pettingzoo import AECEnv
from pettingzoo.utils.env import ActionType, ObsType

from . import core_logic as logic


@functools.cache
def _observation_space() -> gym.spaces.Dict:
    return gym.spaces.Dict(
        {
            "observation": gym.spaces.Box(
                low=0, high=6, shape=(2, 3, 3), dtype=np.int8
            ),
            "action_mask": gym.spaces.MultiBinary(3),
        }
    )


@functools.cache
def _action_space() -> gym.spaces.Discrete:
    return gym.spaces.Discrete(3)


class KnucklebonesEnvironment(AECEnv):
    """
    Knucklebones game environment using AEC API.

    This environment implements a two-player Knucklebones game where agents take turns
    playing actions on a 3x3 board. It follows the PettingZoo AECEnv interface for
    multi-agent reinforcement learning.

    """

    metadata = {  # noqa: RUF012
        "name": "knucklebones_environment_v0",
    }

    def __init__(self) -> None:
        self.timestep = None
        self.possible_agents = ["player_0", "player_1"]
        self.seed = None
        self.board = None

    def reset(self, seed: int | None = None, options: dict | None = None) -> None:
        """Reset the environment to the initial state."""
        self.timestep = 0
        self.agents = copy(self.possible_agents)
        self.board = logic.get_board(3, 3)

        self.random_gen = np.random.default_rng(seed)

        self.options = defaultdict(lambda: None, (options or {}))

        observations = {
            "player_0": {
                "observation": (0, self.board.copy()),
                "action_mask": logic.get_valid_actions(self.board),
            },
            "player_1": {
                "observation": (0, self.board.copy()),
                "action_mask": logic.get_valid_actions(self.board),
            },
        }

    def step(self, action: ActionType) -> None:
        pass

    def render(self):
        raise NotImplementedError

    def observation_space(self, agent) -> gym.spaces.Dict:
        return _observation_space()

    def action_space(self, agent) -> gym.spaces.Discrete:
        return _action_space()
