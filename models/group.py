from .individual import Individual
from typing import List

import statistics

class Group:
    def __init__(self) -> None:
        self.members = []
        self.score = 0
        self.std = 0

    def add_member(self, individual: Individual) -> None:
        self.members.append(individual)
        self.update_stadistics()

    def update_stadistics(self) -> None:
        scores = self.get_scores()
        self.score = sum(scores)
        self.std = statistics.stdev(scores)

    def get_scores(self) -> List:
        #TODO: Cambiar por una lambda function que me consiga los names
        #TODO: Make this method private
        score = 0
        member_names = []
        for member in self.members:
            member_names.append(member.name)
        return [member.get_score(member_names) for member in self.members]