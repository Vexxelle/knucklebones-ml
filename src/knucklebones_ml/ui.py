from typing import TYPE_CHECKING, Literal
from blessed import Terminal
from random import choice

if TYPE_CHECKING:
    from .core.game import Board, Player


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

class Test_UI(User_Interface):
    def choose_players(self) -> tuple["Player", "Player"]:
        from .core.player import Human_Player
        from .bots import PLAYER_LIST
        
        p1 = Human_Player("Player 1")
        if input("Is Player 2 a human? (y/n): ").lower() == 'y':
            p2 = Human_Player("Player 2")
        else:
            p2 = PLAYER_LIST[choice(list(PLAYER_LIST.keys()))]["constructor"]("Player 2")
        return (p1, p2)

    def display_board(self, board: "Board", flip: bool) -> None:
        pass

    def select_row(self, player: "Player", board: "Board", dice: int) -> Literal[0,1,2]:
        self.display_board(board, flip=False)
        while True:
            try:
                row = int(input(f"{player.name}, select a row (1-3) to place your {dice}: ")) - 1
                if 0 <= row <= 2 and len(board.side_0[row]) < 3:
                    return row  # type: ignore
                else:
                    print("Invalid row. Choose an available row (1-3).")
            except ValueError:
                print("Please enter a number between 1 and 3.")

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