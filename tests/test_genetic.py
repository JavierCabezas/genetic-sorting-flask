from models.genetic import Genetic
from models.individual import Individual
from tests.common import get_individual

from typing import List

def test_get_initial_group_groups():
    nidoking = get_individual('nidoking')
    nidoqueen = get_individual('nidoqueen')
    nidoran = get_individual('nidoran')
    raichu = get_individual('raichu')
    pichu = get_individual('pichu')
    pikachu = get_individual('pikachu')
    pachirisu = get_individual('pachirisu')
    plusle = get_individual('plusle')
    minum = get_individual('minum')
    ditto = get_individual('ditto')

    sample_list_8 = [nidoking, nidoqueen, nidoran, raichu, pichu, pikachu, pachirisu, plusle]
    sample_list_9 = [nidoking, nidoqueen, nidoran, raichu, pichu, pikachu, pachirisu, plusle, minum]
    sample_list_10 = [nidoking, nidoqueen, nidoran, raichu, pichu, pikachu, pachirisu, plusle, minum, ditto]

    ## Groups of 2
    genetic_8_2 = Genetic(individuals=sample_list_8, persons_per_group=2)
    generated_groups = genetic_8_2.get_initial_group_groups(sample_list_8).members 
    assert len(generated_groups) == 4
    assert generated_groups[0].individuals_in_members() == [nidoking, nidoqueen]
    assert generated_groups[1].individuals_in_members() == [nidoran, raichu]
    assert generated_groups[2].individuals_in_members() == [pichu, pikachu]
    assert generated_groups[3].individuals_in_members() == [pachirisu, plusle]
    
    genetic_9_2 = Genetic(individuals=sample_list_9, persons_per_group=2)
    generated_groups = genetic_9_2.get_initial_group_groups(sample_list_9).members 
    assert len(generated_groups) == 5
    assert generated_groups[0].individuals_in_members() == [nidoking, nidoqueen]
    assert generated_groups[4].individuals_in_members() == [minum]

    ## Groups of 3
    genetic_10_3 = Genetic(individuals=sample_list_10, persons_per_group=3)
    generated_groups = genetic_10_3.get_initial_group_groups(sample_list_10).members 
    assert len(generated_groups) == 4
    assert generated_groups[0].individuals_in_members() == [nidoking, nidoqueen, nidoran]
    assert generated_groups[1].individuals_in_members() == [raichu, pichu, pikachu]
    assert generated_groups[2].individuals_in_members() == [pachirisu, plusle, minum]
    assert generated_groups[3].individuals_in_members() == [ditto]


    ## Groups of 4
    genetic_10_4 = Genetic(individuals=sample_list_10, persons_per_group=4)
    generated_groups = genetic_10_4.get_initial_group_groups(sample_list_10).members 
    assert len(generated_groups) == 3
    assert generated_groups[0].individuals_in_members() == [nidoking, nidoqueen, nidoran, raichu]
    assert generated_groups[1].individuals_in_members() == [pichu, pikachu, pachirisu, plusle]
    assert generated_groups[2].individuals_in_members() == [minum, ditto]


def no_test_groups_score():
    genetic_class = get_initialized_genetic(number_of_prefs=2, persons_per_group=3)
    assert -59  == genetic_class.get_groups_score([[21, 2, 8], [10, 1, 14], [5, 4, 7], [6, 0, 22], [13, 20, 11], [15, 16, 17], [9, 3, 18], [12, 19]])
    assert -4 == genetic_class.get_groups_score([[0,1,2], [3,4,5], [6,7,8], [9,10,11], [12,13,14], [15,16,17], [18,19,20], [21,22]])
    assert 42 == genetic_class.get_groups_score([[22, 18, 13], [5, 19, 21], [14, 1, 15], [6, 10, 3], [11, 20, 16], [0, 2, 4], [12, 8, 9], [17, 7]])
    assert 50 == genetic_class.get_groups_score([[12, 18, 13], [2, 0, 4], [20, 6, 14], [10, 11, 16], [1, 15, 22], [19, 5, 21], [3, 17, 7], [8, 9]])
    assert 44 == genetic_class.get_groups_score([[18, 19, 22], [11, 5, 21], [7, 3, 17], [0, 2, 4], [1, 15, 16], [12, 8, 9], [6, 10, 13], [14, 20]])
    ##The order of the persons in the group should not modify the result
    assert 44 == genetic_class.get_groups_score([[22, 18, 19], [13, 6, 10], [17, 3, 7], [0, 2, 4], [15, 1, 16], [5, 21, 11], [8, 12, 9], [20, 14]])
