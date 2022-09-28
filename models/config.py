from ast import Str
import json
from os.path import exists, dirname, realpath
from typing import List

class Config:
    DEFAULT_VALUES = {
        "app": {
            "number_of_loops": 10000
        }
    }

    def get_config_file_path(self) -> Str:
        this_path = dirname(realpath(__file__))
        return "{}/../config.json".format(this_path)


    def __init__(self):
        self.create_config_file_if_not_exists()
        with open(self.get_config_file_path()) as json_data_file:
            self.data = json.load(json_data_file)

    def create_config_file_if_not_exists(self):
        if not exists(self.get_config_file_path()):
            config_file = open(self.get_config_file_path(), "w+")
            config_file.write(json.dumps(self.DEFAULT_VALUES, indent=4))
            config_file.close

    def get_config_value(self, path :List):
        return 2

