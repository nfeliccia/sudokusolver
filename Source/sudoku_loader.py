import os
import pickle
from pathlib import Path

import numpy as np
import pandas as pd


def load_puzzle(puzzle_path: Path = None):

    if puzzle_path.suffix =='.xlsx':
        lp_excel_reader = pd.ExcelFile(puzzle_path, engine='openpyxl')
        with lp_excel_reader as ler:
            puzzle_array = pd.read_excel(ler, header=None).fillna(0).astype(np.uint8)

        puzzle_df_array = puzzle_array.values
        return puzzle_df_array

    if puzzle_path.suffix=='.pkl':
        with open(puzzle_path,'rb') as pp:
            puzzle_array = pickle.load(pp)
        return puzzle_array




