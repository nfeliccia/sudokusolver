import time

import numpy as np
import pandas as pd


def test_four_ways_of_creating_one_to_nine():
    limit = 100000

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Test the generation via numpy with a given list
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    direct_numpy_generate_start = time.perf_counter()
    for _ in range(0, limit):
        numpy_array = np.array((1, 2, 3, 4, 5, 6, 7, 8, 9), dtype=np.uint8)
    direct_numpy_generate_end = time.perf_counter()
    direct_numpy_generate_time = (direct_numpy_generate_end - direct_numpy_generate_start) * 1000

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Test the generation via np.arrange
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    numpy_arrange_generate_start = time.perf_counter()
    for _ in range(0, limit):
        numpy_arrange_array = np.arange(1, 10, dtype=np.uint8)
    numpy_arrange_generate_end = time.perf_counter()

    numpy_arrange_generation_time = (numpy_arrange_generate_end - numpy_arrange_generate_start) * 1000

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Test the generation via direct read including import
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    simple_read_start = time.perf_counter()
    from sudoku_utilities import main_nine_array
    import_end_time = time.perf_counter()
    for i in range(0, limit):
        some_nine_array = main_nine_array
    simple_read_end = time.perf_counter()
    simple_read_time = (simple_read_end - simple_read_start) * 1000
    import_time = (import_end_time - simple_read_start) * 1000
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Test the generation via standard_python_range
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    native_python_start = time.perf_counter()

    for i in range(0, limit):
        some_nine_array = range(0, 10)
    native_python_end = time.perf_counter()
    native_python_time = (native_python_end - native_python_start) * 1000

    results_dict = {'typed': direct_numpy_generate_time, 'arange': numpy_arrange_generation_time,
                    'simple_read': simple_read_time, 'import_time': import_time, 'native_python': native_python_time}

    return results_dict


four_ways_collector = [test_four_ways_of_creating_one_to_nine() for x in range(0, 10)]
four_ways_df = pd.DataFrame(data=four_ways_collector).round(3)
four_ways_df.to_csv(r".\four_ways.csv")
