"""
This function is the driver for solving a sudoku puzzle.
"""
import time
from pathlib import Path

from stuff_tried_but_not_used.copytech_with_tim_version import timsolver
from stuff_tried_but_not_used.sudoku_board import SudokuBoard

from Source.sudoku_loader import load_puzzle

board_array = load_puzzle(Path(r"F:\sudokusolver\puzzle_0003.xlsx"))
board_create_start = time.perf_counter()
sudoku_board_a = SudokuBoard(board_array=board_array)
board_create_end = time.perf_counter()
board_create_time = board_create_end - board_create_start
"""
my_way_start = time.perf_counter()
my_sudoku_board = SudokuCellPossibilitiesEliminator(in_sudoku_board=sudoku_board_a).out_sudoku_board
my_way_end = time.perf_counter()
my_time = my_way_end - my_way_start
my_sudoku_board.display_board()
"""

tim_way_start = time.perf_counter()
tim_sudoku_baord = timsolver(board=board_array)
tim_way_end = time.perf_counter()
tim_time = tim_way_end - tim_way_start
print(f" Tim Time {tim_time} \t{board_create_time=}")
sudoku_board_b = SudokuBoard(board_array=tim_sudoku_baord)
sudoku_board_b.display_board()
