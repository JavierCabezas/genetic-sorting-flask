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