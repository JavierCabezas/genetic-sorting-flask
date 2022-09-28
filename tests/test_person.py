from models.person import Person
import common

def test_get_score_from_person_perspective():
    person_class = common.get_initialized_person(2)

    pref_1_idx = 2
    pref_2_idx = 3
    depref_1_idx = 4
    depref_2_idx = 5

    #preferences is a dict in where the index is the id of the preference type and the value is the person id
    preferences = {pref_1_idx: 10, pref_2_idx: 11, depref_1_idx: 20, depref_2_idx: 21 }

    only_disliked_persons = [20, 21]
    score = person_class.get_score_from_person_perspective(only_disliked_persons, preferences)
    assert person_class.get_pref_score(-1) + person_class.get_pref_score(-2) ==score

    disliked_persons_and_others_without_points = [1, 2, 3, 4, 5, 6, 20, 21]
    score = person_class.get_score_from_person_perspective(disliked_persons_and_others_without_points, preferences)
    assert person_class.get_pref_score(-1) + person_class.get_pref_score(-2) ==score

    most_disliked_person_and_others_without_points = [1, 4, 20]
    score = person_class.get_score_from_person_perspective(most_disliked_person_and_others_without_points, preferences)
    assert person_class.get_pref_score(-1) ==score

    everyone = [10, 11, 20, 21]
    score = person_class.get_score_from_person_perspective(everyone, preferences)
    assert sum(person_class.get_pref_score(pref) for pref in[1, 2, -1, -2])  == score

    only_positive_scores = [10, 11]
    score = person_class.get_score_from_person_perspective(only_positive_scores, preferences)
    assert person_class.get_pref_score(1) + person_class.get_pref_score(2)  == score

    neutral_scores = [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 14, 15, 16, 17, 18, 19]
    score = person_class.get_score_from_person_perspective(neutral_scores, preferences)
    assert 0 == score

def test_get_pref_score():
    person_class = common.get_initialized_person(number_of_prefs=2)
    assert person_class.get_pref_score(2)  == 4
    assert person_class.get_pref_score(1)  == 2
    assert person_class.get_pref_score(-2)  == -3
    assert person_class.get_pref_score(-1)  == -6

    person_class = common.get_initialized_person(number_of_prefs=4)
    assert person_class.get_pref_score(2)  == 4
    assert person_class.get_pref_score(1)  == 2
    assert person_class.get_pref_score(-2)  == -9
    assert person_class.get_pref_score(-1)  == -12

