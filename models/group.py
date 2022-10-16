from __future__ import annotations

from .individual import Individual
from typing import List, Dict
from random import randint

import statistics

class Group:
    """
    A group is the class that stores the individuals 
    It has 3 main attributes:
        - members: A dictionary that has both the individual and their individual score for this group. 
            I may change how this works in the future because I'm not 100% sold in this data structure.
        - score: The group score is the sum of the individual scores of all the individuals in the group.
        - std: The standard deviation of each individual score.
    """
    def __init__(self) -> None:
        self.members :List[Dict] = []
        self.score = 0
        self.std = 0
        self.__groupSize = 0 #Cache
        self.__last_flip_origin_member_idx = 0
        self.__last_flip_target_member_idx = 0

    def add_member(self, individual: Individual) -> None:
        self.members.append({'individual': individual, 'score': 0})
        self.update_stadistics()

    def individuals_in_members(self) -> List[Individual]:
        return [individualDict['individual'] for individualDict in self.members]

    def update_stadistics(self) -> None:
        scores = []
        for index in range(len(self.members)):
            new_score = self.get_score_by_individual_in_group(target_individual=self.members[index]['individual'])
            self.members[index].update({'score': new_score})    
            scores.append(new_score)
        self.score = sum(scores)
        if len(scores) > 1:
            self.std = statistics.stdev(scores)
        self.__groupSize = len(self.members)

    def get_score_by_individual_in_group(self, target_individual: Individual) -> int:
        """
        This score is the score given in the point of view of this invidual.
        This means, Does this individual like the other individuals in the group? 
        """
        return target_individual.get_score(*(str(individual) for individual in self.individuals_in_members()))

    def switch_member_with_other_group(self, group: Group) -> None:
        origin_member_idx = randint(0, self.__groupSize -1)
        target_member_idx = randint(0, group.__groupSize -1)
        self.members[origin_member_idx], group.members[target_member_idx] =\
            group.members[target_member_idx], self.members[origin_member_idx]
        
        self.__last_flip_origin_member_idx= origin_member_idx
        self.__last_flip_target_member_idx = target_member_idx
        self.__last_std = self.std
        self.__last_score = self.score
        group.__last_std = group.std
        group.__last_score = group.score
        
        self.update_stadistics()
        group.update_stadistics()

    def undo_last_switch(self, group: Group):
        """
        Assumptions (taken for perfomance reasons, since this is part of the main algorithm):
            - The method won't be called with two different groups (this means that, we won't call switch with group A, 
            then switch with group B and then revert the switch with group A)
            - We intentionally skip the stadistics for performance, that's why the score and std value is saved on switching
        """
        self.members[self.__last_flip_origin_member_idx], group.members[self.__last_flip_target_member_idx] =\
            group.members[self.__last_flip_target_member_idx], self.members[self.__last_flip_origin_member_idx]
        self.score = self.__last_score
        self.std = self.__last_std
        group.score = group.__last_score
        group.std = group.__last_std
