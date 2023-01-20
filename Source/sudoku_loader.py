from copy import copy
from pathlib import Path

import numpy as np
import pandas as pd

from Source.sudoku_utilities import get_index_tuples
from utils import NicPath


def load_puzzle(puzzle_input: NicPath | np.ndarray):
    """
    The purpose of this funciton is to load the puzzle
    :param puzzle_input:
    :return:
    """

    if isinstance(puzzle_input, np.ndarray):
        puzzle_output = copy(puzzle_input)
        return puzzle_output

    # Upgrade a passed path object to a NicPath
    if not isinstance(puzzle_input, NicPath):
        if isinstance(puzzle_input, Path):
            puzzle_input = NicPath(puzzle_input)

    puzzle_output = puzzle_input.read(header=None)
    return puzzle_output


class PuzzleLoader:
    """
    The purpose of this class is to load a puzzle. It can load a puzzle saved as a .xls, .csv, or input as a 9x9 numpy
    array.
    """

    def __init__(self, puzzle_input: NicPath | np.ndarray):
        loaded_puzzle = load_puzzle(puzzle_input)
        verified_puzzle = self.verify_puzzle(input_puzzle=loaded_puzzle)

    def verify_puzzle(self, input_puzzle: np.ndarray | pd.DataFrame = None):
        """
        The purpose of this function is to verify the puzzle is a 9x9 array of integers between 0 and 9.
        n/a are cast to integers.
        :param input_puzzle:
        :return:
        """
        index_tuples = get_index_tuples()

        # Error out on no input
        if input_puzzle is None:
            raise ImportError("No puzzle passed")

        if isinstance(input_puzzle, pd.DataFrame):
            # Eliminate the nan here early if possible.
            output_puzzle = input_puzzle.fillna(value=np.uint8(0)).values
        else:
            output_puzzle = copy(input_puzzle).fillna(value=np.uint8(0))

        # Check that it's a 9x9 array
        row_count = output_puzzle.shape[0]
        column_count = output_puzzle.shape[1]
        if row_count < 9 or column_count < 9:
            raise ImportError("Puzzle too small")

        # If one of the dimensions is greater than 9, iterate through the indicies 0-9.
        if row_count > 9 or column_count > 9:
            trimmed_puzzle = np.zeros((9, 9))
            for index_tuple in index_tuples:
                trimmed_puzzle = output_puzzle[index_tuple]
            output_puzzle = copy(trimmed_puzzle)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Verify that the cells are integers between 0-9
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # See if there are any strings that worked their way in there.
        string_puzzle = copy(output_puzzle).astype(str)
        any_strings = np.char.isalpha(string_puzzle)
        if any_strings.any():
            raise ValueError("Strings in Puzzle")


stringy_puzzle_path = NicPath(r"F:\sudokusolver\puzzles\stringy_puzzle.xlsx")
pl_a = PuzzleLoader(puzzle_input=stringy_puzzle_path)
print("Fin")
