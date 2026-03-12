from typing import SupportsInt

import numpy as np

from knucklebones_ml._env import core_logic as logic
from knucklebones_ml.ui._base_class import BaseUI


def delimiter(
    delimter_char: str = "-",
    length: int = 40,
    pad_up: int = 1,
    pad_down: int = 1,
    pad_side: int = 2,
) -> str:
    """Generate a delimiter line for terminal output."""
    top = "\n" * pad_up
    line = " " * pad_side + delimter_char * length + " " * pad_side
    bottom = "\n" * pad_down
    return top + line + bottom


def board_to_string(board: np.ndarray) -> str:
    cells = board.flatten().tolist()
    for i, cell in enumerate(cells):
        cells[i] = str(cell) if cell != 0 else " "

    col_scores = logic.evaluate_column_scores(board).flatten().tolist()
    for i, score in enumerate(col_scores):
        col_scores[i] = str(score) if score > 9 else " " + str(score)  # noqa: PLR2004

    index = "  1   2   3  \n"

    # Bottom Top
    board_top = "┌" + 2 * ("─" * 3 + "┬") + "─" * 3 + "┐\n"
    board_top += f"│ {cells[0]} │ {cells[1]} │ {cells[2]} │\n"
    board_top += "├" + 2 * ("─" * 3 + "┼") + "─" * 3 + "┤\n"
    board_top += f"│ {cells[3]} │ {cells[4]} │ {cells[5]} │\n"
    board_top += "├" + 2 * ("─" * 3 + "┼") + "─" * 3 + "┤\n"
    board_top += f"│ {cells[6]} │ {cells[7]} │ {cells[8]} │\n"
    board_top += "┼" + 2 * ("─" * 3 + "┼") + "─" * 3 + "┼\n"

    scores = (
        f" {col_scores[0]}  {col_scores[1]}  {col_scores[2]} \n"
        f" {col_scores[3]}  {col_scores[4]}  {col_scores[5]} \n"
    )

    # Bottom Board
    board_bottom = "┼" + 2 * ("─" * 3 + "┼") + "─" * 3 + "┼\n"
    board_bottom += f"│ {cells[15]} │ {cells[16]} │ {cells[17]} │\n"
    board_bottom += "├" + 2 * ("─" * 3 + "┼") + "─" * 3 + "┤\n"
    board_bottom += f"│ {cells[12]} │ {cells[13]} │ {cells[14]} │\n"
    board_bottom += "├" + 2 * ("─" * 3 + "┼") + "─" * 3 + "┤\n"
    board_bottom += f"│ {cells[9]} │ {cells[10]} │ {cells[11]} │\n"
    board_bottom += "└" + 2 * ("─" * 3 + "┴") + "─" * 3 + "┘\n"

    return index + board_top + scores + board_bottom + index


def player_box_top(player_name: str, board: np.ndarray, die: int | None) -> str:
    total_score = logic.evaluate_board_scores(board).tolist()[0]

    space = 11
    if len(player_name) > space:
        player_name = player_name[: space - 1] + "."

    def center(space: int, text: str) -> str:
        rest = space - len(text)
        l_rest = rest // 2
        r_rest = rest - l_rest
        return l_rest * " " + text + r_rest * " "

    kartste = "╔" + space * "═" + "╗\n"
    kartste += "║" + center(space, player_name) + "║\n"
    kartste += "║" + center(space, str(total_score)) + "║\n"
    kartste += "╬" + space * "═" + "╬\n"
    if die is not None:
        kartste += "║" + center(space, str(die)) + "║\n"
    else:
        kartste += "║" + space * " " + "║\n"
    kartste += "╚" + space * "═" + "╝\n"

    return kartste


def player_box_bottom(player_name: str, board: np.ndarray, die: int | None) -> str:
    total_score = logic.evaluate_board_scores(board).tolist()[1]

    space = 11
    if len(player_name) > space:
        player_name = player_name[: space - 1] + "."

    def center(space: int, text: str) -> str:
        rest = space - len(text)
        l_rest = rest // 2
        r_rest = rest - l_rest
        return l_rest * " " + text + r_rest * " "

    kartste = "╔" + space * "═" + "╗\n"
    if die is not None:
        kartste += "║" + center(space, str(die)) + "║\n"
    else:
        kartste += "║" + space * " " + "║\n"
    kartste += "╬" + space * "═" + "╬\n"
    kartste += "║" + center(space, player_name) + "║\n"
    kartste += "║" + center(space, str(total_score)) + "║\n"
    kartste += "╚" + space * "═" + "╝\n"

    return kartste


