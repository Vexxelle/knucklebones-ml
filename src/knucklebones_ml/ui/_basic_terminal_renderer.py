from typing import SupportsInt

from knucklebones_ml.ui._base_class import BaseUI


class BasicRenderer(BaseUI):
    """A basic terminal renderer for the Knucklebones game."""

    def __init__(self, players: tuple[str, str], *, flip_board: bool = False) -> None:
        super().__init__(players)
        self.flip_board = flip_board

    def render(self, obs: dict, player: str, last_action: SupportsInt | None) -> None:
        """
        Render the current game state in the terminal.

        Args:
            obs (dict): The observation dictionary containing the current game state.
            player (str): The name of the player currently taking the turn. The UI may
                need this information to un-flip the board.
            last_action (SupportsInt | None): The last action taken by the opponent.

        """
