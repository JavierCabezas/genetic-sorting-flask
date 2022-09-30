from .groupGroup import GroupGroup
import random

from typing import List
from .matrix import Matrix
from .config import Config

class Genetic:
    persons_per_group: int
    matrix_class: Matrix

    groups: List  # Selected groups.
    current_score: int  # Score of the selected group
    switches: int  # Number of times that the group was changed (just for stats)
    current_std: float  # Standard deviation of all the scores of all the sub-groups of the current solution

    #TODO: Hint that persons should be a list of persons
    def __init__(self, persons :List, persons_per_group: int):
        self.persons_per_group = persons_per_group
        self.groups = self.get_initial_groups(persons)
        #TODO: Initialize the current score and std with the values of the initial group generated
        self.current_score = self.get_solution_score()
        self.current_std = self.get_solution_std()

    def get_initial_groups(self, persons :List):
        """
        Generates the initial groups. 
        Ex: If group size = 3 and Persons = [P1, P2, P3, P4, P5, P6, P7, P8] it generates the groups
        Group 2 = [1,2,3], Group 2 = [4,5,6], Group 3=[7,8]
        """
        groups_to_return = []
        groups_to_add = [persons[i:i + self.persons_per_group] for i in range(0, len(persons), self.persons_per_group)]
        for group_to_add in groups_to_add:
            new_group = Group()
            for individual in group_to_add:
                new_group.add_member(individual=individual)
            groups_to_return.append(new_group)
        return groups_to_return

    def calculate(self):
        """
        Returns the best possible group found within the number of loops configured
        """
        config_model = Config()

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

    def legible_groups(self, groups: List) -> List:
        out = []
        for student_id_list_in_group in self.get_sub_groups(groups):
            #student_id_list_in_group is a list of students ids that are in the resulting group (Ex: [2, 4, 10] for a group for the 3 students with those ids)
            to_add = {
                'rows': [],
                'group_score' : self.get_groups_score([student_id_list_in_group])
            }
            for student_id in student_id_list_in_group:
                preferences = self.matrix_class.persons[student_id][self.matrix_class.INDEX_PREFERENCES]
                to_add['rows'].append({
                    'name': self.matrix_class.get_name_from_person_id(student_id),
                    'score': self.matrix_class.get_score_from_person_perspective(student_id_list_in_group, preferences)
                }),
            out.append(to_add)

        return out

    def number_of_sub_groups(self) -> int:
        """
        :return: int
        """
        return len(self.get_sub_groups(self.groups))


    def get_groups_score(self, groups: List) -> int:
        """
        Receives a list of sub-groups and returns the added up score of each of these sub-groups
        :param groups:
        :param matrix_class:
        :return:
        """
        total_score = 0
        for group in groups:
            # The sub-group contains a group of person_ids
            for selected_person_id in group:
                total_score += self.matrix_class.get_score_from_person_perspective(
                    target_person_ids=group,
                    origin_person_preferences=self.matrix_class.persons[selected_person_id][self.matrix_class.INDEX_PREFERENCES],
                )
        return total_score
