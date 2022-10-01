class Preference:
    def __init__(self, name: str, score :int, preference :int) -> None:
        self.score = score
        self.pref_value = preference
        self.name = name