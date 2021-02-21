import random

from typing import List, Dict
from .person import Person


class Genetic:
    NUMBER_OF_LOOPS = 50000

    persons_per_group :int
    person_class :Person

    groups: List
    current_score: int

    def __init__(self, person: Person, persons_per_group: int):
        self.persons_per_group = persons_per_group
        self.person_class = person

    def calculate(self):
        person_indexes = list(self.person_class.person_cache_dict_name_index.values())
        initial_population = Genetic.create_random_group(ids=person_indexes, persons_per_group=self.persons_per_group)
        population_size = len(person_indexes)

        self.groups = initial_population
        self.current_score = Genetic.get_groups_score(self.groups, self.person_class)

    @staticmethod
    def create_random_group(ids: List, persons_per_group: int) -> List:
        random.shuffle(ids)
        return [ids[i:i + persons_per_group] for i in range(0, len(ids), persons_per_group)]

    @staticmethod
    def get_groups_score(group: List, person_class: Person) -> int:
        total_score = 0
        for sub_group in group:
            #The sub-group contains a group of person_ids
            for selected_person_id in sub_group:
                total_score += Person.get_score_from_person_perspective(
                    target_person_ids=sub_group,
                    origin_person_preferences=person_class.persons[selected_person_id][Person.INDEX_PREFERENCES],
                    score_per_preference_dict=person_class.score_cache_dict
                )
        return total_score