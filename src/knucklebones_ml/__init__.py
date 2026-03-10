r"""
Knucklebones ML - Machine learning module for dice game \"Knucklebones\".

This package provides a PettingZoo environment with render functionality.
"""

import knucklebones_ml.env.core_logic as logic
from knucklebones_ml.env import env, raw_env

__all__ = ["env", "logic", "raw_env"]
