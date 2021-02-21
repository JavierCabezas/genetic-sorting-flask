import random

from typing import List, Dict
from .person import Person


class Genetic:
    SCORE_PREF_1 = 3
    SCORE_PREF_2 = 2
    SCORE_DEPREF_1 = -6
    SCORE_DEPREF_2 = -4

    NUMBER_OF_LOOPS = 50000

    persons_per_group :int
    person_class :Person

    groups: List
    current_score: int

    def __init__(self, person: Person, persons_per_group: int):
        self.persons_per_group = persons_per_group
        self.person_class = person

    def get_score_for_pref(self) -> int:
        return 2

    def calculate(self):
        person_indexes = list(self.person_class.person_cache_dict_name_index.values())
        initial_population = Genetic.create_random_group(ids=person_indexes, persons_per_group=self.persons_per_group)
        population_size = len(person_indexes)

        self.groups = initial_population
        self.current_score = Genetic.get_groups_store(self.groups)
        print("!")

    @staticmethod
    def create_random_group(ids: List, persons_per_group: int) -> List:
        random.shuffle(ids)
        return [ids[i:i + persons_per_group] for i in range(0, len(ids), persons_per_group)]

    @staticmethod
    def get_groups_store(group: List) -> int:
        total_score = 0
        for sub_group in group:
            total_score += 1
        return total_score