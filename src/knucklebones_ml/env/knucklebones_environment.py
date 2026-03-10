"""
PettingZoo environment for Knucklebones dice game.

This module defines the KnucklebonesEnvironment class,
implementing the PettingZoo AECEnv interface.
"""

from __future__ import annotations

from collections import defaultdict
from copy import copy
from functools import cache

import gymnasium as gym
import numpy as np
from pettingzoo import AECEnv
from pettingzoo.utils import AgentSelector, wrappers

from . import core_logic as logic


@cache
def _observation_space() -> gym.spaces.Dict:
    obs_dict: dict[str, gym.spaces.Space] = {
        "die": gym.spaces.Discrete(6, start=1),
        "board": gym.spaces.Box(low=0, high=6, shape=(2, 3, 3), dtype=np.int16),
        "action_mask": gym.spaces.MultiBinary(3),
    }
    return gym.spaces.Dict(obs_dict)


@cache
def _action_space() -> gym.spaces.Discrete:
    return gym.spaces.Discrete(3)


def env(render_mode: str | None = None) -> AECEnv:
    """
    Create a new instance of the Knucklebones environment.

    Args:
        render_mode (str | None): String specifying the rendering mode
            (human, ascii/ansi or pygame) for the environment.
            If not provided, defaults to None (no rendering).

    Returns:
        raw_env: An instance of the Knucklebones environment.

    """
    if render_mode is not None and render_mode not in {
        "human",
        "ascii",
        "ansi",
        "pygame",
    }:
        msg = f"Invalid render_mode: {render_mode}. Must be one of 'human', 'ascii',\
'ansi', 'pygame', or None."
        raise ValueError(msg)

    if render_mode in {"human", "ansi"}:
        render_mode = "ascii"

    env = raw_env(render_mode=render_mode)

    if render_mode == "ascii":
        env = wrappers.CaptureStdoutWrapper(env)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-10)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)

    return env


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

    def observe(self, agent: str) -> dict[str, np.int_ | np.ndarray]:
        """
        Get the observation for the specified agent.

        The observation includes:
        - "die": The current die roll (1-6).
        - "board": The current state of the board, adjusted for the agent's perspective.
        - "action_mask": A binary vector indicating valid actions for
            the current board state.

        """
        adjusted_board = self.board.copy()
        if agent == "player_1":
            adjusted_board = np.flip(adjusted_board, 0)

        return {
            "die": self.die,
            "board": adjusted_board,
            "action_mask": logic.get_valid_actions(adjusted_board)[0],
        }

    def render(self):
        """Render the current state of the environment."""
        if self.render_mode:
            raise NotImplementedError

    def close(self) -> None:
        """Close the environment and release any resources."""

    def observation_space(self, agent: str = "player_0") -> gym.spaces.Dict:  # noqa: ARG002
        """
        Get the observation space for the specified agent.

        In this implementation, the observation space is the same for both
            agents and consists of:
        - "die": A discrete space representing the current die roll (1-6).
        - "board": A 3D box space representing the 3x3 board state for both players.
        - "action_mask": A binary vector indicating valid actions for the
            current board state.
        """
        return _observation_space()

    def action_space(self, agent: str = "player_0") -> gym.spaces.Discrete:  # noqa: ARG002
        """
        Get the action space for the specified agent.

        In this implementation, the action space is the same for both agents and
            consists of three discrete actions:
        - 0: Place the die in the left column.
        - 1: Place the die in the middle column.
        - 2: Place the die in the right column.
        """
        return _action_space()
