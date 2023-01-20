import itertools
import typing
from copy import deepcopy
from functools import lru_cache
from typing import Tuple

import numpy as np

import sudoku_utilities as su
from utils.nic_path import NicPath


def array_whack_a_number(in_array: np.array = None, number_to_whack: int = 0):
    """
    The purpose of this function is to remove a number from a numpy array, since numpy has no delete by value
    :param in_array: Array from which to remove number passed in as number to whack.
    :param number_to_whack: The number to removed from the in_array
    :return: numpy array with the digit removed.
    """
    aw_filter = in_array == number_to_whack
    out_array = in_array[~aw_filter]
    return out_array


def array_remove_multiple_elements(in_array: np.array = None, numbers_to_whack: typing.Iterable = None) -> typing.Union[
    np.array, np.uint8]:
    """
    The purpose of this function is to remove multiple number from a numpy array, since numpy has no delete by value
    :param in_array: Array from which to remove number passed in as number to whack.
    :param numbers_to_whack: The number to removed from the in_array
    :return: numpy array with the digit removed.
    """

    if isinstance(in_array, np.uint8):
        return in_array
    awal_filter = [x not in numbers_to_whack for x in in_array]
    out_array = in_array[awal_filter]
    if len(out_array) == 1:
        out_array = out_array[0]
    return out_array


def array_set(in_array: np.array = None, number_to_set: int = 0) -> np.uint8:
    as_filter = in_array == number_to_set
    out_integer = in_array[as_filter][0]
    return out_integer


def blank_board() -> np.array:
    """
    The purpose of this function is to simply make a numpy array of 9x9 with a datatype of object.

    :return: Numpy Array 9x9 with 0's.
    :rtype: np.array
    """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Numpy is chosen for its speed over native python.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    bb = np.zeros(shape=(9, 9), dtype=np.uint8)
    return bb


@lru_cache(maxsize=81)
def get_super_box_coordinates(in_cell_address: tuple = None) -> Tuple:
    """
    The purpose of this function is to get the indicies of the squares in the "Super box" That is the box that constrains
    the 9x9 grid.
    :param in_cell_address: Tuple with row and column.
    :return:
    """
    # Check box
    box_neighbor_collector_list = list()
    super_box_index_x = in_cell_address[1] // 3
    super_box_index_y = in_cell_address[0] // 3
    super_box_index_x_start = super_box_index_x * 3
    super_box_index_y_start = super_box_index_y * 3

    for i in np.arange(super_box_index_y_start, super_box_index_y_start + 3):
        for j in np.arange(super_box_index_x_start, super_box_index_x_start + 3):
            box_neighbor = (i, j)
            if box_neighbor != in_cell_address:
                box_neighbor_collector_list.append(box_neighbor)
    box_neighbor_collector_tuple = tuple(box_neighbor_collector_list)
    return box_neighbor_collector_tuple


@lru_cache(maxsize=82)
def get_constraining_neighbor_coordinates_for_a_cell(in_cell_address: tuple = None) -> tuple:
    """
    The purpose of this function is to get the addresses of all cells in the board which impose constraints on the
    value of the cell passed in through in_cell address. which share the same row and same index for a given
    pair of coordinates.

    :param in_cell_address: address tuple of a cell on the sudoku board.
    :return: set of row,column tuples for every cell which imposes constraints on this cell.
    """
    not_me_cols = array_whack_a_number(in_array=su.index_array, number_to_whack=in_cell_address[1])
    row_faux_list = (in_cell_address[0],)
    not_me_col_indices = tuple(itertools.product(row_faux_list, not_me_cols))
    del not_me_cols, row_faux_list

    not_me_rows = array_whack_a_number(in_array=su.index_array, number_to_whack=in_cell_address[0])
    column_faux_list = (in_cell_address[1],)
    not_me_row_indices = tuple(itertools.product(not_me_rows, column_faux_list))
    del not_me_rows, column_faux_list

    super_box_coordinates = get_super_box_coordinates(in_cell_address=in_cell_address)
    all_indicies = (super_box_coordinates, not_me_row_indices, not_me_col_indices)

    not_me_colinear_indicies = tuple(sorted(set(itertools.chain.from_iterable(all_indicies))))
    del not_me_row_indices, not_me_col_indices

    return not_me_colinear_indicies


def update_a_board(in_sudoku_board: np.array = None, in_update_board: np.array = None) -> np.array:
    """
    Update a board passed in as in_sudoku_board, with a board passed in as in_update_board
    :param in_sudoku_board: input board to update
    :param in_update_board: updater board
    :return: sudoku board updated with the unpdate board values.
    """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Decouple from the input board
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    output_board = deepcopy(in_sudoku_board)

    for board_coord in su.get_index_tuples():
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # If the coordinate has a value in the loaded puzzle, assign it to the sudoku board. Else give it an array (1-9)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if in_update_board[board_coord]:
            output_board[board_coord] = in_update_board[board_coord]
        else:
            output_board[board_coord] = np.uint8(0)

    return output_board


