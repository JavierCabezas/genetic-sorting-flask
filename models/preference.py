class Preference:
    """
    The Preference class is responsible to save, as the class name implies, a preference. This preference can be both 
    positive (an individual prefering another individual) or negative (an individual prefering to avoid another one). 
    Its attributes are:
        - name: Name of the individual. Just to clarify: This is the TARGET individual. If we want to store that A 
        wants to be in a group with B then the name will be B. Then this preference will be associated to the user A.
        - score: The score is the level of how big the preference is. It can be both positive and negative. So if 
        the preference is a big positive number it means that the individual that we're assinging this preference 
        to really wants to be in a group with the name passed in this preference. The same can be said, but the
        complete opposite, if the preference is a big negative number. This value can't be zero because the indiference
        does not get stored as a Preference.
        - preference: This is an interval value that its needed for displaying the data.
    """
    def __init__(self, name: str, score :int, preference :int) -> None:
        if score == 0:
            pass
        self.score = score
        self.pref_value = preference
        self.name = name