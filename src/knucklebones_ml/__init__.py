r"""
Knucklebones ML - Machine learning module for dice game \"Knucklebones\".

This package provides a PettingZoo environment with render functionality,
core game logic and example agents.
"""

from knucklebones_ml import agents, ui
from knucklebones_ml._env import KnucklebonesEnv, env, logic

__all__ = ["KnucklebonesEnv", "agents", "env", "logic", "ui"]
