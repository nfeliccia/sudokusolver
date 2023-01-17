from Source.sudoku_board import SudokuBoard


def primary_possibilities_iterator(in_sudoku_board: SudokuBoard = None) -> SudokuBoard:
    """
    The purpose of this function is to go throught he rows and columns of a SudokuBoard object, eliminating
    possibilities based on what else exists in the row/column/parent_square.

    :param in_sudoku_board:
    :return: out_sudoku_board = SudokuBoard object with possible number reduced by elimination.
    """
    round_count = 0
    keep_going = True
    feeling_verbose = False
    while keep_going:
        beginning_unknowns = in_sudoku_board.get_board_wide_unknowns_count()
        beginning_solved_cells = in_sudoku_board.count_known_cells()
        round_count += 1
        print(
            f"Round {round_count}\t beginning_unknown_values {beginning_unknowns} \t known cells {beginning_solved_cells}")

        in_sudoku_board.remove_known_neighbors(verbose=feeling_verbose)
        in_sudoku_board.column_solve(verbose=feeling_verbose)
        in_sudoku_board.row_solve(verbose=feeling_verbose)

        ending_unknowns = in_sudoku_board.get_board_wide_unknowns_count()
        removed_unknowns = beginning_unknowns - ending_unknowns

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Capping the iteration at 6 during development.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if round_count > 6 or not ending_unknowns:
            keep_going = False
        else:
            keep_going = bool(removed_unknowns)

    out_sudoku_board = in_sudoku_board
    return out_sudoku_board


class SudokuCellPossibilitiesEliminator:
    """
    The purpose of this class is to speed up the back tracking algorithm by reducing the number of solution
    of possibilities in each cell by simply applying the logic of no numbers shared between row, column or grid box.
    """

    def __init__(self, in_sudoku_board: SudokuBoard = None):
        self.out_sudoku_board = primary_possibilities_iterator(in_sudoku_board=in_sudoku_board)
