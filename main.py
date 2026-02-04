from random import randint
from typing import Literal


class Board:
    def __init__(self, side_0: list[list] = [[], [], []], side_1: list[list] = [[], [], []]):
        self.side_0 = side_0
        self.side_1 = side_1

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
        for row in self.side_0:
            if len(row) < 3:
                break
            return True
        for row in self.side_1:
            if len(row) < 3:
                break
            return True
        return False
    
    def print_board(self) -> None:
        print("Player 1 Side:")
        for row in self.side_1:
            print(row)
        print("Player 0 Side:")
        for row in self.side_0:
            print(row)

    def copy(self, primary_side: Literal[0,1] = 0) -> "Board":
        if primary_side == 0:
            return Board(self.side_0, self.side_1)
        else:
            return Board(self.side_1, self.side_0)
        
class Player:
    def __init__(self, name: str): 
        self.name = name

    def play(self, board: Board):
        pass


def play_knucklebones(player0: Player, player1: Player) -> None:
    board = Board()
    turn = randint(0, 1)
    # Game Loop
    while not board.is_full():
        if turn == 0:
            player0.play(board.copy(0))
            turn = 1
        else:
            player1.play(board.copy(1))
            turn = 0

    # Game Over



def main():
    print("Hello from knucklebones-ml!")


if __name__ == "__main__":
    main()
