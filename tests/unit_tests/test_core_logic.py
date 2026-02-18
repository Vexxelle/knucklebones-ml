import numpy as np
import pytest

from knucklebones_ml.env import core_logic as logic


def test_get_board():
    board = logic.get_board(3, 3)
    assert board.shape == (2, 3, 3)
    assert np.all(board == 0)


def test_evaluate_column_score(sample_board_mixed):
    assert np.array_equal(
        logic.evaluate_column_scores(sample_board_mixed),
        np.array([[0, 26, 27], [0, 16, 16]]),
    )


def test_evaluate_board_scores(sample_board_mixed):
    assert np.array_equal(
        logic.evaluate_board_scores(sample_board_mixed), np.array([53, 32])
    )


def test_get_valid_actions(sample_board_empty, sample_board_full, sample_board_mixed):
    assert np.array_equal(
        logic.get_valid_actions(sample_board_empty), np.array([[1, 1, 1], [1, 1, 1]])
    )
    assert np.array_equal(
        logic.get_valid_actions(sample_board_full), np.array([[0, 0, 0], [0, 0, 0]])
    )
    assert np.array_equal(
        logic.get_valid_actions(sample_board_mixed), np.array([[1, 0, 0], [1, 1, 1]])
    )


def test_apply_action(sample_board_empty, sample_board_mixed):
    board = logic.apply_action(3, sample_board_empty.copy(), 0, 1)
    assert board[0, 2, 1] == 3  # noqa: PLR2004
    assert np.all(board[1] == 0)

    board = logic.apply_action(3, board, 1, 2)
    board = logic.apply_action(6, board, 0, 2)
    board = logic.apply_action(6, board, 1, 2)

    # fmt: off
    expected_board = np.array([[[0, 0, 0],
                                [0, 0, 0],
                                [0, 3, 0]],
                               [[0, 0, 0],
                                [0, 0, 6],
                                [0, 0, 3]]])
    # fmt: on

    assert np.array_equal(board, expected_board)


def test_apply_action_full_column(sample_board_full):
    with pytest.raises(ValueError):
        logic.apply_action(3, sample_board_full, 1, 1)


def test_board_is_full(sample_board_empty, sample_board_full, sample_board_mixed):
    assert not logic.board_is_full(sample_board_empty)
    assert logic.board_is_full(sample_board_full)
    assert not logic.board_is_full(sample_board_mixed)
