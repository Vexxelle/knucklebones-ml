from typing import Any, Literal


class Agent:
    def __init__(self, seed: int | None = None) -> None:
        pass

    def select_action(self, observation: dict[str, Any]) -> Literal[0, 1, 2]:
        msg = "select_action method must be implemented by Agents"
        raise NotImplementedError(msg)
