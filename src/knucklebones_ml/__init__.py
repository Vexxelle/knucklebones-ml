r"""
Knucklebones ML - Machine learning module for dice game \"Knucklebones\".

This package provides a PettingZoo environment with render functionality,
core game logic and example agents.
"""

from knucklebones_ml import bots, ui
from knucklebones_ml._env import env, logic, raw_env

__all__ = ["bots", "env", "logic", "raw_env", "ui"]
