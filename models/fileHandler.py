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