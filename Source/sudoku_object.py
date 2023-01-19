import typing

import numpy as np

from Source.nic_path import NicPath


class SudokuBoard():

    def __init__(self, sudoku_board_input: typing.Union[np.ndarray, NicPath]):
