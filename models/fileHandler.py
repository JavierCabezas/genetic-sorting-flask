from collections import OrderedDict
from io import BytesIO
from json import loads 
import urllib.parse

from pyexcel_xlsx import get_data, save_data
from typing import List

class FileHandler:

    def __init__(self, number_of_preferences :int):
        self.number_of_preferences = number_of_preferences

    @staticmethod
    def get_matrix_from_excel(file) -> List:
            data = get_data(file)
            first_index = next(iter(data))
            return data[first_index][1:]

    @staticmethod
    def get_json_to_io_download(form_data) -> BytesIO:
        row_data = loads(urllib.parse.unquote(form_data))
        group_size = len(row_data[0]['rows'])
        number_of_groups = len(row_data)
        excel_matrix = [[0 for x in range(group_size+1)] for y in range(number_of_groups)]
        row_idx = 0

        for row in row_data:
            excel_matrix[row_idx][0] = "Group " + str(row_idx+1)
            person_idx = 0
            for person in row['rows']:
                excel_matrix[row_idx][person_idx+1] = person['name']
                person_idx = person_idx + 1
            row_idx = row_idx + 1

        
        data = OrderedDict()
        data.update({"Sheet 1": excel_matrix})
        io = BytesIO()
        save_data(io, data)
        io.seek(0)
        return io


    def transform_column_to_preference(self, column_number: int) -> int:
        """
        Gets the column number in the file and returns the preference value associated to it
        Ex: If there are two preferences then the columns 2 and 3 are going to be the first two preferences and
            columns 4 and 5 are going to be the first de-pref and second de-pref. So:

        +---------------+------------+
        |  Column num   | Return val |
        +---------------+------------+
        |       2       |      1     |
        |       3       |      2     |
        |       4       |      -1    |
        |       5       |      -2    |
        +---------------+------------+

        :param column_number:
        :param number_of_preferences:
        :return:
        """

        is_negative_pref = column_number - 1 > self.number_of_preferences
        if is_negative_pref:
            return -1 * (column_number - 1 - self.number_of_preferences)
        else:
            return column_number - 1