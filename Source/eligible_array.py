import typing

import numpy as np


class EligibleNumbers:
    """
    The purpose of this class is to store the eligible numbers for a sudoku square.
    The functions are initialize, retrieve, add, subtract
    """

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Board Values used throughout the class. When using these use copy to get a separate memory reference
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    array_all_true = np.array([0, 1, 1, 1, 1, 1, 1, 1, 1, 1, ], dtype=np.uint8)
    array_all_false = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ], dtype=np.uint8)

    def __init__(self):
        self.base_array = self.array_all_true.copy()

    def get_values(self):
        """
        The purpose of this function is to get the indices of the True values in the array.
        :return:
        """
        values = np.array([x for x in np.arange(0, 10) if self.base_array[x]], dtype=np.uint8)
        return values

    def reset(self) -> np.array:
        """
        The purpose of this function is to assign an all true to the base array.
        Note we use copy to give it a different memory address-otherwise we'd be updating the same object. 
        :return: 
        """
        self.base_array = self.array_all_true.copy()

    def clear(self) -> np.array:
        """
        The purpose of this function is to assign an all False to the base array.
        Note we use copy to give it a different memory address-otherwise we'd be updating the same object. 
        :return: 
        """
        self.base_array = self.array_all_false.copy()

    def set_value(self, set_value: np.uint8 = None):
        """
        The purpose of this function is to set the eligible numbers array to a final value
        :param set_value: np.uint8
        :return: None
        """
        self.clear()
        self.base_array[set_value] = True

    def eliminate_value(self, to_eliminate: np.uint8 = None):
        """
        The purpose of this function is to provide a means to eliminate a value.
        :param to_eliminate:
        :return:
        """

        if self.base_array.sum() == 0:
            raise ValueError('shithitting ')

        self.base_array[to_eliminate] = 0

    def number_of_eligible_values(self):
        noev = len(self.get_values())
        return noev

    def eliminate_values(self, to_eliminate: typing.Iterable = None):
        """
        The purpose of this function is to provide a means to eliminate a value.
        :param to_eliminate:
        :return:
        """
        if self.number_of_eligible_values()==0:
            raise ValueError("SHTF")
        to_eliminate = [np.uint8(x) for x in to_eliminate]
        for x in to_eliminate:
            self.eliminate_value(to_eliminate=x)

    def get_correct_value(self):
        """
        The purpose of this function is to get the correct value, as determined by having an answer found flag be true
        :return:
        """
        if self.answer_found():
            derived_value = self.base_array.argmax().astype(np.uint8)
        else:
            derived_value = 0

        return derived_value

    def answer_found(self):
        """
        The purpose of this function is to determine if an answer has been found. If an answers found there will be only
        one number left, so when you sum the flags for each number they'll add to 1.
        :return:
        """
        bas= self.base_array.sum()
        af = bas == np.uint8(1)
        return af
