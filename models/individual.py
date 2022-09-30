from typing import List
from .preference import Preference

class Individual:

    def __init__(self, name :str) -> None:
        self.name = name
        self.preferences = [] #Cambiar casting a List de Preference

    def add_preference(self, name :str, score :int) -> bool:
        INVALID_NAMES = ['-', ' - ', '', 'None', 'none', '.', '...']
        if name in INVALID_NAMES:
            return False
        else:
            self.preferences.append(Preference(score=score, name=name))
            return True
    
    def get_score(self, names_in_group: List) -> int:
        """
        Given this individual preferences, gets the score for the group passed by a list of names. (Ex: ['Jane', 'Joe', 'Steve']) 
        :names_in_group: A list of strings with each of the names in the group
        """
        #Cambiar por una lambda sum function
        score = 0
        for preference in self.preferences:
            if preference.name in names_in_group:
                score += preference.score
        return score