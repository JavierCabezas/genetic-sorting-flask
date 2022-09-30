from .group import Group
from typing import List

import statistics

class GroupGroup:
    def __init__(self) -> None:
        self.members = []
        self.score = 0

    def add_member(self, group: Group) -> None:
        self.members.append(group)
        self.update_stadistics()

    def update_stadistics(self) -> None:
        scores = self.get_scores()
        self.score = sum(scores)

    def get_scores(self) -> List:
        #TODO: Cambiar por una lambda function que me consiga los names
        #TODO: Make this method private
        return [group.score for group in self.members]