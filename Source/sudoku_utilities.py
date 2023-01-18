import itertools
from functools import lru_cache

import numpy as np

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create array from 1-9 representing the possible numbers in a sudoku square
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
main_nine_array = np.array((1, 2, 3, 4, 5, 6, 7, 8, 9), dtype=np.uint8)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create an array to represent the indices 0-8 ( 9 squares zero based python)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
index_array = np.array((0, 1, 2, 3, 4, 5, 6, 7, 8), dtype=np.uint8)


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
    index_tuples = tuple(itertools.product(index_array, index_array))
    return index_tuples
