import sys
from io import StringIO
from typing import SupportsInt

import numpy as np

import knucklebones_ml as kb
from knucklebones_ml.ui import BasicRenderer

a = np.array([[[0, 6, 3], [0, 6, 3], [0, 2, 3]], [[0, 0, 0], [0, 4, 4], [0, 4, 4]]])


def foo(x: SupportsInt) -> None:
    if x:
        print("x is truthy")


foo(0)
foo(1)
