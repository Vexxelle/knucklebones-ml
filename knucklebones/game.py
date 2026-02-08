from random import randint
from typing import Literal, cast
import knucklebones.ui as ui

interface = ui.No_UI()

class Board:
    def __init__(self, side_0: list[list]|None = None, side_1: list[list]|None = None):
        if side_0 is not None: self.side_0 = side_0
        else: self.side_0 = [[], [], []]
        if side_1 is not None: self.side_1 = side_1
        else: self.side_1 = [[], [], []]

    def place_die(self, side: Literal[0,1], row: int, die: int) -> bool:
        if side == 0:
            if len(self.side_0[row]) < 3:
                self.side_0[row].append(die)
                while die in self.side_1[row]:
                    self.side_1[row].remove(die)
                return True
        else:
            if len(self.side_1[row]) < 3:
                self.side_1[row].append(die)
                while die in self.side_0[row]:
                    self.side_0[row].remove(die)
                return True
        return False


    def evaluate_score(self, side: Literal[0,1]) -> int:
        score = 0
        if side == 0:
            eval_side = self.side_0
        else:
            eval_side = self.side_1
        for row in eval_side:
            for die in row:
                score += die*row.count(die)
        return score
    
    def is_full(self) -> bool:
        side_0_full, side_1_full = True, True
        for row in self.side_0:
            if len(row) < 3:
                side_0_full = False

        for row in self.side_1:
            if len(row) < 3:
                side_1_full = False
        
        return side_0_full or side_1_full
        
    
    def print_board(self, flip: bool = False) -> None: 
        if flip:
            print(f"Player 2 Side ({self.evaluate_score(0)}):" + " "*12 + f"Player 1 Side ({self.evaluate_score(1)}):")
        else:
            print(f"Player 1 Side ({self.evaluate_score(0)}):" + " "*12 + f"Player 2 Side ({self.evaluate_score(1)}):")
        
        for i in range(3):
            print("Row " + str(i+1) + ": ", end="")
            print(str(self.side_0[i]).center(10), end="    ")
            print(str(self.side_1[i]).center(10))
        

    def copy(self, primary_side: Literal[0,1] = 0) -> "Board":
        if primary_side == 0:
            side_0_copy = [row.copy() for row in self.side_0]
            side_1_copy = [row.copy() for row in self.side_1]
            return Board(side_0_copy, side_1_copy)
        else:
            side_0_copy = [row.copy() for row in self.side_0]
            side_1_copy = [row.copy() for row in self.side_1]
            return Board(side_1_copy, side_0_copy)

class Player:
    def __init__(self, name: str): 
        self.name = name
        self.type = None
        self.side = None

    def play(self, dice: int, board: Board, turn: Literal[0,1]) -> Literal[0,1,2]:
        return 0
    
class Human_Player(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.type = "human"

    def play(self, dice: int, board: Board, turn: Literal[0,1]) -> Literal[0,1,2]:
        row = interface.select_row(self, board, dice)
        return row

class AI_Player(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.type = "ai"

def play(player0: Player, player1: Player, start_turn: Literal[None, 0, 1] = None) -> tuple[int, int]:
    # Initialize Game
    board = Board()
    turn = start_turn if start_turn is not None else randint(0, 1)

    # Game Loop
    while not board.is_full():
        dice = randint(1, 6)
        if turn == 0:
            interface.show_turn_start(player0.name, dice, player0.type)
            row = player0.play(dice, board.copy(0), turn)
            if not board.place_die(0, row, dice):
                raise ValueError(f"Invalid move by {player0.name} on row {row+1} with die {dice}.")
            turn = 1
        elif turn == 1:
            interface.show_turn_start(player1.name, dice, player1.type)
            row = player1.play(dice, board.copy(1), turn)
            if not board.place_die(1, row, dice):
                raise ValueError(f"Invalid move by {player1.name} on row {row+1} with die {dice}.")
            turn = 0

    score_0 = board.evaluate_score(0)
    score_1 = board.evaluate_score(1)


    
    return score_0, score_1
