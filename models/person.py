from typing import List, Dict, Optional
from .fileHandler import FileHandler


class Person:
    EXCEL_COL_INDEX_NAME: int = 1

    INDEX_NAME: str = 'name'
    INDEX_IDX_PERSON: str = 'idxPerson'
    INDEX_PREFERENCES: str = 'preferences'

    ERROR_PERSON_NOT_FOUND = -1

    persons: List
    person_cache_dict_name_index: Dict
    score_cache_dict: Dict

    def __init__(self, matrix: List, number_of_preferences:int = 2):
        self.number_of_preferences = number_of_preferences
        self.fill_persons_from_matrix(matrix)
        self.fill_preferences(matrix)

    def fill_persons_from_matrix(self, matrix: List):
        """
        Fills both the persons dict and the cache of dict names
        :param matrix:
        :return:
        """
        names = [row[self.EXCEL_COL_INDEX_NAME] for row in matrix]
        self.persons = []
        self.person_cache_dict_name_index = {}
        for index, name in enumerate(names):
            self.persons.append({
                self.INDEX_NAME: name,
                self.INDEX_IDX_PERSON: index,
                self.INDEX_PREFERENCES: {}
            })
            self.person_cache_dict_name_index[name] = index

    def number_of_persons(self) -> int:
        return len(self.persons)

    def fill_preferences(self, matrix :List):
        preferences_list = [pref_column for pref_column in range(2, 2*(self.number_of_preferences+1))]
        for index, person in enumerate(self.persons):
            for preference_index in preferences_list:
                person_name_for_preference = matrix[index][preference_index]
                person_index_for_preference = self.get_index_from_person_name(person_name_for_preference)
                if person_index_for_preference != self.ERROR_PERSON_NOT_FOUND:
                    self.persons[index][self.INDEX_PREFERENCES][preference_index] = person_index_for_preference

    def get_index_from_person_name(self, name: str) -> int:
        if name in self.person_cache_dict_name_index:
            return self.person_cache_dict_name_index[name]
        else:
            return self.ERROR_PERSON_NOT_FOUND

    def get_pref_score(self, preference_number :int) -> int:
        """
        Returns the score of a specific preference value. A preference value is the value that the students select in the excel file (first preference, second preference, first depreference, 
        second depreference, etc...). So if the system has 3 preference values:
    
        +---------------+-------+
        |  Preference   | Value |
        +---------------+-------+
        | First         |     1 |
        | Second        |     2 |
        | Third         |     3 |
        | First depref  |    -1 |
        | Second depref |    -2 |
        | Third depref  |    -3 |
        +---------------+-------+

        And the output score will be calculated by doing:
            For positive scores: 2 times the preference amount
            For negative scores: -3 times how un-preferable (-1 being the most un-preferable) the match is
            (So we punish more teams with de-preferences)
        :prefNumber:
        """
        if preference_number > 0:
            return preference_number * 2
        elif preference_number == 0:
            return 0
        else:
            return -3 * (self.number_of_preferences  - abs(preference_number) + 1)

    def get_score_from_person_perspective(self, target_person_ids: List, origin_person_preferences: Dict) -> int:
        total_score = 0
        reader = FileHandler(number_of_preferences=self.number_of_preferences)
        for id_preference_type in origin_person_preferences.keys():
            preferred_person_id = origin_person_preferences[id_preference_type]
            if preferred_person_id in target_person_ids:
                pref_number = reader.transform_column_to_preference(id_preference_type)
                total_score += self.get_pref_score(pref_number)
        
        return total_score

    def get_name_from_person_id(self, person_id: Optional[int] = None) -> str:
        """
        :param person_id:
        :return:
        """
        if person_id in list(range(0, len(self.persons))):
            return self.persons[person_id][self.INDEX_NAME]
        else:
            return '-'