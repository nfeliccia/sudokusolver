import typing

import numpy as np

from Source.sudoku_loader import PuzzleLoader
from utils.nic_path import NicPath


class SudokuBoard():
    """
    The purpose of this class is to drive the solution of and generate metadata on the analysis of a sudoku board.

    The input can be either a .csv or .xslx/.xls with the puzzle startting at cell (A1) in the upper left corner
    """

    def __init__(self, sudoku_board_input: typing.Union[np.ndarray, NicPath]):
        puzzle_board = PuzzleLoader(puzzle_input=sudoku_board_input)
