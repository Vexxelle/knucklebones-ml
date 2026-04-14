from typing import Any, Literal

from numpy.random import default_rng

from knucklebones_ml.agents._base_class import Agent


class RandomAgent(Agent):
    def __init__(self, seed: int | None = None) -> None:
        self.rng = default_rng(seed)

    def select_action(self, observation: dict[str, Any]) -> Literal[0, 1, 2]:

        action_mask = observation["action_mask"]
        actions = action_mask.nonzero()
        action = self.rng.choice(actions)

        return action
