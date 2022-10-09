from .matrix import Matrix
from .config import Config
from .group import Group
from .groupGroup import GroupGroup
from .individual import Individual

from typing import List


class Genetic:
    persons_per_group: int
    matrix_class: Matrix

    groupGroup: GroupGroup  # Selected groups.
    switches: int  # Number of times that the group was changed (just for stats)

    def __init__(self, individuals :List[Individual], persons_per_group: int):
        self.persons_per_group = persons_per_group
        self.groupGroup = self.get_initial_group_groups(individuals)

    def get_initial_group_groups(self, persons :List[Individual]):
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
            self.groupGroup.flip_between_groups()
            # If the score is better, switch.
            # If the score is the same but the std is lower, switch.
            # Otherwise, keep current solution
            if self.groupGroup.get_score(get_cached_value=True) > self.groupGroup.get_last_score():
                is_candidate_group_better = True
            elif self.groupGroup.get_score(get_cached_value=True) == self.groupGroup.get_last_score():
                if self.groupGroup.get_std(get_cached_value=True) < self.groupGroup.get_last_std():
                    is_candidate_group_better = True
                else:
                    is_candidate_group_better = False
            else:
                is_candidate_group_better = False

            if not is_candidate_group_better:
                self.groupGroup.undo_last_flip()
                self.switches += 1


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