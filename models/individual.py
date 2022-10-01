from typing import List, Optional
from .preference import Preference

class Individual:

    def __init__(self, name :str) -> None:
        self.name = name
        self.preferences :List[Preference] = []

    def __str__(self) -> str:
        return self.name

    def add_preference(self, name :str, score :int, preference :int) -> bool:
        INVALID_NAMES = ['-', ' - ', '', 'None', 'none', '.', '...']
        if name in INVALID_NAMES:
            return False
        else:
            self.preferences.append(Preference(score=score, name=name, preference=preference))
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

    def preference_by_value(self, pref_value :int) -> Optional[Preference]:
        """
        Returns, if exists, the preference for this individual with this specific preference value
        """
        for preference in self.preferences:
            if preference.pref_value == pref_value:
                return preference
        return None