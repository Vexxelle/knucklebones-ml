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
        side_0_full, side_1_full = True, True
        for row in self.side_0:
            if len(row) < 3:
                side_0_full = False

        for row in self.side_1:
            if len(row) < 3:
                side_1_full = False
        
        return side_0_full or side_1_full
        
    
    def print_board(self) -> None:
        print(f"Player 1 Side ({self.evaluate_score(0)}):" + " "*12 + f"Player 2 Side ({self.evaluate_score(1)}):")
        for i in range(3):
            print("Row " + str(i) + ": ", end="")
            print(str(self.side_0[i]).center(10), end="    ")
            print(str(self.side_1[i]).center(10))
        

    def copy(self, primary_side: Literal[0,1] = 0) -> "Board":
        if primary_side == 0:
            return Board(self.side_0, self.side_1)
        else:
            return Board(self.side_1, self.side_0)
        
class Player:
    def __init__(self, name: str): 
        self.name = name

    def play(self, dice: int, board: Board) -> Literal[0,1,2]:
        return 0

class Human_Player(Player):
    def play(self, dice: int, board: Board) -> Literal[0,1,2]:
        print("\n"*2 + f"{self.name}, it's your turn! You rolled a {dice}.")
        board.print_board()
        while True:
            try:
                row = int(input("Select a row to place your die (0, 1, or 2): "))
                if row not in [0, 1, 2]:
                    print("Invalid row. Please select 0, 1, or 2.")
                    continue
                if len(board.side_0[row]) >= 3:
                    print("That row is full. Please select a different row.")
                    continue
                match row:
                    case 0: return 0
                    case 1: return 1
                    case 2: return 2
                    case _: raise ValueError(f"Player {self.name} selected invalid row. Selected Value: {row}, valid rows: 0,1,2.")
                
            except ValueError:
                print("Invalid input. Please enter a number.")

def play_knucklebones(player0: Player, player1: Player) -> None:
    board = Board()
    turn = randint(0, 1)
    # Game Loop
    while not board.is_full():
        dice = randint(1, 6)
        if turn == 0:
            row = player0.play(dice, board.copy(0))
            board.side_0[row].append(dice)
            turn = 1
        else:
            row = player1.play(dice, board.copy(1))
            board.side_1[row].append(dice)
            turn = 0

    # Game Over



def main():
    print("Hello from knucklebones-ml!")
    p_0 = Human_Player(input("Player 1 Name: "))
    p_1 = Human_Player(input("Player 2 Name: "))
    play_knucklebones(p_0, p_1)


if __name__ == "__main__":
    main()
