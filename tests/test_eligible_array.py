import numpy as np

from stuff_tried_but_not_used.eligible_array import EligibleNumbers


def test_eligible_numbers_initialization():
    """
    The purpose of this function is to test the initialization makes the correct array.
    :return:
    """
    en_a = EligibleNumbers()
    en_a_values = en_a.base_array
    correct_answer = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1]).astype(np.uint8)
    correct_checker = all((en_a_values[i] == correct_answer[i] for i in range(0, 10)))
    assert correct_checker is True


def test_eligible_numbers_get_values():
    """
    The purpose of this function is to test the get values
    :return:
    """
    en_a = EligibleNumbers()
    en_a_values = en_a.get_values()
    correct_answer = np.array([0, 2, 3, 4, 5, 6, 7, 8, 9]).astype(np.uint8)
    correct_checker = all((en_a_values[i] == j for i, j in enumerate(correct_answer)))
    assert correct_checker is True


def test_eligible_numbers_reset():
    """
    The purpose of this function is to test the get values
    :return:
    """
    en_a = EligibleNumbers()
    en_a.reset()
    en_a_values = en_a.base_array
    correct_answer = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1]).astype(np.uint8)
    correct_checker = all((en_a_values[i] == correct_answer[i] for i in range(0, 10)))
    assert correct_checker is True


def test_eligible_numbers_clear():
    """
    The purpose of this function is to test the get values
    :return:
    """
    en_a = EligibleNumbers()
    en_a.clear()
    en_a_values = en_a.base_array
    correct_answer = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).astype(np.uint8)
    correct_checker = all((en_a_values[i] == correct_answer[i] for i in range(0, 10)))
    assert correct_checker is True


def test_eligible_numbers_set_value():
    """
    The purpose of this function is to test the get values
    :return:
    """
    en_a = EligibleNumbers()
    en_a.clear()
    en_a.set_value(set_value=np.uint8(3))
    en_a_values = en_a.base_array
    correct_answer = np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0]).astype(np.uint8)
    correct_checker = all((en_a_values[i] == correct_answer[i] for i in range(0, 10)))
    assert correct_checker is True


def test_eligible_numbers_eliminate_value():
    """
    The purpose of this function is to test the get values
    :return:
    """
    en_a = EligibleNumbers()
    en_a.clear()
    en_a.eliminate_value(to_eliminate=np.uint8(7))
    en_a_values = en_a.base_array
    correct_answer = np.array([0, 1, 1, 1, 1, 1, 1, 0, 1, 1]).astype(np.uint8)
    correct_checker = all((en_a_values[i] == correct_answer[i] for i in range(0, 10)))
    assert correct_checker is True


def test_eligible_numbers_number_of_eligible_values():
    """
    The purpose of this function is to test the get values
    :return:
    """
    en_a = EligibleNumbers()
    en_a.reset()
    en_a.eliminate_value(to_eliminate=np.uint8(7))
    en_a.eliminate_value(to_eliminate=np.uint8(3))
    en_a_values = en_a.number_of_eligible_values()
    correct_answer = np.array([0, 1, 1, 0, 1, 1, 1, 0, 1, 1]).astype(np.uint8).sum()
    correct_checker = en_a_values == correct_answer
    assert correct_checker == True


def test_eligible_numbers_eliminate_values():
    """
    The purpose of this function is to test the get values
    :return:
    """
    en_a = EligibleNumbers()
    en_a.reset()
    elimination_tuple = (np.uint8(7),np.uint8(3))
    en_a.eliminate_values(to_eliminate=elimination_tuple)
    en_a_values = en_a.number_of_eligible_values()
    correct_answer = np.array([0, 1, 1, 0, 1, 1, 1, 0, 1, 1]).astype(np.uint8).sum()
    correct_checker = en_a_values == correct_answer
    assert correct_checker == True