from ast import Str
import json
from os.path import exists, dirname, realpath
from typing import Dict, List

class Config:
    DEFAULT_VALUES = {
        "app": {
            "number_of_loops": 10000,
            "default_persons_per_group": 3,
            "default_preference_columns": 2
        }
    }

    def get_config_file_path(self) -> Str:
        this_path = dirname(realpath(__file__))
        return "{}/../config.json".format(this_path)

    def __init__(self):
        self.create_config_file_if_not_exists()
        self.values = self.get_fill_values_from_config_file()

    def create_config_file_if_not_exists(self):
        if not exists(self.get_config_file_path()):
            config_file = open(self.get_config_file_path(), "w+")
            config_file.write(json.dumps(self.DEFAULT_VALUES, indent=4))
            config_file.close

    def get_fill_values_from_config_file(self) -> Dict:
        if not exists(self.get_config_file_path()):
            # If the file wasn't created for any reason then get the default values anyway
            return self.DEFAULT_VALUES
        
        config_file = open(self.get_config_file_path(), "r")
        config_file_contents = config_file.read()
        config_file.close()

        try:
            config_values = json.loads(config_file_contents)
        except ValueError as e:
            return self.DEFAULT_VALUES

        return config_values

        
    def get_config_value(self, path :List) -> Str:
        temp = self.values
        try:
            for key in path:
                temp = temp[key]
        except KeyError as e:
            raise RuntimeError('Failed to load config value')
        else:
            value_to_return = temp

        return value_to_return

