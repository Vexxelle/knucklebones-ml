from random import choice
from typing import Literal, cast

from .core.board import Board
from .core.player import AI_Player

PLAYER_LIST = {
    "random": {
        "name": "Random Player",
        "adjective": "Confused",
        "constructor": lambda name: Random_Player(name),
    },
    "sequential": {
        "name": "Sequential Player",
        "adjective": "Methodical",
        "constructor": lambda name: Sequential_Player(name),
    },
    "aggressive": {
        "name": "Aggressive Player",
        "adjective": "Aggressive",
        "constructor": lambda name: Aggressive_Player(name),
    },
    "smart": {
        "name": "Smart Player",
        "adjective": "Smart",
        "constructor": lambda name: Smart_Player(name),
    },
    "stupid": {
        "name": "Stupid Player",
        "adjective": "Slow",
        "constructor": lambda name: Stupid_Player(name),
    },
    "combo": {
        "name": "Combo Player",
        "adjective": "Gambler",
        "constructor": lambda name: Combo_Player(name),
    },
    "pupser": {
        "name": "Der Pupser",
        "adjective": "Stinky",
        "constructor": lambda name: Pupser(name),
    },
}


class Random_Player(AI_Player):
    def play(self, dice: int, board: Board, turn: Literal[0, 1]) -> Literal[0, 1, 2]:
        valid_rows = [i for i in range(3) if len(board.side_0[i]) < 3]
        return cast(Literal[0, 1, 2], choice(valid_rows))


class Sequential_Player(AI_Player):
    def play(self, dice: int, board: Board, turn: Literal[0, 1]) -> Literal[0, 1, 2]:
        for i in range(3):
            if len(board.side_0[i]) < 3:
                return cast(Literal[0, 1, 2], i)
        return 0  # Fallback, should never reach here


class Aggressive_Player(AI_Player):
    def play(self, dice: int, board: Board, turn: Literal[0, 1]) -> Literal[0, 1, 2]:
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
                    return cast(Literal[0, 1, 2], i)
        return cast(Literal[0, 1, 2], best_row)


class Smart_Player(AI_Player):
    def play(self, dice: int, board: Board, turn: Literal[0, 1]) -> Literal[0, 1, 2]:
        def rel_score(board: Board) -> int:
            return board.evaluate_score(0) - board.evaluate_score(1)

        best_row = -1
        best_score = float("-inf")
        for i in range(3):
            temp_board = board.copy(0)
            if not temp_board.place_die(0, i, dice):
                continue
            if rel_score(temp_board) >= best_score:
                best_row = i
                best_score = rel_score(temp_board)

        return cast(Literal[0, 1, 2], best_row)


class Stupid_Player(AI_Player):
    def play(self, dice: int, board: Board, turn: Literal[0, 1]) -> Literal[0, 1, 2]:
        def rel_score(board: Board) -> int:
            return board.evaluate_score(0) - board.evaluate_score(1)

        best_row = -1
        best_score = float("inf")
        for i in range(3):
            temp_board = board.copy(0)
            if not temp_board.place_die(0, i, dice):
                continue
            if rel_score(temp_board) <= best_score:
                best_row = i
                best_score = rel_score(temp_board)

        return cast(Literal[0, 1, 2], best_row)


class Combo_Player(AI_Player):
    def play(self, dice: int, board: Board, turn: Literal[0, 1]) -> Literal[0, 1, 2]:
        legal = -1
        for idx, row in enumerate(board.side_0):
            if len(row) < 3:
                legal = idx
                if dice in row:
                    return cast(Literal[0, 1, 2], idx)

        return cast(Literal[0, 1, 2], legal)


e = 0
s = 0


class Pupser(AI_Player):
    def play(self, dice: int, board: Board, turn: Literal[0, 1]) -> Literal[0, 1, 2]:
        global e, s

        best_delta = float("-inf")
        best_play = -1

        # no special action
        def side_play(dice: int, board: Board):
            big = False
            if dice > 3:
                big = True

            # place big number in safe zone
            if big:
                for idx, row in enumerate(board.side_1):
                    if len(row) == 3:
                        best_play = 1

            # actual random
            for idx, row in enumerate(board.side_0):
                if len(row) < 3:
                    return idx

        # delete
        for idx, erow in enumerate(board.side_1):
            temp_board = board.copy(0)
            if temp_board.place_die(
                0, idx, dice
            ):  # and erow.count(dice) > 0: # maybe remove first cond and make it general
                points = (erow.count(dice)) ** 2 * dice + (
                    board.side_0[idx].count(dice) + 1
                ) ** 2 * dice

                for i in range(1, 6 + 1):
                    if i in board.side_0[idx] and len(board.side_0[idx]) < 3:
                        empty = (
                            9
                            - len(board.side_1[0])
                            + len(board.side_1[1])
                            + len(board.side_1[2])
                            + board.side_1[idx].count(dice)
                        )
                        prob = 0
                        for p in range(empty):
                            prob += 1 / 6 * (5 / 6) ** p

                        # print("checking", i)
                        # print(points, dice)
                        points -= prob * (i * (board.side_0[idx].count(i)) ** 2)
                        # print(board.side_0, board.side_1)
                        # print(empty, prob, points)
                        # print(idx)
                # print()

                if points > best_delta:
                    best_delta = points
                    best_play = idx

        # print("del", best_delta, best_play)

        return cast(Literal[0, 1, 2], best_play)

        # combo
        for idx, row in enumerate(board.side_0):
            if dice in row and len(row) < 3:
                points = (row.count(dice) + 1) ** 2 * dice
                if points > best_delta:
                    best_delta = points
                    best_play = idx
                # return cast(Literal[0,1,2], idx)

        # print("com", best_delta, best_play)

        # else
        if best_play == -1:
            s += 1
            return cast(Literal[0, 1, 2], side_play(dice, board))
        e += 1
        return cast(Literal[0, 1, 2], best_play)
