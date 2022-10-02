from .matrix import Matrix
from .config import Config
from .group import Group
from .groupGroup import GroupGroup

from typing import List
from copy import deepcopy


class Genetic:
    persons_per_group: int
    matrix_class: Matrix

    groupGroup: GroupGroup  # Selected groups.
    current_score: int  # Score of the selected group
    switches: int  # Number of times that the group was changed (just for stats)
    current_std: float  # Standard deviation of all the scores of all the sub-groups of the current solution

    #TODO: Hint that persons should be a list of persons
    def __init__(self, persons :List, persons_per_group: int):
        self.persons_per_group = persons_per_group
        self.groupGroup = self.get_initial_group_groups(persons)

    def get_initial_group_groups(self, persons :List):
        """
        Generates the initial groups. 
        Ex: If group size = 3 and Persons = [P1, P2, P3, P4, P5, P6, P7, P8] it generates the groups
        Group 2 = [1,2,3], Group 2 = [4,5,6], Group 3 = [7,8]
        """
        group_group_to_return = GroupGroup()
        groups_to_add = [persons[i:i + self.persons_per_group] for i in range(0, len(persons), self.persons_per_group)]
        for group_to_add in groups_to_add:
            new_group = Group()
            for individual in group_to_add:
                new_group.add_member(individual=individual)
            group_group_to_return.add_member(new_group)
        return group_group_to_return


    def calculate(self):
        """
        Returns the best possible group found within the number of loops configured
        """
        config_model = Config()

        self.switches = 0
        if len(self.groupGroup.members) < 2:
            pass #Can't optimize if there are less than two groups

        number_of_loops = config_model.get_config_value(path=['app', 'number_of_loops'])
        for _ in range(number_of_loops):
            candidate_group_group = self.create_group_group_by_crossing_over()
            # If the score is better, switch.
            # If the score is the same but the std is lower, switch.
            # Otherwise, keep current solution
            if candidate_group_group.get_score(get_cached_value=True) > self.current_score:
                is_candidate_group_better = True
            elif candidate_group_group.get_score(get_cached_value=True) == self.current_score:
                candidate_std = candidate_group_group.get_std(get_cached_value=True)
                if candidate_std < self.current_std:
                    is_candidate_group_better = True
                else:
                    is_candidate_group_better = False
            else:
                is_candidate_group_better = False

            if is_candidate_group_better:
                self.groupGroup = candidate_group_group
                self.current_score = candidate_group_group.get_score(get_cached_value=True) 
                self.current_std = candidate_group_group.get_std(get_cached_value=True)
                self.switches += 1

    def create_group_group_by_crossing_over(self) -> GroupGroup:
        copied_group_group : GroupGroup = deepcopy(self.groupGroup())
        copied_group_group.flip_between_groups()
        return copied_group_group

    def legible_groups(self) -> List:
        out = []
        for group in self.groupGroup.members:
            to_add = {
                'rows': [],
                'group_score' : group.score
            }
            for individualWithScore in group.members:
                to_add['rows'].append({
                    'name': str(individualWithScore['individual']),
                    'score': individualWithScore['score']
                }),
            out.append(to_add)

        return out