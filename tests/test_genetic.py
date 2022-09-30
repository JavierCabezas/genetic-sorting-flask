from models.genetic import Genetic
import common


def get_initialized_genetic(number_of_prefs :int, persons_per_group: int) -> Genetic:
    return Genetic(common.get_initialized_person(number_of_prefs), persons_per_group)

def test_sub_groups():
    sample_list_7 = [1, 2, 3, 4, 5, 6, 7]
    sample_list_8 = [1, 2, 3, 4, 5, 6, 7, 8]
    sample_list_9 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    sample_list_10 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    ## Groups of 2
    genetic_class = get_initialized_genetic(number_of_prefs=2, persons_per_group=2)
    assert genetic_class.get_sub_groups(sample_list_8) == [[1,2], [3,4], [5,6], [7,8]]
    assert genetic_class.get_sub_groups(sample_list_9) == [[1,2], [3,4], [5,6], [7,8], [9]]

    ## Groups of 3
    genetic_class = get_initialized_genetic(number_of_prefs=2, persons_per_group=3)
    assert genetic_class.get_sub_groups(sample_list_8) == [[1,2,3], [4,5,6], [7,8]]
    assert genetic_class.get_sub_groups(sample_list_9) == [[1,2,3], [4,5,6], [7,8,9]]
    assert genetic_class.get_sub_groups(sample_list_10) == [[1,2,3], [4,5,6], [7,8,9], [10]]

    ## Groups of 4
    genetic_class = get_initialized_genetic(number_of_prefs=2, persons_per_group=4)
    assert genetic_class.get_sub_groups(sample_list_7) == [[1,2,3,4], [5,6,7]]
    assert genetic_class.get_sub_groups(sample_list_8) == [[1,2,3,4], [5,6,7,8]]
    assert genetic_class.get_sub_groups(sample_list_9) == [[1,2,3,4], [5,6,7,8], [9]]

def no_test_groups_score():
    genetic_class = get_initialized_genetic(number_of_prefs=2, persons_per_group=3)
    assert -59  == genetic_class.get_groups_score([[21, 2, 8], [10, 1, 14], [5, 4, 7], [6, 0, 22], [13, 20, 11], [15, 16, 17], [9, 3, 18], [12, 19]])
    assert -4 == genetic_class.get_groups_score([[0,1,2], [3,4,5], [6,7,8], [9,10,11], [12,13,14], [15,16,17], [18,19,20], [21,22]])
    assert 42 == genetic_class.get_groups_score([[22, 18, 13], [5, 19, 21], [14, 1, 15], [6, 10, 3], [11, 20, 16], [0, 2, 4], [12, 8, 9], [17, 7]])
    assert 50 == genetic_class.get_groups_score([[12, 18, 13], [2, 0, 4], [20, 6, 14], [10, 11, 16], [1, 15, 22], [19, 5, 21], [3, 17, 7], [8, 9]])
    assert 44 == genetic_class.get_groups_score([[18, 19, 22], [11, 5, 21], [7, 3, 17], [0, 2, 4], [1, 15, 16], [12, 8, 9], [6, 10, 13], [14, 20]])
    ##The order of the persons in the group should not modify the result
    assert 44 == genetic_class.get_groups_score([[22, 18, 19], [13, 6, 10], [17, 3, 7], [0, 2, 4], [15, 1, 16], [5, 21, 11], [8, 12, 9], [20, 14]])
