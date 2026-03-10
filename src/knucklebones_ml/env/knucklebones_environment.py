"""
PettingZoo environment for Knucklebones dice game.

This module defines the KnucklebonesEnvironment class,
implementing the PettingZoo AECEnv interface.
"""

from __future__ import annotations

from collections import defaultdict
from copy import copy

import numpy as np
from pettingzoo import AECEnv
from pettingzoo.utils import AgentSelector

from . import core_logic as logic


class raw_env(AECEnv):  # noqa: N801
    """
    Knucklebones game environment using AEC API.

    This environment implements a two-player Knucklebones game where agents take turns
    playing actions on a 3x3 board. It follows the PettingZoo AECEnv interface for
    multi-agent reinforcement learning.

    """

    metadata = {  # noqa: RUF012
        "name": "knucklebones_environment_v0",
        "render_modes": ["human", "ascii", "pygame"],  # TODO: Implement rendering modes
    }

    def __init__(self, render_mode: str | None = None) -> None:
        self.possible_agents = ["player_0", "player_1"]
        self.seed = None
        self.render_mode = render_mode

    def reset(self, seed: int | None = None, options: dict | None = None) -> None:
        """
        Reset the environment to the initial state.

        Args:
            seed (int | None): Optional random seed for reproducibility.
            options (dict | None): Optional dictionary of environment
            configuration options. Options can include:
            - "max_steps" (int): Maximum number of steps before the environment
                is truncated. Defaults to None (no truncation).

        """
        self.timestep = 0
        self.random_gen = np.random.default_rng(seed)
        self.options = defaultdict(lambda: None, (options or {}))

        self.die = self.random_gen.integers(1, 7, dtype=np.int16)
        self.board = logic.get_board(3, 3)
        self.previous_die = self.die
        self.previous_board = self.board.copy()

        self.agents = copy(self.possible_agents)

        self.terminations = dict.fromkeys(self.agents, False)
        self.truncations = dict.fromkeys(self.agents, False)

        self.rewards = dict.fromkeys(self.agents, 0)
        self._cumulative_rewards = dict.fromkeys(self.agents, 0)

        self.infos = {key: {} for key in self.agents}

        self._agent_selector = AgentSelector(self.agents)
        self.agent_selection = self._agent_selector.next()

    def render(self):
        pass

    def observation_space(self, agent):
        return self.observation_spaces[agent]

    def action_space(self, agent):
        return self.action_spaces[agent]
