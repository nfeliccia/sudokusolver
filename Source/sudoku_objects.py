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
        remaining_unknowns = ','.join([f"{str(x)}" for x in self.get_remaining_unknowns()])
        out_string = f"Row {self.row}, Col {self.column} {remaining_unknowns}"
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
        if isinstance(removal_values, typing.Iterable):
            if self.remaining_unknowns_count() == 0:
                raise ValueError('shtf')
            self.eligible_numbers.eliminate_values(to_eliminate=removal_values)
        elif isinstance(removal_values, int | np.uint8):
            self.eligible_numbers.eliminate_value(to_eliminate=np.uint8(removal_values))

    def has_value_in_eligible(self, test_value: np.uint8 = None):
        hvie = self.eligible_numbers.base_array[test_value]
        return hvie

    def remaining_unknowns_count(self):
        bas = self.eligible_numbers.base_array.sum()
        if bas == 1:
            ruc = 0
        else:
            ruc = bas
        return ruc

    def get_remaining_unknowns(self):
        ruc = self.eligible_numbers.get_values()
        return ruc


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
        for uba_row, uba_column in CoordinatesList.coordinates_list():
            this_sudoku_square = self.board[uba_row, uba_column]

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Check if the input has a value in it for updating.
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            input_board_array_value = external_update_board[uba_row, uba_column]
            if input_board_array_value:
                this_sudoku_square.eligible_numbers.set_value(set_value=input_board_array_value)

    def count_known_cells(self):
        """
        The purpose of this function is to count the number of known cells to determine if iterations are paying off

        :return:
        """
        cl = CoordinatesList.coordinates_list()
        known_count_list = np.array([self.board[ckc_row, ckc_row].answer_found for ckc_row, ckc_column in cl])
        known_counts = known_count_list.sum().astype(np.uint8)
        return known_counts

    def get_board_wide_unkowns_count(self):
        cl = CoordinatesList.coordinates_list()
        gbwuc = np.array([self.board[gbw_row, gbw_column].remaining_unknowns_count() for gbw_row, gbw_column in cl])
        board_wide_unknowns_count = gbwuc.sum()
        return board_wide_unknowns_count

    def remove_known_neighbors(self, verbose=False):
        """
        The purpose of this function is to run all cells on the board and eliminate possible numbers based on other
        values in the square.
        :return:
        """
        print(f"**removing known neighbors**")
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Modify coordinates list to eliminate known cells
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        cl = CoordinatesList.coordinates_list()

        keep_going = True
        while keep_going:
            before_unknowns = self.get_board_wide_unkowns_count()
            if verbose:
                print(f"{before_unknowns=}", end='\t')
            for rkn_row, rkn_column in cl:
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Extract the cell at the iterated position
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                b_cell = self.board[rkn_row, rkn_column]
                if b_cell.answer_found:
                    continue
                b_cnl = b_cell.neighbor_list

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Find coordinates of neighbors with known values.
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                nwkn_coord = [(c_row, c_col) for c_row, c_col in b_cnl if self.board[c_row, c_col].answer_found]

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # neighbor cells known values
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ncwkv = [self.board[c_row, c_col].get_correct_answer_value() for c_row, c_col in nwkn_coord]

                if not ncwkv:
                    continue
                else:
                    b_cell.remove_values(removal_values=ncwkv)

            after_unknowns = self.get_board_wide_unkowns_count()
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

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # The coordinates list of all row, column combinations
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            cl = CoordinatesList.coordinates_list()
            for b_row, b_col in cl:

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Read cell at coordinates and kick out if the answer found status is true.
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                b_cell = self.board[b_row, b_col]
                if b_cell.answer_found:
                    continue

                before_unknowns_count = b_cell.remaining_unknowns_count()
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Get the same row and column from the cell
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                current_board_column = self.board[:, b_col]
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
                current_unknowns = self.get_board_wide_unkowns_count()
                if verbose:
                    print(f"Cell at Row {b_row} and Column {b_col}  removed {unknowns_eliminated_this_cell} "
                          f"known count {known_count} total_removed {total_removed} \t current unknown {current_unknowns}")
                    print(f"Round {round_counter}")

            if known_count == 81 or total_removed == 0:
                keep_going = False

    def row_solve(self, verbose=False):
        """
        The purpose of this function is to analyze rows and columns to solve a sudoku square
        :return:
        """

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

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # The coordinates list of all row, column combinations
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            cl = CoordinatesList.coordinates_list()
            for b_row, b_col in cl:

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Read cell at coordinates and kick out if the answer found status is true.
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                b_cell = self.board[b_row, b_col]
                if b_cell.answer_found:
                    continue

                before_unknowns_count = b_cell.remaining_unknowns_count()
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Get the same row and column from the cell
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                current_board_row = self.board[b_row, :]
                cbr = current_board_row

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Get the known values out of the current rows and columns. Use set logic to find where the remaining
                # unknowns overlap with the known values of the colinear row and column
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                row_knowns = set([x.get_correct_answer_value() for x in cbr if x.answer_found])

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # remove the incremental values from this cell, if any
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                b_cell.remove_values(removal_values=row_knowns)

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Evaluate the results and tally
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                after_unknowns_count = b_cell.remaining_unknowns_count()
                unknowns_eliminated_this_cell = before_unknowns_count - after_unknowns_count
                total_removed += unknowns_eliminated_this_cell
                known_count = self.count_known_cells()
                current_unknowns = self.get_board_wide_unkowns_count()
                if verbose:
                    print(f"Cell at Row {b_row} and Column {b_col}  removed {unknowns_eliminated_this_cell} "
                          f"known count {known_count} total_removed {total_removed} \t current unknown {current_unknowns}")
                    print(f"Round {round_counter}")

            if known_count == 81 or total_removed == 0:
                keep_going = False

    def board_display(self):
        display_string = str()
        for i in nine_range:
            for j in nine_range:
                display_string += f"{self.board[i, j].get_correct_answer_value()} "
            display_string += '\n'
        trailing_text = f"unknowns {self.get_board_wide_unkowns_count()} solved {self.count_known_cells()}\n\n"
        display_string += trailing_text
        return display_string

    def check_out_of_options(self):
        cl = CoordinatesList.coordinates_list()
        out_of_options_list = list()
        for coo_row, coo_col in cl:
            coo_cell = self.board[coo_row, coo_col]
            remaining_options_count = coo_cell.eligible_numbers.base_array.sum()
            if remaining_options_count == 0:
                out_of_options_list.append((coo_row, coo_col))
        if not out_of_options_list:
            print(f"Out of options check ok")
        else:
            print(f"Out of options {copy(out_of_options_list)}")
