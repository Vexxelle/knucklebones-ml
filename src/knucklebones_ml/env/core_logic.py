"""
Core logic unit for Knucklebones game.

The core logic unit should be considered the single source of truth
for all game rules and mechanics.

This module contains vectorized numpy functions for:
 - Initializing the game board
 - Determining valid actions, score, and game over status for a given board state
 - Applying a turn action to the board
"""

import numpy as np


def get_board(size_x: int, size_y: int) -> np.ndarray:
    """Initialize a 3D numpy array representing game board with dimensions (2, x, y)."""
    return np.zeros((2, size_x, size_y), dtype=int)


def evaluate_column_scores(board: np.ndarray) -> np.ndarray:
    """
    Calculate the score for each column of each player on the board.

    Scores are computed by summing the contributions from each die value (1-6),
    where each die value contributes (die_value * count^2) to the column score
    and count is the number of dice in that column.

    Returns:
        A 2D numpy array of shape (num_players, num_columns) containing the
        calculated scores for each player's columns.

    """
    scores = np.zeros((2, board.shape[2]), dtype=int)
    for die in range(1, 7):
        column_counts = (board == die).sum(axis=1)
        scores += die * column_counts**2
    return scores


def evaluate_board_scores(board: np.ndarray) -> np.ndarray:
    """
    Calculate the scores for each player based on the current board state.

    Returns:
        A 1D numpy array of length 2 containing the scores for each player.

    """
    scores = np.zeros(2, dtype=int)
    for die in range(1, 7):
        column_counts = (board == die).sum(axis=1)
        scores += (die * column_counts**2).sum(axis=1)
    return scores


def get_valid_actions(board: np.ndarray) -> np.ndarray:
    """
    Determine valid actions for the current board state.

    Returns:
        A 1D numpy array of integers where each index represents a column and the value
        is 1 if the column is a valid action (has empty space), 0 otherwise.

    """
    valid_actions = (board[:, 0, :] == 0).astype(int).tolist()
    return valid_actions


def apply_action(die: int, board: np.ndarray, side: int, action: int) -> np.ndarray:
    """
    Apply a die placement action to the game board.

    Places a die in the specified column of the given side's board at the lowest
    available position. Then removes all enemy dice in the same column that match
    the placed die's value.

    Args:
        die (int): The value of the die being placed.
        board (np.ndarray): A 3D array representing the game board with shape (2, 3, 3)
                           where board[side] is the player's side.
        side (int): The player side (0 or 1) where the die is being placed.
        action (int): The column index (0, 1, or 2) where the die should be placed.

    Returns:
        np.ndarray: The updated game board after the die placement.

    Raises:
        ValueError: If the specified column is completely full and cannot accept
                   the die placement.

    """
    board_side = board[side]
    # Find the lowest empty cell in the specified column
    col = board_side[:, action]
    empty_indices = np.flatnonzero(col == 0)
    try:
        idx = empty_indices[-1]  # Bottom-most zero
        col[idx] = die
    except IndexError as e:
        msg = f"Column {action} is full."
        raise ValueError(msg) from e

    # Delete Enemy Dice
    enemy_side = board[1 - side]
    enemy_col = enemy_side[:, action]
    remaining_dice = enemy_col[(enemy_col != die) & (enemy_col != 0)]
    num_zeros = enemy_col.size - remaining_dice.size

    # Reconstruct the column: Zeros on top, remaining dice on bottom
    enemy_side[:, action] = np.concatenate(
        [np.zeros(num_zeros, dtype=int), remaining_dice],
    )

    return board


def board_is_full(board: np.ndarray) -> bool:
    """Check if either side of the board is full."""
    return bool(np.all(board[0, 0, :] != 0)) or bool(np.all(board[1, 0, :] != 0))
