import numpy as np

def get_board_side(size_x: int, size_y: int) -> np.ndarray:
    return np.zeros((size_x, size_y), dtype=int)

def get_board(size_x: int, size_y: int) -> tuple[np.ndarray, np.ndarray]:
    return get_board_side(size_x, size_y), get_board_side(size_x, size_y)

def evaluate_column_score(column: np.ndarray) -> int:
    score = 0
    # Ignore empty cells (zeros) when computing the score
    non_zero_column = column[column != 0]
    unique, counts = np.unique(non_zero_column, return_counts=True)
    for u, c in zip(unique, counts):
        score += u*(c**2)
    return score

def evaluate_side_score(board_side: np.ndarray) -> int:
    # 1. Find all unique dice values on the board at once (excluding 0)
    unique_vals = np.unique(board_side)
    unique_vals = unique_vals[unique_vals != 0]
    
    score = 0
    for val in unique_vals:
        # 2. Create a mask of where this value exists (Matrix of True/False)
        mask = (board_side == val)
        
        # 3. Sum down the rows (axis 0) to get counts per column
        #    Example: [[T, F], [T, T]] -> [2, 1]
        col_counts = mask.sum(axis=0)
        
        # 4. Vectorized scoring: val * count^2
        score += np.sum(val * (col_counts ** 2))
        
    return int(score)

def evaluate_board_score(board: tuple[np.ndarray, np.ndarray]) -> tuple[int, int]:
    player_0_score = evaluate_side_score(board[0])
    player_1_score = evaluate_side_score(board[1])
    return player_0_score, player_1_score

def get_valid_actions(board_side: np.ndarray) -> list[int]:
    valid_actions = (board_side[0, :] == 0).astype(int).tolist()
    return valid_actions

def apply_action(die: int, board: tuple[np.ndarray, np.ndarray], side: int, action: int) -> tuple[np.ndarray, np.ndarray]:
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
    enemy_side = board[1-side]
    enemy_col = enemy_side[:,action]
    remaining_dice = enemy_col[(enemy_col != die) & (enemy_col != 0)]
    num_zeros = enemy_col.size - remaining_dice.size
            
    # Reconstruct the column: Zeros on top, remaining dice on bottom
    enemy_side[:, action] = np.concatenate([
        np.zeros(num_zeros, dtype=int), 
        remaining_dice
    ])

    return board

def board_is_full(board: tuple[np.ndarray, np.ndarray]) -> bool:
    return bool(np.all(board[0] != 0)) or bool(np.all(board[1] != 0))