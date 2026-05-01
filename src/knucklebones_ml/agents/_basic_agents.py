from typing import Any, Literal, cast

import numpy as np
from numpy.random import default_rng

from knucklebones_ml.agents._base_class import Agent


class RandomAgent(Agent):
    """An agent that selects a random legal action each turn."""

    def __init__(self, seed: int | None = None) -> None:
        self.rng = default_rng(seed)

    def select_action(self, observation: dict[str, Any]) -> Literal[0, 1, 2]:
        """Select a random legal action."""
        action_mask = observation["action_mask"]
        actions = np.flatnonzero(action_mask)
        action = self.rng.choice(actions)

        return action


class ColumnFillAgent(Agent):
    """An agent that fills columns in a randomised order."""

    def __init__(self, seed: int | None = None) -> None:
        rng = default_rng(seed)
        self.column_order = rng.permutation(3)

    def select_action(self, observation: dict[str, Any]) -> Literal[0, 1, 2]:
        """Select the first available column in the randomised column fill order."""
        action_mask = observation["action_mask"]
        for i in self.column_order:
            if action_mask[i] == 1:
                return cast("Literal[0, 1, 2]", i)

        msg = "No legal actions available."
        raise ValueError(msg)


class SequentialAgent(Agent):
    """An agent that cycles through columns in a randomised order."""

    def __init__(self, seed: int | None = None) -> None:
        rng = default_rng(seed)
        self.column_order = rng.permutation(3)
        self.next_column = -1

    def select_action(self, observation: dict[str, Any]) -> Literal[0, 1, 2]:
        """Cycle through legal actions in the randomised column order."""
        action_mask = observation["action_mask"]
        while True:
            self.next_column = (self.next_column + 1) % 3
            action = self.column_order[self.next_column]
            if action_mask[action] == 1:
                return cast("Literal[0, 1, 2]", action)
