import pytest
import numpy as np
from knucklebones_ml.env import core_logic as logic


def test_get_board_side():
    board_side = logic.get_board_side(3, 3)
    assert board_side.shape == (3, 3)
    assert np.all(board_side == 0)


def test_get_board():
    board = logic.get_board(3, 3)
    assert len(board) == 2
    for side in board:
        assert side.shape == (3, 3)
        assert np.all(side == 0)


def test_evaluate_column_score_mixed():
    column = np.array([6, 6, 2])
    assert logic.evaluate_column_score(column) == 26

    column = np.array([3, 3, 3])
    assert logic.evaluate_column_score(column) == 27

    column = np.array([0, 4, 4])
    assert logic.evaluate_column_score(column) == 16


def test_evaluate_column_score_empty():
    column = np.array([0, 0, 0])
    assert logic.evaluate_column_score(column) == 0

    column = np.array([0, 0])
    assert logic.evaluate_column_score(column) == 0


def test_evaluate_column_score_single_value():
    column = np.array([0, 0, 2])
    assert logic.evaluate_column_score(column) == 2

    column = np.array([0, 2])
    assert logic.evaluate_column_score(column) == 2

    column = np.array([0, 0, 0, 5])
    assert logic.evaluate_column_score(column) == 5


def test_evaluate_side_score():
    board_side = np.array([[0, 0, 0], [6, 6, 2], [3, 3, 3]])
    assert logic.evaluate_side_score(board_side) == 23

    board_side = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    assert logic.evaluate_side_score(board_side) == 0

    board_side = np.array([[0, 4], [4, 4], [4, 4]])
    assert logic.evaluate_side_score(board_side) == 52


def test_evaluate_board_score():
    board = (
        np.array([[0, 0, 0], [6, 6, 2], [3, 3, 3]]),
        np.array([[0, 4, 0], [4, 4, 0], [4, 4, 0]]),
    )
    assert logic.evaluate_board_score(board) == (23, 52)

    board = (
        np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
        np.array([[0, 1, 2], [0, 1, 2], [0, 1, 2]]),
    )
    assert logic.evaluate_board_score(board) == (0, 27)


def test_get_valid_actions():
    board_side = np.array([[0, 0, 0], [6, 6, 2], [3, 3, 3]])
    assert logic.get_valid_actions(board_side) == [1, 1, 1]

    board_side = np.array([[0, 4], [4, 4], [4, 4]])
    assert logic.get_valid_actions(board_side) == [1, 0]

    board_side = np.array([[1, 2, 3], [3, 4, 5], [5, 6, 7]])
    assert logic.get_valid_actions(board_side) == [0, 0, 0]


def test_apply_action():
    board = (
        np.array([[0, 0, 0], [6, 6, 2], [3, 3, 3]]),
        np.array([[0, 4, 0], [4, 4, 0], [4, 4, 0]]),
    )
    board = logic.apply_action(4, board, 0, 1)
    expected_board = (
        np.array([[0, 4, 0], [6, 6, 2], [3, 3, 3]]),
        np.array([[0, 0, 0], [4, 0, 0], [4, 0, 0]]),
    )
    assert np.array_equal(board[0], expected_board[0])
    assert np.array_equal(board[1], expected_board[1])

    board = (
        np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
        np.array([[0, 0, 0], [0, 1, 0], [0, 3, 0]]),
    )
    board = logic.apply_action(3, board, 0, 2)
    expected_board = (
        np.array([[0, 0, 0], [0, 0, 0], [0, 0, 3]]),
        np.array([[0, 0, 0], [0, 1, 0], [0, 3, 0]]),
    )
    assert np.array_equal(board[0], expected_board[0])
    assert np.array_equal(board[1], expected_board[1])

    board = (
        np.array([[0, 1, 1], [0, 4, 1], [0, 1, 1]]),
        np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
    )
    board = logic.apply_action(4, board, 1, 1)
    expected_board = (
        np.array([[0, 0, 1], [0, 1, 1], [0, 1, 1]]),
        np.array([[0, 0, 0], [0, 0, 0], [0, 4, 0]]),
    )
    assert np.array_equal(board[0], expected_board[0])
    assert np.array_equal(board[1], expected_board[1])


def test_apply_action_full_column():
    board = (
        np.array([[0, 0, 0], [6, 6, 2], [3, 3, 3]]),
        np.array([[0, 4, 0], [4, 4, 0], [4, 4, 0]]),
    )
    with pytest.raises(ValueError):
        logic.apply_action(5, board, 1, 1)
