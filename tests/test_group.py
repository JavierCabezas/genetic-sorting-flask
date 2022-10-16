from models import individual
from tests.common import get_individual, create_group

def test_basics():
    nidoking = get_individual('nidoking')
    nidoqueen = get_individual('nidoqueen')
    nidoran = get_individual('nidoran')
    pichu = get_individual('pichu')
    pikachu = get_individual('pikachu')
    raichu = get_individual('raichu')

    nido_line = create_group(nidoking, nidoqueen, nidoran)
    assert nido_line.members[0]['individual'] == nidoking
    assert nido_line.members[1]['individual'] == nidoqueen
    assert nido_line.members[2]['individual'] == nidoran
    assert len(nido_line.members) == 3
    assert [str(individual) for individual in nido_line.individuals_in_members()] == ['nidoking', 'nidoqueen', 'nidoran']
    members_in_group = nido_line.individuals_in_members()
    assert members_in_group[0] == nidoking
    assert members_in_group[1] == nidoqueen
    assert members_in_group[2] == nidoran
    assert nido_line.get_score_by_individual_in_group(nidoking) == 14
    total_nido_score = nido_line.get_score_by_individual_in_group(nidoking) +\
        nido_line.get_score_by_individual_in_group(nidoqueen) +\
        nido_line.get_score_by_individual_in_group(nidoran) 
    assert nido_line.score == 38
    assert nido_line.score == total_nido_score
    assert nido_line.std == 2.309401076758503

    #Add new member and check if everything gets updated
    nido_line_plus_raichu = nido_line
    nido_line_plus_raichu.add_member(raichu)
    total_nido_plus_raichu_score = nido_line_plus_raichu.get_score_by_individual_in_group(nidoking) +\
        nido_line_plus_raichu.get_score_by_individual_in_group(nidoqueen) +\
        nido_line_plus_raichu.get_score_by_individual_in_group(nidoran) +\
        nido_line_plus_raichu.get_score_by_individual_in_group(raichu)    
    assert nido_line_plus_raichu.score == 29
    assert nido_line_plus_raichu.score == total_nido_plus_raichu_score
    assert nido_line_plus_raichu.std == 8.99536917900909
    assert nido_line.get_score_by_individual_in_group(raichu) == -6

    unconfortable_group = create_group(nidoking, pichu, pikachu, raichu)
    assert unconfortable_group.get_score_by_individual_in_group(nidoking) == -9
    assert unconfortable_group.get_score_by_individual_in_group(pikachu) == 10 #Pikachu likes everyone
    assert unconfortable_group.get_score_by_individual_in_group(pichu) == 4
    assert unconfortable_group.get_score_by_individual_in_group(raichu) == 4
    assert -9 + 10 + 4 + 4 == unconfortable_group.score

def test_crossovers():
    nidoking = get_individual('nidoking')
    nidoqueen = get_individual('nidoqueen')
    nidoran = get_individual('nidoran')
    pichu = get_individual('pichu')
    pikachu = get_individual('pikachu')
    raichu = get_individual('raichu')

    nido_group = create_group(nidoking, nidoqueen, nidoran)
    pika_group = create_group(pichu, pikachu, raichu)

    members_in_nido_group = nido_group.individuals_in_members()
    members_in_pika_group = pika_group.individuals_in_members()
    assert nidoking in members_in_nido_group and nidoqueen in members_in_nido_group and nidoran in members_in_nido_group
    assert pikachu in members_in_pika_group and pichu in members_in_pika_group and raichu in members_in_pika_group
    assert nido_group.score == 38
    assert nido_group.std == 2.309401076758503
    assert pika_group.score == 30
    assert pika_group.std == 0

    #Switch members between the nido and the pika group
    #Since the switch is random you must implement creative ways to see how well it worked
    nido_group.switch_member_with_other_group(pika_group)
    members_in_new_nido_group = nido_group.individuals_in_members()
    members_in_new_pika_group = pika_group.individuals_in_members()
    assert pichu in members_in_new_nido_group or pikachu in members_in_new_nido_group or raichu in members_in_new_nido_group
    assert nidoran in members_in_new_pika_group or nidoqueen in members_in_new_pika_group or nidoking in members_in_new_pika_group
    assert not (nidoking in members_in_new_nido_group and nidoqueen in members_in_new_nido_group and nidoran in members_in_new_nido_group)
    assert not (pikachu in members_in_new_pika_group and pichu in members_in_new_pika_group and raichu in members_in_new_pika_group)

    assert nido_group.std != 2.309401076758503
    assert pika_group.std != 0 #Exactly the same values as before

    #Check that the new values are exactly the new ones expected
    score_new_nido_group = sum([
        member.get_score(*(member.name for member in members_in_new_nido_group))
        for member 
        in members_in_new_nido_group
    ])
    assert nido_group.score == score_new_nido_group

    #Revert the crossover and everything should go back to normal
    nido_group.undo_last_switch(pika_group)

    members_in_nido_group = nido_group.individuals_in_members()
    members_in_pika_group = pika_group.individuals_in_members()
    assert nidoking in members_in_nido_group and nidoqueen in members_in_nido_group and nidoran in members_in_nido_group
    assert pikachu in members_in_pika_group and pichu in members_in_pika_group and raichu in members_in_pika_group
    assert nido_group.score == 38
    assert nido_group.std == 2.309401076758503
    assert pika_group.score == 30
    assert pika_group.std == 0
