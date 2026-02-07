from random import randint, choice
from typing import Literal, cast


class Board:
    def __init__(self, side_0: list[list]|None = None, side_1: list[list]|None = None):
        if side_0: self.side_0 = side_0
        else: self.side_0 = [[], [], []]
        if side_1: self.side_1 = side_1
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

    def play(self, dice: int, board: Board, turn: Literal[0,1]) -> Literal[0,1,2]:
        return 0

class Human_Player(Player):
    def play(self, dice: int, board: Board, turn: Literal[0,1]) -> Literal[0,1,2]:
        
        dice_art = f'''
            -----
            | {dice} |
            -----'''.center(40)
        print("\n"*2 + f"{self.name}, it's your turn! You rolled a:" + dice_art)
        

        board.print_board(turn)
        while True:
            try:
                row = int(input("Select a row to place your dice (1, 2, or 3): "))-1
                if row not in [0, 1, 2]:
                    print("Invalid row. Please select 1, 2, or 3.")
                    continue
                if len(board.side_0[row]) >= 3:
                    print("That row is full. Please select a different row.")
                    continue
                
                return cast(Literal[0,1,2], row)
                
            except ValueError:
                print("Invalid input. Please enter a number.")

class Random_Player(Player):
    def play(self, dice: int, board: Board, turn: Literal[0,1]) -> Literal[0,1,2]:
        valid_rows = [i for i in range(3) if len(board.side_0[i]) < 3]
        return cast(Literal[0,1,2], choice(valid_rows))

class Sequential_Player(Player):
    def play(self, dice: int, board: Board, turn: Literal[0,1]) -> Literal[0,1,2]:
        for i in range(3):
            if len(board.side_0[i]) < 3:
                return cast(Literal[0,1,2], i)
        return 0  # Fallback, should never reach here

class Aggressive_Player(Player):
    def play(self, dice: int, board: Board, turn: Literal[0,1]) -> Literal[0,1,2]:
        # Look for a row to place the dice that would remove the most opponent dice
        best_row = 0
        most_removed = 0
        for i, opponent_row in enumerate(board.side_1):
            if len(board.side_0[i]) < 3:
                if opponent_row.count(dice) > most_removed:
                    best_row = i
                    most_removed = opponent_row.count(dice)
        
        if most_removed == 0:
            # If no dice can be removed, just place in the first available row
            for i in range(3):
                if len(board.side_0[i]) < 3:
                    return cast(Literal[0,1,2], i)
        return cast(Literal[0,1,2], best_row)
    
class Smart_Player(Player):
    def play(self, dice: int, board: Board, turn: Literal[0,1]) -> Literal[0,1,2]:
        def rel_score(board: Board) -> int:
            return board.evaluate_score(0) - board.evaluate_score(1)

        best_row = -1
        best_score = float('-inf')
        for i in range(3):
            temp_board = board.copy(0)
            if not temp_board.place_die(0, i, dice): 
                continue
            if rel_score(temp_board) >= best_score:
                best_row = i
                best_score = rel_score(temp_board)

        return cast(Literal[0,1,2], best_row)
    



def play_knucklebones(player0: Player, player1: Player, ui: bool = False) -> tuple[int, int]:
    # Initialize Game
    if ui:
        print("Welcome to Knucklebones!")
        print(f"Player 1: {player0.name}")
        print(f"Player 2: {player1.name}")
        print("Let's begin!\n")
    board = Board()
    turn = randint(0, 1)

    # Game Loop
    while not board.is_full():
        dice = randint(1, 6)
        if turn == 0:
            row = player0.play(dice, board.copy(0), turn)
            if not board.place_die(0, row, dice):
                raise ValueError(f"Invalid move by {player0.name} on row {row+1} with die {dice}.")
            turn = 1
        else:
            row = player1.play(dice, board.copy(1), turn)
            if not board.place_die(1, row, dice):
                raise ValueError(f"Invalid move by {player1.name} on row {row+1} with die {dice}.")
            turn = 0

    score_0 = board.evaluate_score(0)
    score_1 = board.evaluate_score(1)

    # Game Over
    if ui:
        print("\n\nFinal Board State:")
        board.print_board()

        print("\nGame Over!")
        if score_0 > score_1:
            print(f"{player0.name} wins with a score of {score_0} against {score_1}!")
        elif score_1 > score_0:
            print(f"{player1.name} wins with a score of {score_1} against {score_0}!")
        else:
            print(f"It's a tie! Both players scored {score_0}!")

        print("Thanks for playing!")
    
    return score_0, score_1



def main():
    print("Hello from knucklebones-ml!")
    p_0 = Human_Player(input("Player 1 Name: "))
    if bool(input("Play against a bot? (y/n): ").lower() == 'y'):
        p_1 = Random_Player("Bot")
    else:
        p_1 = Human_Player(input("Player 2 Name: "))
    play_knucklebones(p_0, p_1, ui=True)


if __name__ == "__main__":
    main()
