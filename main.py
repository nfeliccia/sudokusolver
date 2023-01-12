"""
This function is the driver for solving a sudoku puzzle.
"""
import os
from pathlib import Path

import numpy as np

from Source.sudoku_loader import load_puzzle
from Source.sudoku_objects import SudokuBoard

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load in the puzzle, for dev, I'm keeping them in excel sheets.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
current_dir = Path(os.getcwd())
file_name = r".\puzzle_0002.xlsx"
puzzle_path = current_dir.joinpath(file_name)
puzzle_array = load_puzzle(puzzle_path=puzzle_path)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create a blank sudoku board with all elements necessary
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sudoku_board = SudokuBoard(start_board_array=puzzle_array)
board_array = sudoku_board.board
round_count = 0
keep_going = True
feeling_verbose = False
while keep_going:
    round_count += 1
    beginning_unknowns = sudoku_board.get_board_wide_unknowns_count()
    beginning_cells = sudoku_board.count_known_cells()
    print(f"Round {round_count}\t beginning_unknown_values {beginning_unknowns} \t known cells {beginning_cells}")
    sudoku_board.check_if_any_cells_out_of_options()
    sudoku_board.remove_known_neighbors(verbose=feeling_verbose)
    sudoku_board.check_if_any_cells_out_of_options()
    sudoku_board.column_solve(verbose=feeling_verbose)
    sudoku_board.check_if_any_cells_out_of_options()
    sudoku_board.row_solve(verbose=feeling_verbose)
    sudoku_board.check_if_any_cells_out_of_options()
    solved = sudoku_board.count_known_cells()
    ending_unknowns = sudoku_board.get_board_wide_unknowns_count()
    removed_unknowns = beginning_unknowns - ending_unknowns
    print(f"This round removed unknowns {removed_unknowns}")
    if round_count > 6:
        keep_going = False
    else:
        keep_going = bool(removed_unknowns)

print(sudoku_board)

row_seven_ok = sudoku_board.verify_row_solved(row_index=np.uint8(6))

ubc = sudoku_board.get_all_unsolved_board_cells()
ubc_unknowns = [len(x.get_remaining_unknowns()) for x in ubc]
print(f"{ubc}")
