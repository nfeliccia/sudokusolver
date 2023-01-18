import itertools
import time
from functools import lru_cache
from typing import Tuple

import numpy as np

import sudoku_utilities as su


@lru_cache(maxsize=3)
def get_index_tuples() -> tuple:
    """
    The purpose of this function is to create the 81 index tuples from (0,0) to (8,8) for addressing the squares.
    It's wrapped in an lru_cache so that we only have to run it once and can refer to memory the rest of the time.
    :return: 81 tuples from (0,0) to (8,8) use for indexing the sudoku board.
    :rtype tuple:
    """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # leverage itertools product instead fo nested for loops.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    index_tuples = tuple(itertools.product(su.index_array, su.index_array))
    return index_tuples


@lru_cache(maxsize=3)
def make_index_tuples() -> Tuple:
    mit = (
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
        (1, 5), (1, 6), (1, 7), (1, 8), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (3, 0),
        (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
        (4, 6), (4, 7), (4, 8), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (6, 0), (6, 1),
        (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),
        (7, 7), (7, 8), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8))
    return mit


mit_collector = list()
for i in range(0, 100):
    trials = 100000
    mit_start = time.perf_counter()
    for i in range(0, trials):
        r = make_index_tuples()
    mit_end = time.perf_counter()
    mit_duration = mit_end - mit_start

    git_start = time.perf_counter()
    for i in range(0, trials):
        r = make_index_tuples()
    git_end = time.perf_counter()
    git_duration = git_end - git_start

    mit_advantage = (git_duration - mit_duration)
    mit_collector.append(mit_advantage)

mit_array = np.array(mit_collector).mean()
print(f"Trials {trials} Making from interpreter read {mit_duration}\tmaking from itertools {git_duration}")
print(f"Mit Advantage {mit_advantage}")
print(f"average advantage {mit_array}")
