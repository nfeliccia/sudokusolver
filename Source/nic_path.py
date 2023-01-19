import os
import typing
from pathlib import PosixPath, WindowsPath

import pandas as pd

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This code gives operating system flexibility
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if os.name == 'posix':
    base = PosixPath
else:
    base = WindowsPath


# The purpose of the NIC Path is to provide

class NicPath(base):

    def __init__(self, opin=r"C:\\"):
        super().__init__()

    def read_excel(self, load_multiple_sheets: bool = False, **kwargs: dict) -> pd.DataFrame | typing.Dict:
        """
        The purpose of this function is to read an Excel file using Pandas. If load_multiple_sheets is set to true
        and there is  more than one sheet in the workbook, the return will be a dictionary with the keys as
        sheet names, and the values as dataframes. Otherwise, the return will be just a simple dataframe.


        :param bool load_multiple_sheets: If multiple sheets exist, and this is True, return the
        :param kwargs: Any kwargs that cna be passed along to pandas read_excel function.
        :return: dataframe of the first data sheet in an Excel file.
        :rtype: pd.DataFrame
        """

        # Create the Excel reader
        re_excel_reader = pd.ExcelFile(path_or_buffer=self, engine='openpyxl')

        # Set flag for multiple workbooks read.
        sheets_in_workbook = len(re_excel_reader.sheet_names)
        multiple_sheets_exist = sheets_in_workbook > 1
        read_multiple = multiple_sheets_exist and load_multiple_sheets

        if read_multiple:
            with re_excel_reader as reer:
                read_excel_dictionary = {x: pd.read_excel(io=reer, sheet_name=x, **kwargs) for x in
                                         re_excel_reader.sheet_names}
            return read_excel_dictionary

        with re_excel_reader as reer:
            read_df = pd.read_excel(io=reer, **kwargs)
        return read_df
