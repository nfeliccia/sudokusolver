from copy import copy

import numpy as np

from Source.sudoku_objects import SudokuCell
from Source.sudoku_utilities import NineRange, CoordinatesList

nine_range = NineRange.nine_range()


def create_initial_board():
    """
    The purpose of this function is to create a blank board, and populate it with Sudoku cell objects.
    :return: Board Array - 9 x 9 array of blank SudokuCell Objects.
    """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Create initial 9x9 square array.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    board_array = np.array(np.zeros(shape=(9, 9), dtype=object))
    for cib_row in nine_range:
        for cib_col in nine_range:
            board_array[cib_row, cib_col] = SudokuCell(sudoku_cell_row=cib_row, sudoku_cell_column=cib_col)
    return board_array


class SudokuBoard:
    """
    This is the class to hold a sudoku board of 9x9 squares. Each square holds an object called a SudokuCell.
    """

    def __repr__(self):
        ds = self.display_board()
        return ds

    def __init__(self, board_array=None):
        self.board = create_initial_board()
        self.update_board_array(external_update_board=board_array)

    def update_board_array(self, external_update_board: np.array = None):
        """
        The purpose of this function is to update the board array with the value read from an excel sheet.
        Note empty values are represented by 0, which is never an acceptable value for the array to be true.
        :param external_update_board: numpy array which holds the SudokuCell objects.
        :return:
        """
        current_board_cells = self.get_all_board_cells()
        for board_cell in current_board_cells:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Check if the input has a value in it for updating.
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            new_board_array_value = external_update_board[board_cell.row, board_cell.column]
            if new_board_array_value:
                board_cell.eligible_numbers.set_value(set_value=new_board_array_value)

    def get_all_board_cells(self):
        """
        The purpose of this function is to return a list of all cell objects on the board.
        :return: Tuple of board cells
        :rtype: tuple
        """
        cl = CoordinatesList.coordinates_list()
        all_board_cells = tuple([self.board[ckc_row, ckc_column] for ckc_row, ckc_column in cl])
        return all_board_cells

    def get_all_unsolved_board_cells(self) -> tuple:
        """
        The purpose of this function is to return a list of all cell objects on the board which do *not* yet have a
        solution.
        :return: Tuple of board cells
        :rtype: tuple
        """

        all_board_cells = self.get_all_board_cells()
        all_unsolved_board_cells = tuple(x for x in all_board_cells if not x.answer_found)
        return all_unsolved_board_cells

    def count_known_cells(self):
        """
        The purpose of this function is to count the number of known cells to determine if iterations are paying off

        :return: Number of known cells on the sudoku board
        :rtype:np.uint8
        """
        all_board_cells = self.get_all_board_cells()
        known_count_list = np.array([x.answer_found for x in all_board_cells])
        known_counts = known_count_list.sum().astype(np.uint8)
        return known_counts

    def get_board_wide_unknowns_count(self, verbose=False):
        """
        The purpose of this function is to count the number of total unknown values across all cells.
        This is an important value to determine progress being made
        :return: Board wide count of unknowns
        :rtype: np.uint16
        """
        all_board_cells = self.get_all_board_cells()
        abc = all_board_cells
        board_wide_unknowns_count = np.array([x.remaining_unknowns_count() for x in abc]).sum().astype(np.uint16)
        if verbose:
            print(f"board_wide_unknonws_count={board_wide_unknowns_count}")
        return board_wide_unknowns_count

    def single_pass_of_known_neighbors(self):
        """
        The purpose of this function is to pass once through all cells and modify them based on the rules that
        parent square can have only values 1-9
        :return:
        """
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Iterate through each of the unsolved cells and modify based on neighbors.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for b_cell in self.get_all_unsolved_board_cells():
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Get neighbor cells based on coordinates, extract the known values into a tuple and pass to the cell
            # remove method.
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            b_cell_neighbor_cells = tuple(self.board[n_row, n_column] for n_row, n_column in b_cell.neighbor_list)
            cvfn = tuple(x.get_correct_answer_value() for x in b_cell_neighbor_cells if x.answer_found)
            correct_values_from_neighbor_cells = cvfn
            b_cell.remove_values(removal_values=correct_values_from_neighbor_cells)

    def remove_known_neighbors(self, verbose=False):
        """
        The purpose of this function is to run all cells on the board and eliminate possible numbers based on other
        values in the square.
        :return:
        """
        print(f"**removing known neighbors**")

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Loop and call the single pass of known neighbors until the improvement is zero.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        keep_going = True
        while keep_going:
            before_unknowns = self.get_board_wide_unknowns_count()
            self.single_pass_of_known_neighbors()
            after_unknowns = self.get_board_wide_unknowns_count()
            known_improvement = before_unknowns - after_unknowns
            if verbose:
                print(f"{after_unknowns=}\t{known_improvement=}")
            keep_going = bool(known_improvement)

        return True

    def column_solve(self, verbose=False):
        """
        The purpose of this function is to analyze rows and columns to solve a sudoku square
        :return:
        """
        print(f"Column Solve")
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Set the while loop controls and a round counter.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        keep_going = True
        round_counter = 0

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # While loop to keep iterating rows and columns while additional information is gathered.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        while keep_going:
            total_removed = 0
            round_counter += 1
            known_count = self.count_known_cells()

            for b_cell in self.get_all_unsolved_board_cells():

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Benchmark how many unknowns there are in this cell
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                before_unknowns_count = b_cell.remaining_unknowns_count()

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Get all the cells in the column
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                current_board_column = self.board[:, b_cell.column]
                cbc = current_board_column

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Get the known values out of the current rows and columns. Use set logic to find where the remaining
                # unknowns overlap with the known values of the colinear row and column
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                column_row_knowns = set([x.get_correct_answer_value() for x in cbc if x.answer_found])

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # remove the incremental values from this cell, if any
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                b_cell.remove_values(removal_values=column_row_knowns)

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Evaluate the results and tally
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                after_unknowns_count = b_cell.remaining_unknowns_count()
                unknowns_eliminated_this_cell = before_unknowns_count - after_unknowns_count
                total_removed += unknowns_eliminated_this_cell
                known_count = self.count_known_cells()
                current_unknowns = self.get_board_wide_unknowns_count()
                if verbose:
                    print(f"Cell at Row {b_cell.row} and Column {b_cell.column} "
                          f"removed {unknowns_eliminated_this_cell} "
                          f"known count {known_count} total_removed {total_removed} \t"
                          f" current unknown {current_unknowns}")
                    print(f"Round {round_counter}")

            if known_count == 81 or total_removed == 0:
                keep_going = False

    def row_solve(self, verbose=False):
        """
        The purpose of this function is to analyze rows and columns to solve a sudoku square
        :return:
        """
        print(f"Row Solve")
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Set the while loop controls and a round counter.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        keep_going = True
        round_counter = 0

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # While loop to keep iterating rows and columns while additional information is gathered.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        while keep_going:
            total_removed = 0
            round_counter += 1
            known_count = self.count_known_cells()

            for b_cell in self.get_all_unsolved_board_cells():

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Benchmark how many unknowns there are in this cell
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                before_unknowns_count = b_cell.remaining_unknowns_count()

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Get all the cells in the column
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                current_board_row = self.board[b_cell.row, :]
                cbr = current_board_row

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Get the known values out of the current rows and columns. Use set logic to find where the remaining
                # unknowns overlap with the known values of the colinear row and column
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                column_row_knowns = set([x.get_correct_answer_value() for x in cbr if x.answer_found])

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # remove the incremental values from this cell, if any
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                b_cell.remove_values(removal_values=column_row_knowns)

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Evaluate the results and tally
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                after_unknowns_count = b_cell.remaining_unknowns_count()
                unknowns_eliminated_this_cell = before_unknowns_count - after_unknowns_count
                total_removed += unknowns_eliminated_this_cell
                known_count = self.count_known_cells()
                current_unknowns = self.get_board_wide_unknowns_count()
                if verbose:
                    print(f"Cell at Row {b_cell.row} and Column {b_cell.column} "
                          f"removed {unknowns_eliminated_this_cell} "
                          f"known count {known_count} total_removed {total_removed} \t"
                          f" current unknown {current_unknowns}")
                    print(f"Round {round_counter}")

            if known_count == 81 or total_removed == 0:
                keep_going = False

    def display_board(self):
        """
        The source algorithm came from here. Thanks
        https://www.techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
        :return:
        """
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Iterate through the cells and get their value. Include pretty print.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for i in nine_range:
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - - ")

            for j in nine_range:
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Call the correct answer and string it.
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                this_sudoku_cell_correct_answer_value = str(self.board[i, j].get_correct_answer_value())
                cav = f"{this_sudoku_cell_correct_answer_value} "
                cav_end = f"{this_sudoku_cell_correct_answer_value}\n"

                if j == 8:
                    print(cav_end, end="")
                else:
                    print(cav, end="")

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Add trailing text about the

        trailing_text = f"unknowns {self.get_board_wide_unknowns_count()} solved {self.count_known_cells()}\n\n"
        print(f"*************************\n{trailing_text}")

    def check_if_any_cells_out_of_options(self, verbose=False):
        """
        The purpose of this function is to report if a cell has all the eligible numbers removed.
        This is an error condition and should not happen.
        :return:
        """
        all_board_cells = self.get_all_board_cells()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Use list comprehension because it is faster here.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        out_of_options_list = [(x.row, x.column) for x in all_board_cells if x.cell_out_of_options()]
        if not out_of_options_list and verbose:
            print(f"Out of options check ok")
            return False
        elif verbose:
            print(f"Out of options {copy(out_of_options_list)}")
            return True
        elif out_of_options_list:
            raise ValueError("Out of options")

    def verify_row_solved(self, row_index: np.uint8 = None) -> bool:

        row_index = np.uint8(row_index)
        row_values = self.board[row_index, :]
        set_of_correct_values = set(x.get_correct_answer_value() for x in row_values)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # THe length should be 9 if all distinct numbers are used, and so should the set if the duplicates are dropped
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        row_solved = len(set_of_correct_values) == 9
        return row_solved

    def find_empty(self) -> tuple | None:
        """
        https://www.techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
        :return:
            (tuple|none): Tuple of coordinates if an empty cell is found. None if no empty cell is found.
        """

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Use already constructed coordinates list.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        all_board_cells = self.get_all_unsolved_board_cells()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Iterate through rows and columns until a 0 is found
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for board_cell in all_board_cells:
            carac = board_cell.get_correct_answer_value()
            if not carac:
                return board_cell.row, board_cell.column

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # If iterate all the way through and no zeroes found, return none.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        return None

    @property
    def cell_values(self):
        blank_nine_by_nine = np.zeros((9, 9), dtype=np.uint8)
        for board_cell in self.get_all_board_cells():
            blank_nine_by_nine[board_cell.row, board_cell.column] = board_cell.get_correct_answer_value()

        filled_in_nine_by_nine = blank_nine_by_nine.copy()
        return filled_in_nine_by_nine
