from typing import Literal, SupportsInt

import numpy as np


class UserInterface:
    """Base class for the user interface of the Knucklebones game."""

    def __init__(self, players: tuple[str, str]) -> None:
        """
        Initialize the user interface.

        Args:
            players (tuple[str, str]): Tuple containing the names of
                "player_0" and "player_1". Names must be unique.

        """
        if players[0] == players[1]:
            msg = "Player names must be unique."
            raise ValueError(msg)
        self.players = players

    def render(
        self,
        obs: dict,
        player: str,
        last_action: SupportsInt | None,
        terminated: bool,
        truncated: bool,
    ) -> None:
        """
        Render the current game state.

        Args:
            obs (dict): The observation dictionary containing the current game state.
            player (str): The name of the player currently taking the turn. The UI may
                need this information to un-flip the board.
            last_action (SupportsInt | None): The last action taken by the opponent.
            terminated (bool): Whether the game has terminated.
            truncated (bool): Whether the game has been truncated.

        """

    def get_human_action(
        self, player: str, action_mask: np.ndarray
    ) -> Literal[0, 1, 2]:
        """
        Get an action from the user.

        Returns:
            Literal[0, 1, 2]: The action chosen by the user.

        """
        msg = "The get_human_action method needs to be implemented by subclasses."
        raise NotImplementedError(msg)

    def close(self) -> None:
        """Close the user interface and release any resources."""
