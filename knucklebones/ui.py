from typing import TYPE_CHECKING, Literal
from blessed import Terminal

if TYPE_CHECKING:
    from .game import Board, Player


class User_Interface:
    def choose_players(self) -> tuple["Player", "Player"]:
        raise NotImplementedError

    def display_board(self, board: "Board", flip: bool) -> None:
        raise NotImplementedError
    
    def select_row(self, player: "Player", board: "Board", dice: int) -> Literal[0,1,2]:
        raise NotImplementedError

    def show_turn_start(self, player_name: str, dice: int, player_type: Literal["human", "ai"]|None) -> None:
        raise NotImplementedError

    def show_turn_end(self, player_name: str, dice: int, row: int) -> None:
        raise NotImplementedError

    def show_game_end(self, player_1_name: str, player_2_name: str, score_1: int, score_2: int) -> None:
        raise NotImplementedError

# No UI
class No_UI(User_Interface):
    def choose_players(self) -> tuple["Player", "Player"]:
        raise NotImplementedError("No_UI does not support player selection. Please choose players in the main function and pass them to play().")

    def display_board(self, board: "Board", flip: bool) -> None:
        pass

    def show_turn_start(self, player_name: str, dice: int, player_type: Literal["human", "ai"]|None) -> None:
        pass

    def show_turn_end(self, player_name: str, dice: int, row: int) -> None:
        pass

    def show_game_end(self, player_1_name: str, player_2_name: str, score_1: int, score_2: int) -> None:
        pass

class Test_UI(User_Interface):
    def choose_players(self) -> tuple["Player", "Player"]:
        raise NotImplementedError("Test_UI does not support player selection. Please choose players in the main function and pass them to play().")

    def display_board(self, board: "Board", flip: bool) -> None:
        print("Displaying Board:")
        board.print_board(flip)

    def show_turn_start(self, player_name: str, dice: int, player_type: Literal["human", "ai"]|None) -> None:
        print(f"{player_name} is starting their turn with a roll of {dice}.")

    def show_turn_end(self, player_name: str, dice: int, row: int) -> None:
        print(f"{player_name} placed a {dice} on row {row+1}.")

    def show_game_end(self, player_1_name: str, player_2_name: str, score_1: int, score_2: int) -> None:
        print(f"Game Over! {player_1_name} scored {score_1}, while {player_2_name} scored {score_2}.")

# Blessed Terminal-based UI
class CLI(User_Interface):
    def dice_art(self, dice: int) -> str:
        return f'''
            -----
            |   |
            | {dice} |
            |   |
            -----'''

    def __init__(self):
        self.term = Terminal()
        print(self.term.fullscreen())
        print(self.term.clear())

    def choose_players(self) -> tuple["Player", "Player"]:
        raise NotImplementedError

    def display_board(self, board: "Board", flip: bool) -> None:
        pass

    def show_turn_start(self, player_name: str, dice: int, player_type: Literal["human", "ai"]|None) -> None:
        pass

    def show_turn_end(self, player_name: str, dice: int, row: int) -> None:
        pass

    def show_game_end(self, player_1_name: str, player_2_name: str, score_1: int, score_2: int) -> None:
        pass

# Placeholder for GUI display, to be implemented in the future
class GUI(User_Interface):
    def __init__(self):
        pass

    def display_board(self, board: "Board", flip: bool) -> None:
        pass

    def show_turn_start(self, player_name: str, dice: int, player_type: Literal["human", "ai"]|None) -> None:
        pass

    def show_turn_end(self, player_name: str, dice: int, row: int) -> None:
        pass

    def show_game_end(self, player_1_name: str, player_2_name: str, score_1: int, score_2: int) -> None:
        pass