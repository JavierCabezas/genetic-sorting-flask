from .group import Group
from typing import List
from functools import reduce
from random import randint

import statistics

class GroupGroup:
    """
    A GroupGroup, as the name implies, is a group of groups.
    It has 3 attributes:
        - members: The list of groups that composes this GroupGroup
        - score: This score is the sum of the scores of all the groups in this GroupGroup.
        - std: The std of the scores of all of the groups in this GroupGroup.
    """
    def __init__(self) -> None:
        self.members  :List[Group] = []
        self.__score = 0
        self.__std = 0
        self.__number_of_groups = 0 #Cache
        self.__last_flip_origin_group_idx = 0
        self.__last_flip_target_group_idx = 0

    def add_member(self, group: Group) -> None:
        self.members.append(group)
        self.update_stadistics()

    def update_stadistics(self) -> None:
        scores = self.__get_scores()
        self.__score = sum(scores)
        if len(scores) > 1:
            self.std = statistics.stdev(scores)
        self.__number_of_groups = len(self.members)

    def __get_scores(self) -> List:
         return [int(group.score) for group in self.members]

    def get_score(self, get_cached_value :bool =False) -> int:
        if not get_cached_value:
            self.update_stadistics()
        return self.__score

    def get_std(self, get_cached_value :bool = False) -> float:
        if not get_cached_value:
            self.update_stadistics()
        return self.__std

    def get_number_of_individuals(self):
        return sum(len(group.members) for group in self.members)
    
    def get_all_individuals(self):
        return reduce((lambda x, y: x + y),  [group.individuals_in_members() for group in self.members])

    def flip_between_groups(self):
        """
        Takes one individual from one of the groups chosen at random and switches is with an individual 
        from other group, also chosen at random. 
        Assumes that there's more than one group (otherwise it can get into an infinite loop, but I didn't
        want to add the validation here in order to avoid extra overhead to the calculation method)
        """

        origin_group_idx = randint(0, self.__number_of_groups - 1) 
        target_group_idx = origin_group_idx  #This is to force a value and to emulate a do-while 
        while target_group_idx == origin_group_idx:
            target_group_idx = randint(0, self.__number_of_groups - 1)

        self.__last_flip_origin_group_idx = origin_group_idx
        self.__last_flip_target_group_idx = target_group_idx
        self.__last_std = self.__std
        self.__last_score = self.__score

        self.members[origin_group_idx].switch_member_with_other_group(self.members[target_group_idx])
        self.update_stadistics()

    def get_last_score(self) -> int:
        return self.__last_score

    def get_last_std(self) -> float:
        return self.__last_std

    def undo_last_flip(self):
        self.members[self.__last_flip_origin_group_idx].undo_last_switch(self.members[self.__last_flip_target_group_idx])
        
        #The update_statdistics() method is not called for performance
        self.__score = self.__last_score
        self.__last_std = self.__last_std