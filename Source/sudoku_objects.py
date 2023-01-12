import typing
from copy import copy

import numpy as np

from Source.eligible_array import EligibleNumbers
from Source.sudoku_utilities import CoordinatesList, PatentSquareArray, NineRange, NeighborListDictionary

nine_range = NineRange.nine_range()


def assign_parent_square(p_row: np.uint8 = None, p_column: np.uint8 = None) -> str:
    """
    The purpose of this function is to take a row, column and find which of the 9 big "Parent Squares" that it belongs
    to and assign it that value
    :rtype: str
    :param p_row: Sudoko board row
    :dtype p_row: np.uint8
    :param p_column: Sudoku board column.
    :return:
    """
    parent_square_master_df = PatentSquareArray.patent_square_array()
    parent_square_master_value = parent_square_master_df[p_row, p_column]
    return parent_square_master_value


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


class SudokuCell:
    """
    This is the class for a single square of a sudoku board.
    """

    def __repr__(self):
        out_string = f"Row {self.row}, Col {self.column}"
        return out_string

    def __init__(self, sudoku_cell_row: np.uint8 = None, sudoku_cell_column: np.uint8 = None):

        # CHeck that the inputs are np.uint8
        if not isinstance(sudoku_cell_row, np.uint8) or not isinstance(sudoku_cell_column, np.uint8):
            raise TypeError("Sudoku Cell addreses are np.uint8")

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Each cell has a list of eligible numbers that it can hold. THe purpose of the solving algorithms is to
        # reduce this list down to one number thus solving the square
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.eligible_numbers = EligibleNumbers()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Since rules of sudoku limit repetition in a specific 3x3 square, we divide the board for analysis sake into
        # 9 such of these 3x3 squares labeled a through i
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.parent_square = assign_parent_square(p_row=sudoku_cell_row, p_column=sudoku_cell_column)

        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # Find the neighbor cell
        # ~~~~~~~~~~~~~~~~~~~~~~~~

        neighbor_list_dictionary = NeighborListDictionary.neighbor_list_dictionary()
        self.neighbor_list = neighbor_list_dictionary.get((sudoku_cell_row, sudoku_cell_column))
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Track the row and column  as  cell properties.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.row = sudoku_cell_row
        self.column = sudoku_cell_column

    @property
    def answer_found(self):
        af = self.eligible_numbers.answer_found()
        return af

    def get_correct_answer_value(self):
        """
        The purpose of this function is to get the number which is the correct answer by looking at the underlyin
        numbers array.
        :return:
        """
        final_number = self.eligible_numbers.get_correct_value()
        return final_number

    def remove_values(self, removal_values: int | typing.Iterable):
        """
        The purpose of this function is to remove values from the list of eligible numbers in the cell which
        is used for solving.
        :param removal_values:
        :return:
        """

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Handle instance of iterable. Set up function to handle iterable or integer
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if isinstance(removal_values, typing.Iterable):

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Do the checking if the input value is an empty iterable here rather than further up in the code
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if not removal_values:
                return False

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # If the remaining unknowns are 0 we've got a condition we shouldn't have  so raised an error
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if self.remaining_unknowns_count() == 0:
                raise ValueError('shtf')

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Call the eligible numbers class eliminate numbers
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            self.eligible_numbers.eliminate_values(to_eliminate=removal_values)
        elif isinstance(removal_values, int | np.uint8):
            self.eligible_numbers.eliminate_value(to_eliminate=np.uint8(removal_values))

    def has_value_in_eligible(self, test_value: np.uint8 = None):
        hvie = self.eligible_numbers.base_array[test_value]
        return hvie

    def remaining_unknowns_count(self):
        """
        The purpose of this function is to count up the number of remaining unknowns, regardless of what they are.
        :return:
        """
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # If there's only one unknown, then it's really not an unknown, it's a known, so we return there are 0 unknown
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        bas = self.eligible_numbers.base_array.sum()
        if bas == 1:
            ruc = 0
        else:
            ruc = bas

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Cast to numpy int 8 on the way out.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ruc = np.uint8(ruc)
        return ruc

    def get_remaining_unknowns(self):
        ruc = self.eligible_numbers.get_values()
        return ruc

    def cell_out_of_options(self) -> bool:
        """
        The purpose of this function is to determine if a cell is out of options, which is a bad condition we
        really don't want.
        :return: True if the cell is out of options.
        :rtype: bool
        """
        enbas = self.eligible_numbers.base_array.sum()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # return True if the sum is zero.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        cooo = not bool(enbas)
        return cooo


class SudokuBoard:
    """
    This is the class to hold a sudoku board of 9x9 squares. Each square holds an object called a SudokuCell.
    """

    def __repr__(self):
        ds = self.board_display()
        return ds

    def __init__(self, start_board_array=None):
        self.board = create_initial_board()
        self.update_board_array(external_update_board=start_board_array)

    def update_board_array(self, external_update_board: np.array = None):
        """
        The purpose of this function is to update the board array with the value read from an excel sheet.
        Note empty values are represented by 0, which is never an acceptable value for the array to be true.
        :param external_update_board: numpy array which holds the SudokuCell objects.  
        :return: 
        """
        all_board_cells = self.get_all_board_cells()
        for board_cell in all_board_cells:
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Check if the input has a value in it for updating.
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            input_board_array_value = external_update_board[board_cell.row, board_cell.column]
            if input_board_array_value:
                board_cell.eligible_numbers.set_value(set_value=input_board_array_value)

    def get_all_board_cells(self):
        """
        The purpose of this function is to return a list of all cell objects on the board.
        :return: Tuple of board cells
        :rtype: tuple
        """
        cl = CoordinatesList.coordinates_list()
        all_board_cells = tuple([self.board[ckc_row, ckc_column] for ckc_row, ckc_column in cl])
        return all_board_cells

    def get_all_unsolved_board_cells(self):
        """
        The purpose of this function is to return a list of all cell objects on the board which do *not* yet have a
        solution.
        :return: Tuple of board cells
        :rtype: tuple
        """

        all_board_cells = self.get_all_board_cells()
        all_unsolved_board_cells = [x for x in all_board_cells if not x.answer_found]
        return all_unsolved_board_cells

    def count_known_cells(self):
        """
        The purpose of this function is to count the number of known cells to determine if iterations are paying off

        :return: Number of known cells on the sudoku board
        :rtype:np.uint8
        """
        abc = self.get_all_board_cells()
        known_count_list = np.array([x.answer_found for x in abc])
        known_counts = known_count_list.sum().astype(np.uint8)
        return known_counts

    def get_board_wide_unknowns_count(self, verbose=False):
        """
        The purpose of this function is to count the number of total unknown values across all cells.
        This is an important value to determine progress being made
        :return: Board wide count of unknowns
        :rtype: np.uint16
        """
        bc = self.get_all_board_cells()
        board_wide_unknowns_count = np.array([x.remaining_unknowns_count() for x in bc]).sum().astype(np.uint16)
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

    def board_display(self):
        display_string = str()
        for i in nine_range:
            for j in nine_range:
                display_string += f"{self.board[i, j].get_correct_answer_value()} "
            display_string += '\n'
        trailing_text = f"unknowns {self.get_board_wide_unknowns_count()} solved {self.count_known_cells()}\n\n"
        display_string += trailing_text
        return display_string

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
