from .group import Group
from typing import List
from functools import reduce

import statistics

class GroupGroup:
    def __init__(self) -> None:
        self.members  :List[Group] = []
        self.__score = 0
        self.__std = 0

    def add_member(self, group: Group) -> None:
        self.members.append(group)
        self.update_stadistics()

    def update_stadistics(self) -> None:
        scores = self.__get_scores()
        self.__score = sum(scores)
        if len(scores) > 1:
            self.std = statistics.stdev(scores)

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