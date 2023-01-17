"""

The purpose of this file is to store utilities used for making mathematical objects needed for sudoku solving.

"""
from functools import lru_cache

import numpy as np


class CoordinatesList:
    """
    The purose of this class is to wrap the coordinates list.
    """

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # We use a static method since we dont' need any input. We wrap it in an LRU Cache so it doesn't have to go
    # to the create_coordinates_list() function if its already been done. Bit time saver.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @staticmethod
    @lru_cache(maxsize=2)
    def coordinates_list() -> tuple:
        """
        The purpose of this function is to create a list of the row,column coordinates on the board
        :rtype: tuple
        :return:

        """
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # In limited scale, its faster to generate directly than through a loop
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        coordinates_out = (
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (1, 0), (1, 1), (1, 2), (1, 3),
            (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
            (2, 8), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (4, 0), (4, 1), (4, 2),
            (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),
            (5, 7), (5, 8), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (7, 0), (7, 1),
            (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5),
            (8, 6), (8, 7), (8, 8))

        return coordinates_out


class PatentSquareArray:
    """
    the purpose of this class is to wrap  and deliver the patent_square array
    """

    @staticmethod
    @lru_cache(maxsize=3)
    def patent_square_array():
        """
        The purpose of this function is to create an array which maps each cell to its parent square.
        The sudoku board has nine 3x3 super squares which constrain the numbers 1-9 only being used once in that
        square. I implement this by giving each cell an address of its parent square.

        :return:numpy array of 9 by 9 where each element is the letter of the parent square.
        :rtype:np.array(str)
        """

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # For something on this scale, tests have shown that a straight reading of numbers in code where the value
        # is known is faster than any looping.  This is also wrapped in a lru_cache because the value is static and
        # we don't need to re-invent each time we call.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        parent_square_array = np.zeros(shape=(9, 9), dtype=str)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # I wonder if doing this is  'pythonic' - someone can comment if they think it is or not.
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # a
        parent_square_array[0, 0] = parent_square_array[0, 1] = parent_square_array[0, 2] = 'a'
        parent_square_array[1, 0] = parent_square_array[1, 1] = parent_square_array[1, 2] = 'a'
        parent_square_array[2, 0] = parent_square_array[2, 1] = parent_square_array[2, 2] = 'a'

        # b
        parent_square_array[0, 3] = parent_square_array[0, 4] = parent_square_array[0, 5] = 'b'
        parent_square_array[1, 3] = parent_square_array[1, 4] = parent_square_array[1, 5] = 'b'
        parent_square_array[2, 3] = parent_square_array[2, 4] = parent_square_array[2, 5] = 'b'

        # c
        parent_square_array[0, 6] = parent_square_array[0, 7] = parent_square_array[0, 8] = 'c'
        parent_square_array[1, 6] = parent_square_array[1, 7] = parent_square_array[1, 8] = 'c'
        parent_square_array[2, 6] = parent_square_array[2, 7] = parent_square_array[2, 8] = 'c'

        # d
        parent_square_array[3, 0] = parent_square_array[3, 1] = parent_square_array[3, 2] = 'd'
        parent_square_array[4, 0] = parent_square_array[4, 1] = parent_square_array[4, 2] = 'd'
        parent_square_array[5, 0] = parent_square_array[5, 1] = parent_square_array[5, 2] = 'd'

        # e
        parent_square_array[3, 3] = parent_square_array[3, 4] = parent_square_array[3, 5] = 'e'
        parent_square_array[4, 3] = parent_square_array[4, 4] = parent_square_array[4, 5] = 'e'
        parent_square_array[5, 3] = parent_square_array[5, 4] = parent_square_array[5, 5] = 'e'

        # f
        parent_square_array[3, 6] = parent_square_array[3, 7] = parent_square_array[3, 8] = 'f'
        parent_square_array[4, 6] = parent_square_array[4, 7] = parent_square_array[4, 8] = 'f'
        parent_square_array[5, 6] = parent_square_array[5, 7] = parent_square_array[5, 8] = 'f'

        # g
        parent_square_array[6, 0] = parent_square_array[6, 1] = parent_square_array[6, 2] = 'g'
        parent_square_array[7, 0] = parent_square_array[7, 1] = parent_square_array[7, 2] = 'g'
        parent_square_array[8, 0] = parent_square_array[8, 1] = parent_square_array[8, 2] = 'g'

        # h
        parent_square_array[7, 3] = parent_square_array[7, 4] = parent_square_array[7, 5] = 'h'
        parent_square_array[6, 3] = parent_square_array[6, 4] = parent_square_array[6, 5] = 'h'
        parent_square_array[8, 3] = parent_square_array[8, 4] = parent_square_array[8, 5] = 'h'

        # i
        parent_square_array[6, 6] = parent_square_array[6, 7] = parent_square_array[6, 8] = 'i'
        parent_square_array[7, 6] = parent_square_array[7, 7] = parent_square_array[7, 8] = 'i'
        parent_square_array[8, 6] = parent_square_array[8, 7] = parent_square_array[8, 8] = 'i'

        return parent_square_array


class NineRange:
    """
    The purpose fo this class is to wrap the nine range, and allow a specific number to be skipped in it.
    """

    @staticmethod
    @lru_cache(maxsize=11)
    def nine_range(skip: int = None):
        """
        The purpose of this function is to create a range from 0 to 8 for running the index of the sudoku array.
        It also allows one number to be removed from the array, passed along by the skip parameter.
        :param skip: Number to remove from the array
        :return: np.array(0-8).astype(np.uint8)
        """
        # ~~~~~~~~~~~~~~~~
        # Alias np.uint8
        # ~~~~~~~~~~~~~~~~
        uate = np.uint8

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Check for invalid index to delete
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if skip is not None:
            if skip > 8:
                skip = None

        if skip is None:
            nr = np.array((uate(0), uate(1), uate(2), uate(3), uate(4), uate(5), uate(6), uate(7), uate(8),))
        else:
            nr = NineRange.nine_range(skip=None)
            nr = np.delete(nr, skip)
        return nr


class TenRange:
    """
    The purpose fo this class is to wrap the nine range
    """

    @staticmethod
    @lru_cache(maxsize=3)
    def ten_range():
        uate = np.uint8
        nr = np.array((uate(0), uate(1), uate(2), uate(3), uate(4), uate(5), uate(6), uate(7), uate(8), uate(9)))
        return nr


class NeighborListDictionary:
    """
    The purpose fo this class is to wrap the neighbor list dictionary method.
    """

    @staticmethod
    @lru_cache(maxsize=3)
    def neighbor_list_dictionary() -> dict:
        """
        The purpose of this function is to create a dictionary where the keys are a tuple of the row and column,
        and the values are a list of all cells with the same parent block (a..i)
        :return:dictionary where the keys are a board coordinate and the value is parent block designator
        :rtype:dict
        """

        coordinates_points_list = CoordinatesList.coordinates_list()
        patent_square_array = PatentSquareArray.patent_square_array()
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Create collector list and iterate through the coordinate points list
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        neighbor_list_dict = dict()
        for anltc_row, anltc_col in coordinates_points_list:
            neighbor_collector_list = list()
            serving_cell_letter = patent_square_array[anltc_row, anltc_col]
            nr = NineRange.nine_range()
            for neighbor_row in nr:
                for neighbor_col in nr:
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    # Avoid adding self as neighbor
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    if (neighbor_row == anltc_row) and (neighbor_col == anltc_col):
                        continue

                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    # Get the name of the big block this cell belongs to
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    neighbor_letter = patent_square_array[neighbor_row, neighbor_col]
                    if neighbor_letter == serving_cell_letter:
                        neighbor_collector_list.append((neighbor_row, neighbor_col))

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Store the neighbor list as a tuple for memory efficiency
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            neighbor_list_dict[(anltc_row, anltc_col)] = tuple(neighbor_collector_list)

        return neighbor_list_dict
