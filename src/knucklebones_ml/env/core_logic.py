"""
Core logic unit for Knucklebones game. This module contains functions for:
 - Initializing the game board
 - Determining valid actions, score, and game over status for a given board state
 - Applying a turn action to the board
"""

import numpy as np


def get_board(size_x: int, size_y: int) -> np.ndarray:
    return np.zeros((2, size_x, size_y), dtype=int)


def evaluate_column_scores(board: np.ndarray) -> np.ndarray:
    scores = np.zeros((2, board.shape[2]), dtype=int)
    for die in range(1, 7):
        column_counts = (board == die).sum(axis=1)
        scores += die * column_counts**2
    return scores


def evaluate_board_scores(board: np.ndarray) -> np.ndarray:
    scores = np.zeros(2, dtype=int)
    for die in range(1, 7):
        column_counts = (board == die).sum(axis=1)
        scores += (die * column_counts**2).sum(axis=1)
    return scores


def get_valid_actions(
    board: np.ndarray,
) -> list[int]:
    valid_actions = (board[:, 0, :] == 0).astype(int).tolist()
    return valid_actions


def apply_action(die: int, board: np.ndarray, side: int, action: int) -> np.ndarray:
    board_side = board[side]
    # Find the lowest empty cell in the specified column
    col = board_side[:, action]
    empty_indices = np.flatnonzero(col == 0)
    try:
        idx = empty_indices[-1]  # Bottom-most zero
        col[idx] = die
    except IndexError:
        raise ValueError(f"Column {action} is full. Cannot place die.")

    # Delete Enemy Dice
    enemy_side = board[1 - side]
    enemy_col = enemy_side[:, action]
    remaining_dice = enemy_col[(enemy_col != die) & (enemy_col != 0)]
    num_zeros = enemy_col.size - remaining_dice.size

    # Reconstruct the column: Zeros on top, remaining dice on bottom
    enemy_side[:, action] = np.concatenate(
        [np.zeros(num_zeros, dtype=int), remaining_dice]
    )

    return board


def board_is_full(board: np.ndarray) -> bool:
    return bool(np.all(board[0, 0, :] != 0)) or bool(np.all(board[1, 0, :] != 0))
