from models.genetic import GroupGroup
from common import get_individual, create_group, create_groupgroup

def test_groups_score():
    nidoking = get_individual('nidoking')
    nidoqueen = get_individual('nidoqueen')
    nidoran = get_individual('nidoran')
    pichu = get_individual('pichu')
    pikachu = get_individual('pikachu')
    raichu = get_individual('raichu')

    nido_group = create_group(nidoking, nidoqueen, nidoran)
    pika_group = create_group(pichu, pikachu, raichu)

    wholesome_groupgroup = create_groupgroup(nido_group, pika_group)
    total_score = nido_group.score + pika_group.score
    assert total_score == wholesome_groupgroup.get_score()
    assert 68 == wholesome_groupgroup.get_score()

    terrible_group_1 = create_group(nidoking, pikachu, raichu)
    terrible_group_2 = create_group(nidoqueen, pichu)
    terrible_groupgroup = create_groupgroup(terrible_group_1, terrible_group_2)
    total_score = terrible_group_1.score + terrible_group_2.score
    assert total_score == terrible_groupgroup.get_score()
    assert -12 == terrible_groupgroup.get_score()

    ##Test that the score is updated after a flip
    terrible_groupgroup.flip_between_groups()
    assert total_score != terrible_groupgroup.get_score()
    assert -12 != terrible_groupgroup.get_score()


    
