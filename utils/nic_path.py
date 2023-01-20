import os
import pickle
import typing
from copy import copy
from pathlib import PosixPath, WindowsPath
from typing import Type

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

    def __init__(self, operational_input=r"C:\\"):
        super().__init__()

    def __copy__(self):
        copy_path = NicPath(str(self))
        return copy_path

    def _set_suffix(self, set_suffix: str = None, read: bool = False) -> Type[FileNotFoundError] | 'NicPath':
        """
        This function returns a separate NicPath based on the current path with the suffix changed.
        :param str set_suffix: new suffix to set
        :param bool read: True verifies new file exists
        :return: New NicPath with the suffix changed.
        :rtype: NicPath
        :raises FileNotFoundError"
        """

        # don't change if not necessary
        if self.suffix == set_suffix:
            if read and not self.exists():
                return FileNotFoundError
            set_suffix_path = copy(self)
            return set_suffix_path

        # return copy of with suffix output.
        set_suffix_path = self.with_suffix(set_suffix)
        return set_suffix_path

    def read(self, **kwargs) -> typing.Any:
        """
        The purpose of this function is to provide a simplified single point read which reads based on the suffix.
        :return:
        """

        if self.suffix == '.xlsx' or self.suffix == '.xls':
            read_df = self.read_excel(**kwargs)
            return read_df

        if self.suffix == '.csv':
            read_df = self.read_csv(**kwargs)
            return read_df

        if self.suffix == '.pkl':
            read_df = self.read_pickle(**kwargs)
            return read_df

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

        # Adjust engine for suffix.  Capture the most common 2 and let pandas handle other less common logic.
        read_path = copy(self)
        if self.suffix == '.xlsx':
            re_engine = 'openpyxl'
        elif self.suffix == '.xls':
            re_engine = 'xlrd'
        elif self.suffix is None:
            read_path = self.with_suffix('.xlsx')
            re_engine = 'openpyxl'
        else:
            re_engine = None

        # Create the Excel reader
        re_excel_reader = pd.ExcelFile(path_or_buffer=read_path, engine=re_engine)

        # Set flag for multiple workbooks read.
        sheets_in_workbook = len(re_excel_reader.sheet_names)
        multiple_sheets_exist = sheets_in_workbook > 1
        read_multiple = multiple_sheets_exist and load_multiple_sheets

        # read multiple worksheets case.
        if read_multiple:
            with re_excel_reader as re_excel_reader_context:
                read_excel_dictionary = {x: pd.read_excel(io=re_excel_reader_context, sheet_name=x, **kwargs) for x in
                                         re_excel_reader.sheet_names}
            return read_excel_dictionary

        # read single worksheet case
        with re_excel_reader as re_excel_reader_context:
            read_df = pd.read_excel(io=re_excel_reader_context, **kwargs)

        return read_df

    def read_csv(self, **kwargs: dict) -> pd.DataFrame:
        """
        The purpose of this function is to read csv files for the NicPath object.
        Uses pandas as an engine.
        https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html

        :param kwargs: a dictionary of kwargs which are compatible with pandas read_csv
        :return: Dataframe reflecting csv contents
        :rtype pd.DataFrame:
        """
        # correct the input path if it's not csv.
        read_path = self._set_suffix(set_suffix='.csv')

        # create the pandas reader
        read_csv_df = pd.read_csv(read_path, **kwargs)

        return read_csv_df

    def read_pickle_df(self, **kwargs) -> pd.DataFrame:
        """
        The purpose of this function is to read a dataframe which has been pickled.
        It leverages the pandas read pickle function.
        :return:Unpickled DataFrame Object
        """

        # correct the input path if it's not pkl.
        read_path = self._set_suffix(set_suffix='.pkl')

        # create the pickle reader
        read_pickle_df = pd.read_pickle(read_path, **kwargs)

        return read_pickle_df

    def read_pickle(self, **kwargs) -> pd.DataFrame:
        # correct the input path if it's not pkl.
        read_path = self._set_suffix(set_suffix='.pkl')

        # create the pickle reader
        with open(read_path, 'rb') as rprp:
            read_pickle_objec = pickle.load(rprp, **kwargs)

        return read_pickle_objec
