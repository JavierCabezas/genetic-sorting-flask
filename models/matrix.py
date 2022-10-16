from typing import List, Dict, Optional
from .individual import Individual


class Matrix:
    MATRIX_INDEX_NAME = 1
    individuals: List
    score_cache_dict: Dict

    def __init__(self, matrix: List, number_of_preferences:int = 2):
        self.number_of_preferences = number_of_preferences
        self.individuals = self.get_individuals_from_matrix(matrix)

    def get_individuals_from_matrix(self, matrix: List):
        """
        Fills the individuals array with the data from the array, then it fills the preferences of them
        :param matrix:
        :return:
        """
        individuals = []
        for row in matrix:
            individual = Individual(name=row[self.MATRIX_INDEX_NAME])
            ## Preferences
            for column_index in range(2, 2+2*self.number_of_preferences):
                target_person_name = row[column_index]
                pref_score = self.matrix_column_to_pref_score(column_index)                
                target_person_score = self.get_pref_score(pref_score)
                individual.add_preference(name=target_person_name, score=target_person_score, preference=pref_score)
            individuals.append(individual)
        return individuals

    def matrix_column_to_pref_score(self, matrix_column_number :int):
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

        :param matrix_column_number:
        :return:
        """
        if matrix_column_number < 2 or matrix_column_number > 2*self.number_of_preferences+1:
            raise RuntimeError('Invalid column number given (this should not happen')

        pref_value = matrix_column_number - 1
        return pref_value if pref_value <= self.number_of_preferences else -1 * (pref_value-self.number_of_preferences) 

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