import numpy as np
import pytest
from knucklebones_ml.env import core_logic as logic


def test_manual_game():
    board = logic.get_board(3, 3)
    assert board[0].shape == (3, 3)
    assert board[1].shape == (3, 3)
    assert np.all(board[0] == 0)
    assert np.all(board[1] == 0)

    board = logic.apply_action(3, board, 0, 1)
    assert board[0][2, 1] == 3
    assert np.all(board[1] == 0)

    board = logic.apply_action(3, board, 1, 2)
    board = logic.apply_action(6, board, 0, 2)
    board = logic.apply_action(6, board, 1, 2)

    expected_board = (
        np.array([[0, 0, 0], [0, 0, 0], [0, 3, 0]]),
        np.array([[0, 0, 0], [0, 0, 6], [0, 0, 3]]),
    )
    assert np.array_equal(board[0], expected_board[0])
    assert np.array_equal(board[1], expected_board[1])

    assert logic.evaluate_column_score(board[0][:, 1]) == 3
    assert logic.evaluate_column_score(board[1][:, 2]) == 9

    board = logic.apply_action(3, board, 1, 2)
    with pytest.raises(ValueError):
        logic.apply_action(6, board, 1, 2)
