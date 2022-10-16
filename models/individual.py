from typing import List, Optional
from .preference import Preference

class Individual:
    """
    The individual class defines each of the members, this means the persons, that we're assigning into groups. 
    It has two attributes:
        - name: As the name implies, the name of this individual. There is a limitation that this acts as a 
            the primary key, meaning that we can't have two individuals with the same name.
        - preferences: A list of the class Preference. See the preference class for details. 
    """
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
    
    def get_score(self, *names_in_group: str) -> int:
        """
        Given this individual preferences, gets thee score for the names passed as arugment (Ex: 'Jane', 'Joe', 'Steve'...) 
        :names_in_group: 
        """
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