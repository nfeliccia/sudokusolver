nine_range = NineRange.nine_range

ten_range = TenRange.ten_range()[1:]


def valid_column(board_array: np.array = None, valid_check_num: np.uint8 = None, test_point: tuple = None) -> bool:
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Extract the test point row and column from the input tuple
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    test_point_row = test_point[0]
    test_point_column = test_point[1]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Iterate through all possible columns, skipping the one that was just included
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for check_column in nine_range(skip=test_point_column):

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # See if that check column has the value we want to insert in it.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if board_array[test_point_row, check_column] == valid_check_num:
            return False

    return True


def valid_row(board_array: np.array = None, valid_check_num: np.uint8 = None, test_point: tuple = None) -> bool:
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Extract the test point row and column from the input tuple
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    test_point_row = test_point[0]
    test_point_column = test_point[1]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Iterate through all possible columns, skipping the one that was just included
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for check_row in nine_range(skip=test_point_row):

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # See if that check row has the value we want to insert in it.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if board_array[test_point_column, check_row] == valid_check_num:
            return False

    return True


def check_box(board_array: np.array = None, valid_check_num: np.uint8 = None, test_point: tuple = None) -> bool:
    # Check box
    box_x = test_point[1] // 3
    box_y = test_point[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board_array[i][j] == valid_check_num and (i, j) != test_point:
                return False

    return True


def is_a_valid_insertion(board_array: np.array = None, valid_check_num: np.uint8 = None,
                         test_point: tuple = None) -> bool:
    """
    The puprose of this function is to test if a number is a valid insertion into a Sudoku Square

    :param board_array: 9x9 board array of sudoku squares
    :param valid_check_num: a number to check between 1 and 9 to see if entering it violates any of the rules
    :param test_point: location on the board (row,column) where you want to check a number.
    :return:
    """
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Cascade for efficiency, because any one of these is a show stopper
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    is_valid_column = valid_column(board_array=board_array, valid_check_num=valid_check_num, test_point=test_point)
    if is_valid_column:
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Column passed now handle Row
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        is_valid_row = valid_row(board_array=board_array, valid_check_num=valid_check_num, test_point=test_point)
    else:
        return False

    if is_valid_row:
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Column and row passed now handle box
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        is_valid_box = check_box(board_array=board_array, valid_check_num=valid_check_num, test_point=test_point)
    else:
        return False

    if is_valid_box:
        return True
    else:
        return False


def find_empty(bo: np.array) -> tuple | bool:
    """
    The purpose of this functin is to find an empty square.
    :param bo:
    :return:
    """

    for i in nine_range():
        for j in nine_range():
            if bo[i, j] == 0:
                return i, j  # row, col

    return 9, 9


def solve(bo):
    """
    The purpose of this function is to recursively solve a 9x9 sudoku array.
    :param bo: np.array(9x9)
    :return:
    """

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # The first step in solve serves A twofold purpose. One, to find the next empty square, and Two, to determine
    # if we are done iterating.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    next_empty_square = find_empty(bo)
    print(f"Next_empty_square = {next_empty_square}")
    no_next_empty_square = next_empty_square == (9, 9)
    if no_next_empty_square:
        return True
    else:
        row, col = next_empty_square

    # ~~~~~~~~~~~~~~~~~~~~~~~
    # Test all possibilities.
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    for i in ten_range:
        valid_insertion = is_a_valid_insertion(board_array=bo, valid_check_num=i, test_point=(row, col))
        if valid_insertion:
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Load in the puzzle, for dev, I'm keeping them in excel sheets.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
current_dir = Path(os.getcwd())
file_name = r".\puzzle_0003.xlsx"
puzzle_path = current_dir.joinpath(file_name)
puzzle_array = load_puzzle(puzzle_path=puzzle_path)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create a blank sudoku board with all elements necessary
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sudoku_board = SudokuBoard(board_array=puzzle_array)
sudoku_board_b = copy.deepcopy(sudoku_board)
just_the_values = sudoku_board_b.cell_values
print_board(just_the_values)
solve(just_the_values)
