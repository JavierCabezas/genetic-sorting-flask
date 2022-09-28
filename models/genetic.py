import random
import statistics

from typing import List, Dict
from .person import Person
from .config import Config

class Genetic:
    persons_per_group: int
    person_class: Person

    groups: List  # Selected groups.
    current_score: int  # Score of the selected group
    switches: int  # Number of times that the group was changed (just for stats)
    current_std: float  # Standard deviation of all the scores of all the sub-groups of the current solution

    def __init__(self, person: Person, persons_per_group: int):
        self.persons_per_group = persons_per_group
        self.person_class = person

    def calculate(self):
        """
        Returns the best possible group found within the number of loops configured
        """
        person_indexes = list(self.person_class.person_cache_dict_name_index.values())
        population_size = len(person_indexes)
        config_model = Config()

        self.groups = person_indexes
        self.current_score = self.get_groups_score(self.get_sub_groups(self.groups))
        self.current_std = self.get_sub_group_std(self.get_sub_groups(self.groups))
        self.switches = 0
        number_of_loops = config_model.get_config_value(path=['app', 'number_of_loops'])
        for _ in range(number_of_loops):
            candidate_group = self.create_group_by_crossing_over(population_size)
            candidate_score = self.get_groups_score(self.get_sub_groups(candidate_group))
            # If the score is better, switch.
            # If the score is the same but the std is lower, switch.
            # Otherwise, keep current solution
            if candidate_score > self.current_score:
                is_candidate_group_better = True
            elif candidate_score == self.current_score:
                candidate_std = self.get_sub_group_std(self.get_sub_groups(candidate_group))
                if candidate_std < self.current_std:
                    is_candidate_group_better = True
                else:
                    is_candidate_group_better = False
            else:
                is_candidate_group_better = False

            if is_candidate_group_better:
                self.groups = candidate_group
                self.current_score = candidate_score
                self.current_std = self.get_sub_group_std(self.get_sub_groups(self.groups))
                self.switches += 1

    def create_group_by_crossing_over(self, population_size: int) -> List:
        number_of_flips = random.randint(1, population_size)
        out = self.groups.copy()
        for _ in range(number_of_flips):
            origin_person_idx = random.randint(0, population_size - 1)
            target_person_idx = random.randint(0, population_size - 1)
            out[origin_person_idx], out[target_person_idx] = out[target_person_idx], out[origin_person_idx]
        return out

    def get_sub_groups(self, ids: List) -> List:
        """
        Receives a list of person_id and returns the sub-groups
        Ex: If group size = 3 and ids = [1, 2, 3, 4, 5, 6, 7, 8] returns [[1,2,3], [4,5,6], [7,8]]
        :param ids:
        :return:
        """
        return [ids[i:i + self.persons_per_group] for i in range(0, len(ids), self.persons_per_group)]

    def legible_groups(self, groups: List) -> List:
        out = []
        for student_id_list_in_group in self.get_sub_groups(groups):
            #student_id_list_in_group is a list of students ids that are in the resulting group (Ex: [2, 4, 10] for a group for the 3 students with those ids)
            to_add = {
                'rows': [],
                'group_score' : self.get_groups_score([student_id_list_in_group])
            }
            for student_id in student_id_list_in_group:
                preferences = self.person_class.persons[student_id][self.person_class.INDEX_PREFERENCES]
                to_add['rows'].append({
                    'name': self.person_class.get_name_from_person_id(student_id),
                    'score': self.person_class.get_score_from_person_perspective(student_id_list_in_group, preferences)
                }),
            out.append(to_add)

        return out

    def number_of_sub_groups(self) -> int:
        """
        :return: int
        """
        return len(self.get_sub_groups(self.groups))

    def get_sub_group_std(self, separated_groups: List):
        """
        Gets the standard deviation of the scores of each of the sub-groups of the groups array
        :param separated_groups:
        :return:
        """
        scores = [self.get_groups_score([group]) for group in separated_groups]
        return statistics.stdev(scores)

    def get_groups_score(self, groups: List) -> int:
        """
        Receives a list of sub-groups and returns the added up score of each of these sub-groups
        :param groups:
        :param person_class:
        :return:
        """
        total_score = 0
        for group in groups:
            # The sub-group contains a group of person_ids
            for selected_person_id in group:
                total_score += self.person_class.get_score_from_person_perspective(
                    target_person_ids=group,
                    origin_person_preferences=self.person_class.persons[selected_person_id][self.person_class.INDEX_PREFERENCES],
                )
        return total_score
