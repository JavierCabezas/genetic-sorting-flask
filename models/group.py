from re import I
from .individual import Individual
from typing import List, Dict

import statistics

class Group:
    def __init__(self) -> None:
        self.members :List[Dict] = []
        self.score = 0
        self.std = 0

    def individuals_in_members(self) -> List[Individual]:
        return [individualDict['individual'] for individualDict in self.members]

    def add_member(self, individual: Individual) -> None:
        self.members.append({'individual': individual, 'score': 0})
        self.update_stadistics()

    def update_stadistics(self) -> None:
        scores = []
        for individualWithScore in self.members:
            individualWithScore['score'] = self.get_score_by_individual_in_group(individual=individualWithScore['individual'])
            scores.append(individualWithScore['score'])
        self.score = sum(scores)
        if len(scores) > 1:
            self.std = statistics.stdev(scores)

    def get_score_by_individual_in_group(self, individual: Individual) -> int:
        """
        This score is the score given in the point of view of this invidual, this means, Does this individual like the
        other individuals in the group? 
        """
        #TODO: Lambda this
        score = 0
        member_names = [str(individual) for individual in self.individuals_in_members()]
        for preference in individual.preferences:
            if preference.name in member_names:
                score += preference.score
        return score


