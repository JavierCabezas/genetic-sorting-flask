from typing import List, Dict, Optional


class Person:
    EXCEL_COL_INDEX_NAME: int = 1
    EXCEL_COL_INDEX_PREF_1: int = 2
    EXCEL_COL_INDEX_PREF_2: int = 3
    EXCEL_COL_INDEX_NOPREF_1: int = 4
    EXCEL_COL_INDEX_NOPREF_2: int = 5

    INDEXES_PREFERENCES: List = [
        EXCEL_COL_INDEX_PREF_1,
        EXCEL_COL_INDEX_PREF_2,
        EXCEL_COL_INDEX_NOPREF_1,
        EXCEL_COL_INDEX_NOPREF_2
    ]

    SCORE_PREF_1 = 3
    SCORE_PREF_2 = 2
    SCORE_DEPREF_1 = -6
    SCORE_DEPREF_2 = -4

    INDEX_NAME: str = 'name'
    INDEX_IDX_PERSON: str = 'idxPerson'
    INDEX_PREFERENCES: str = 'preferences'

    ERROR_PERSON_NOT_FOUND = -1

    persons: List
    person_cache_dict_name_index: Dict
    score_cache_dict: Dict

    def __init__(self, matrix: List):
        self.fill_persons_from_matrix(matrix)
        self.fill_preferences(matrix)
        self.fill_score_cache_dict()

    def fill_score_cache_dict(self):
        self.score_cache_dict = {
            self.EXCEL_COL_INDEX_PREF_1: self.SCORE_PREF_1,
            self.EXCEL_COL_INDEX_PREF_2: self.SCORE_PREF_2,
            self.EXCEL_COL_INDEX_NOPREF_1: self.SCORE_DEPREF_1,
            self.EXCEL_COL_INDEX_NOPREF_2: self.SCORE_DEPREF_2,
        }

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
        """
        :param matrix:
        :return:
        """
        preferences_list = [
            self.EXCEL_COL_INDEX_PREF_1,
            self.EXCEL_COL_INDEX_PREF_2,
            self.EXCEL_COL_INDEX_NOPREF_1,
            self.EXCEL_COL_INDEX_NOPREF_2
        ]

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

    def get_pref_score(self, prefNumber :int) -> int:
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
        :prefNumber:
        """
        if prefNumber == 1:
            return self.SCORE_PREF_1
        elif prefNumber == 2:
            return self.SCORE_PREF_2
        if prefNumber == -1:
            return self.SCORE_DEPREF_1
        elif prefNumber == -2:
            return self.SCORE_DEPREF_2
        raise ValueError('Not a valid preference number')

    @staticmethod
    def get_score_from_person_perspective(
        target_person_ids: List,
        origin_person_preferences: Dict,
        score_per_preference_dict: Dict
    ) -> int:
        total_score = 0
        for id_preference_type in origin_person_preferences.keys():
            prefered_person_id = origin_person_preferences[id_preference_type]
            if prefered_person_id in target_person_ids:
                total_score += score_per_preference_dict[id_preference_type]
        
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