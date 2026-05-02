from typing import Any, Literal

import numpy as np

from knucklebones_ml.agents._base_class import Agent


class AggressiveAgent(Agent):
    """An agent that always selects the action with the most dice destroyed."""

    def select_action(self, observation: dict[str, Any]) -> Literal[0, 1, 2]:
        """Select the action that destroys the most dice."""
        action_mask = observation["action_mask"]
        die = observation["die"]
        board = observation["board"]

        destroyed_dice = (board[1] == die).sum(axis=1)
        valid_actions = np.where(action_mask == 1)[0]
        best_action = valid_actions[np.argmax(destroyed_dice[valid_actions])]

        return best_action