def get_coordinates_of_value_cells(in_board: np.array = None) -> Tuple:
    """
    Extract the cells out of the board which are arrays, meaning that they're unsolved at this point.
    :param in_board: np.array representing sudoku board
    :return: tuple of coordinates of array cells.
    :rtype tuple:
    """
    gbcsa = tuple([row_column for row_column in su.get_index_tuples() if in_board[row_column] != 0])
    return gbcsa


def get_coodinates_of_empty_cells(in_board: np.array = None):
    gbcsa = tuple([row_column for row_column in su.get_index_tuples() if in_board[row_column] == 0])
    return gbcsa


def get_coordinates_of_next_empty_cell(in_board: np.array = None) -> tuple | None:
    """
    The purpose of this function is to get the coordinates of the next empty cell in a board.
    :param in_board: 9x9 array repersenting sudoku board
    :return: tuple location of next empty cell, or if no empty cells, None.
    """
    for index_tuple in su.get_index_tuples():
        cell_value = in_board[index_tuple]
        if not cell_value:
            return index_tuple

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # If we loop through all the indices and there's no empties, return none to trigger the code to end.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    return None


def check_insertion_value_is_valid(in_board: np.array, in_coord: tuple, test_num: np.uint8):
    """
    This function determines if an insertion to a cell fits within the constraints of not conflicting with anything
    in the same row, grid, or superbox.

    :param in_board: 9x9 sudoku board
    :param in_coord: row and column at which insertion takes place
    :param test_num: number which is being tested
    :return:
    """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Extract the coordinates of the cell's constraining neighbors
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    this_cell_constraining_neighbors = get_constraining_neighbor_coordinates_for_a_cell(in_cell_address=in_coord)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Extract the values from the known constraining neighbors
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    tcnv = {in_board[nc] for nc in this_cell_constraining_neighbors if in_board[nc] != np.uint8(0)}
    is_valid = test_num not in tcnv
    return is_valid


def check_board_for_violations(in_board: np.array = None):
    """
    The purpose of this function is to check the board for violations where a number violates a constraint.
    :param in_board: 9x9 sudoku board.
    :return: True  if  Violations found.
    """
    cbfv_board = in_board
    value_cells = su.get_index_tuples()
    valid_array = np.array(
        [check_insertion_value_is_valid(in_board=cbfv_board, in_coord=value_cell, test_num=cbfv_board[value_cell]) for
         value_cell in value_cells])
    all_cells_valid = valid_array.all()
    violations = not all_cells_valid
    return violations


def solve_nic(in_board: np.array = None):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # An unsolved value in the board holds an array of possibilities which are derived from the previous section.
    # Therefore, a way to determine if a cell is unsolved is to see the datatype in the cell.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    next_empty_cell = get_coordinates_of_next_empty_cell(in_board=in_board)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # If the board is solved, this will be empty and the solution is complete
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if not next_empty_cell:
        return True

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # If the board is not solved, try working through the solutions of the first unsolved cell
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    else:
        board_coord = next_empty_cell

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Instead of testing numbers 1-10 as in a standard algorithm, we iterate through the values in the cell's array
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for solve_possibiliy in su.main_nine_array:
        civviv = check_insertion_value_is_valid
        this_possibilty_valid = civviv(in_board=in_board, in_coord=board_coord, test_num=solve_possibiliy)
        if this_possibilty_valid:
            in_board[board_coord] = solve_possibiliy
            if solve_nic(in_board=in_board):
                return True
            else:
                in_board[board_coord] = 0
    return False


the_loaded_puzzle = NicPath(r"..\puzzles\puzzle_0008.xlsx").read_excel(load_multiple_sheets=True, header=None)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create a blank board which is a 9x9 grid of arrays from 1-9 signifying all eligible numbers.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sudoku_board_a = the_loaded_puzzle
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Populate the board by reference to the loaded puzzle. Iterate through board coordinates
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sudoku_board_a = update_a_board(in_sudoku_board=sudoku_board_a, in_update_board=the_loaded_puzzle)

initial_volation_check = check_board_for_violations(in_board=sudoku_board_a)
if initial_volation_check:
    raise ValueError
solve_nic(in_board=sudoku_board_a)
out_voard_violations = check_board_for_violations(in_board=sudoku_board_a)
print(f"{out_voard_violations=}")
print("fin")
