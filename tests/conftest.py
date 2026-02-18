import numpy as np
from pytest import fixture


@fixture
def sample_board_empty():
    return np.zeros((2, 3, 3), dtype=int)


@fixture
def sample_board_full():
    # fmt: off
    return np.array([  [[1, 2, 3], 
                        [4, 5, 6],
                        [4, 3, 2]],
                       [[6, 5, 4],
                        [3, 2, 1],
                        [5, 5, 5]] ])
    # fmt: on


@fixture
def sample_board_mixed():
    # fmt: off
    return np.array([  [[0, 6, 3],
                        [0, 6, 3], 
                        [0, 2, 3]],
                       [[0, 0, 0],
                        [0, 4, 4],
                        [0, 4, 4]]])
    # fmt: on
