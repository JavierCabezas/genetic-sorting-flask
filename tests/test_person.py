from models.person import Person
import common

def test_get_score_from_person_perspective():
    person_class = common.get_initialized_person(2)
    pref_dict = common.get_score_per_preferece_dict(2)

    pref_1_idx = 2
    pref_2_idx = 3
    depref_1_idx = 4
    depref_2_idx = 5

    #preferences is a dict in where the index is the id of the preference type and the value is the person id
    preferences = {pref_1_idx: 10, pref_2_idx: 11, depref_1_idx: 20, depref_2_idx: 21 }

    only_disliked_persons = [20, 21]
    score = person_class.get_score_from_person_perspective(only_disliked_persons, preferences, pref_dict)
    assert person_class.get_pref_score(-1) + person_class.get_pref_score(-2) ==score

    disliked_perons_and_others_without_points = [1, 2, 3, 4, 5, 6, 20, 21]
    score = person_class.get_score_from_person_perspective(disliked_perons_and_others_without_points, preferences, pref_dict)
    assert person_class.get_pref_score(-1) + person_class.get_pref_score(-2) ==score

    most_disliked_person_and_others_without_points = [1, 4, 20]
    score = person_class.get_score_from_person_perspective(most_disliked_person_and_others_without_points, preferences, pref_dict)
    assert person_class.get_pref_score(-1) ==score

    everyone = [10, 11, 20, 21]
    score = person_class.get_score_from_person_perspective(everyone, preferences, pref_dict)
    assert sum(person_class.get_pref_score(pref) for pref in[1, 2, -1, -2])  == score

    only_positive_scores = [10, 11]
    score = person_class.get_score_from_person_perspective(only_positive_scores, preferences, pref_dict)
    assert person_class.get_pref_score(1) + person_class.get_pref_score(2)  == score

    neutral_scores = [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 14, 15, 16, 17, 18, 19]
    score = person_class.get_score_from_person_perspective(neutral_scores, preferences, pref_dict)
    assert 0 == score