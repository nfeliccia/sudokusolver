"""

The purpose of this file is to store utilities used for making mathematical objects needed for sudoku solving.

"""
from functools import lru_cache

import numpy as np

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This value is used several times so lets store it up here as global
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
nine_range = np.arange(0, 9).astype(np.uint8)


@lru_cache(maxsize=3)
def create_parent_square_array():
    """
    The purpose of this function is to create an array which maps each cell to it's parent square.

    :return:
    """
    parent_square_array = np.zeros(shape=(9, 9), dtype=str)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # For something on this scale, tests have shown that a straight reading of numbers in code is faster than any
    # looping
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    parent_square_array[0, 0] = 'a'
    parent_square_array[0, 1] = 'a'
    parent_square_array[0, 2] = 'a'
    parent_square_array[0, 3] = 'b'
    parent_square_array[0, 4] = 'b'
    parent_square_array[0, 5] = 'b'
    parent_square_array[0, 6] = 'c'
    parent_square_array[0, 7] = 'c'
    parent_square_array[0, 8] = 'c'
    parent_square_array[1, 0] = 'a'
    parent_square_array[1, 1] = 'a'
    parent_square_array[1, 2] = 'a'
    parent_square_array[1, 3] = 'b'
    parent_square_array[1, 4] = 'b'
    parent_square_array[1, 5] = 'b'
    parent_square_array[1, 6] = 'c'
    parent_square_array[1, 7] = 'c'
    parent_square_array[1, 8] = 'c'
    parent_square_array[2, 0] = 'a'
    parent_square_array[2, 1] = 'a'
    parent_square_array[2, 2] = 'a'
    parent_square_array[2, 3] = 'b'
    parent_square_array[2, 4] = 'b'
    parent_square_array[2, 5] = 'b'
    parent_square_array[2, 6] = 'c'
    parent_square_array[2, 7] = 'c'
    parent_square_array[2, 8] = 'c'
    parent_square_array[3, 0] = 'd'
    parent_square_array[3, 1] = 'd'
    parent_square_array[3, 2] = 'd'
    parent_square_array[3, 3] = 'e'
    parent_square_array[3, 4] = 'e'
    parent_square_array[3, 5] = 'e'
    parent_square_array[3, 6] = 'f'
    parent_square_array[3, 7] = 'f'
    parent_square_array[3, 8] = 'f'
    parent_square_array[4, 0] = 'd'
    parent_square_array[4, 1] = 'd'
    parent_square_array[4, 2] = 'd'
    parent_square_array[4, 3] = 'e'
    parent_square_array[4, 4] = 'e'
    parent_square_array[4, 5] = 'e'
    parent_square_array[4, 6] = 'f'
    parent_square_array[4, 7] = 'f'
    parent_square_array[4, 8] = 'f'
    parent_square_array[5, 0] = 'd'
    parent_square_array[5, 1] = 'd'
    parent_square_array[5, 2] = 'd'
    parent_square_array[5, 3] = 'e'
    parent_square_array[5, 4] = 'e'
    parent_square_array[5, 5] = 'e'
    parent_square_array[5, 6] = 'f'
    parent_square_array[5, 7] = 'f'
    parent_square_array[5, 8] = 'f'
    parent_square_array[6, 0] = 'g'
    parent_square_array[6, 1] = 'g'
    parent_square_array[6, 2] = 'g'
    parent_square_array[6, 3] = 'h'
    parent_square_array[6, 4] = 'h'
    parent_square_array[6, 5] = 'h'
    parent_square_array[6, 6] = 'i'
    parent_square_array[6, 7] = 'i'
    parent_square_array[6, 8] = 'i'
    parent_square_array[7, 0] = 'g'
    parent_square_array[7, 1] = 'g'
    parent_square_array[7, 2] = 'g'
    parent_square_array[7, 3] = 'h'
    parent_square_array[7, 4] = 'h'
    parent_square_array[7, 5] = 'h'
    parent_square_array[7, 6] = 'i'
    parent_square_array[7, 7] = 'i'
    parent_square_array[7, 8] = 'i'
    parent_square_array[8, 0] = 'g'
    parent_square_array[8, 1] = 'g'
    parent_square_array[8, 2] = 'g'
    parent_square_array[8, 3] = 'h'
    parent_square_array[8, 4] = 'h'
    parent_square_array[8, 5] = 'h'
    parent_square_array[8, 6] = 'i'
    parent_square_array[8, 7] = 'i'
    parent_square_array[8, 8] = 'i'

    return parent_square_array


@lru_cache(maxsize=3)
def create_coordinates_list() -> tuple:
    """
    The purpose of this function is to create a list of the row,column coordinates on the board
    :rtype: tuple
    :return:
    """
    coordinates_list = list()
    for ccl_row in nine_range:
        for ccl_col in nine_range:
            coordinates_list.append((ccl_row, ccl_col))
    coordinates_out = tuple(coordinates_list)
    return coordinates_out


@lru_cache(maxsize=3)
def create_neighbor_list_dictionary():
    """
    The purpose of this function is to create a dictionary where the keys are a tuple of the row and column,
    and the values are a list of all cells with the same parent block (a..i)
    :return:
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
        for neighbor_row in nine_range:
            for neighbor_col in nine_range:
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


class CoordinatesList:
    """
    The purose of this class is to wrap the coordinates list.
    """

    @staticmethod
    def coordinates_list():
        cl = create_coordinates_list()
        return cl


class PatentSquareArray:
    """
    the purpose of this class is to wrap the patent_square array
    """

    @staticmethod
    def patent_square_array():
        psa = create_parent_square_array()
        return psa


class NineRange:
    """
    The purpose fo this class is to wrap the nine range
    """

    @staticmethod
    def nine_range():
        nr = np.arange(0, 9).astype(np.uint8)
        return nr


class NeighborListDictionary:

    @staticmethod
    def neighbor_list_dictionary():
        nld = create_neighbor_list_dictionary()
        return nld