def concatenate_elements(
    board_str: str, player_0_str: str, player_1_str: str, pad: int = 2
) -> str:
    p0 = player_0_str.splitlines()
    p1 = player_1_str.splitlines()
    board = board_str.splitlines()

    height_p0 = len(p0)
    width_p0 = len(p0[0])
    height_p1 = len(p1)
    width_p1 = len(p1[0])
    height_board = len(board)
    width_board = len(board[0])

    start_p0 = 1
    start_p1 = height_board - height_p1 - 1
    start_board = 0

    output = ""

    for line in range(height_board):
        if start_p1 <= line < start_p1 + height_p1:
            output += p1[line - start_p1]
        else:
            output += " " * width_p0

        output += " " * pad

        if start_board <= line < start_board + height_board:
            output += board[line - start_board]
        else:
            output += " " * width_board

        output += " " * pad

        if start_p0 <= line < start_p0 + height_p0:
            output += p0[line - start_p0]
        else:
            output += " " * width_p1

        output += "\n"

    return output


class BasicRenderer(BaseUI):
    """A basic terminal renderer for the Knucklebones game."""

    def __init__(self, players: tuple[str, str], *, flip_board: bool = False) -> None:
        super().__init__(players)
        self.flip_board = flip_board
        self.last_die = None

    def render(
        self,
        obs: dict,
        player: str,
        last_action: SupportsInt | None,
        terminated: bool,
        truncated: bool,
    ) -> None:
        """
        Render the current game state in the terminal.

        Args:
            obs (dict): The observation dictionary containing the current game state.
            player (str): The name of the player currently taking the turn. The UI may
                need this information to un-flip the board.
            last_action (SupportsInt | None): The last action taken by the opponent.
            terminated (bool): Whether the game has terminated.
            truncated (bool): Whether the game has been truncated.

        """
        board = obs["board"]
        die = obs["die"]
        if self.flip_board and player == self.players[1]:
            board = np.flipud(board)

        other_player = self.players[1] if player == self.players[0] else self.players[0]

        if last_action:
            print(
                f"{other_player} placed a {self.last_die} on row {int(last_action) + 1}."  # noqa: E501
            )
            print(delimiter())
            if not terminated and not truncated:
                print(f"{player} is up!")

        else:
            print(delimiter("=", pad_up=3))
            print(f"Knucklebones Game Started! {self.players[0]} vs {self.players[1]}")
            print(delimiter("="))
            print(f"{player} goes first! They rolled a {obs['die']}.")

        p0 = player_box_top(
            self.players[0], board, (die if player == self.players[0] else None)
        )
        p1 = player_box_bottom(
            self.players[1], board, (die if player == self.players[1] else None)
        )
        b = board_to_string(board)
        print(concatenate_elements(b, p0, p1))

        if terminated or truncated:
            print(delimiter("="))
            if terminated:
                print("Game Over!".center(40))
            else:
                print("Game Truncated!".center(40))

            scores = logic.evaluate_board_scores(board).tolist()
            if scores[0] > scores[1]:
                print(f"{self.players[0]} wins with {scores[0]} points!")
            elif scores[1] > scores[0]:
                print(f"{self.players[1]} wins with {scores[1]} points!")
            else:
                print(f"It's a tie! Both players have {scores[0]} points!")
            print(delimiter("=", pad_down=3))

        self.last_die = die

    def get_human_action(self, player: str, action_mask: np.ndarray) -> SupportsInt:
        """
        Get an action from the user.

        Returns:
            SupportsInt: The action chosen by the user.

        """
        try:
            position = int(
                input(
                    "Please enter the row number (1-3) where you want to place your die:\n"  # noqa: E501
                )
            )

            min_v, max_v = 1, 3
            if max_v < position or position < min_v or action_mask[position - 1] == 0:
                raise ValueError  # noqa: TRY301

            return position - 1
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")
            return self.get_human_action(player, action_mask)


if __name__ == "__main__":
    board = np.arange(18).clip(0, 6).reshape(2, 3, 3)
    die = 6
    last_action = None
    player_names = ("Gluipi", "Blario")
    flip_board = True
    terminated, truncated = False, False
    obs = {"board": board, "die": die}

    br = BasicRenderer(player_names, flip_board=flip_board)

    br.render(obs, "Gluipi", last_action, terminated, truncated)

    action_mask = np.array([1, 0, 0])
    i = br.get_human_action("Gluipi", action_mask)
    a = logic.apply_action(die, board, 0, i)

    obs = {"board": a, "die": die}
    last_action = i
    terminated = True
    br.render(obs, "Blario", last_action, terminated, truncated)
