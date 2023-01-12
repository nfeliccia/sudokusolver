# This is a sample Python script.
import os
from pathlib import Path

from Source.sudoku_loader import load_puzzle
from Source.sudoku_objects import SudokuBoard
from Source.sudoku_utilities import CoordinatesList

current_dir = Path(os.getcwd())
file_name = r".\puzzle_0002.xlsx"
puzzle_path = current_dir.joinpath(file_name)
puzzle_array = load_puzzle(puzzle_path=puzzle_path)

sudoku_board = SudokuBoard(start_board_array=puzzle_array)
board_array = sudoku_board.board
round_count = 0
keep_going = True
while keep_going:
    beginning_unknowns = sudoku_board.get_board_wide_unkowns_count()
    sudoku_board.check_out_of_options()
    round_count += 1
    sudoku_board.remove_known_neighbors(verbose=True)
    sudoku_board.check_out_of_options()
    sudoku_board.column_solve(verbose=False)
    sudoku_board.check_out_of_options()
    sudoku_board.row_solve(verbose=False)
    sudoku_board.check_out_of_options()
    solved = sudoku_board.count_known_cells()
    ending_unknowns = sudoku_board.get_board_wide_unkowns_count()
    removed_unknowns = beginning_unknowns - ending_unknowns
    print(f"{removed_unknowns}")
    if round_count > 25:
        keep_going = False
    else:
        keep_going = bool(removed_unknowns)

print(sudoku_board)

cl = CoordinatesList.coordinates_list()
for quebra_row, quebra_column in cl:
    quebra_cell = sudoku_board.board[quebra_row, quebra_column]
    qc_ru = quebra_cell.get_remaining_unknowns()
    print(f"{quebra_cell}")

