from tests.common import create_individual

def get_growlithe():
    return create_individual('growlite',
        {'name':'arcanine', 'score':6, 'preference': 1},
        {'name':'vulpix', 'score':4, 'preference' : 2},
        {'name':'meowth', 'score':-6, 'preference' : -1},
        {'name':'persian', 'score':-3, 'preference': -2}
    )

def test_preference_assignation():
    growlithe = get_growlithe()
    assert len(growlithe.preferences) == 4
    assert growlithe.preferences[0].name == 'arcanine'
    growlithe.add_preference('primeape', -3, -3)
    assert len(growlithe.preferences) == 5
    assert growlithe.preferences[4].name == 'primeape'


def test_get_score():
    growlithe = get_growlithe()
    assert 10 == growlithe.get_score('arcanine', 'vulpix')
    assert -9 == growlithe.get_score('meowth', 'persian')
    assert 1 == growlithe.get_score('arcanine', 'vulpix', 'meowth', 'persian')
    assert 0 == growlithe.get_score('growlithe')
    assert 0 == growlithe.get_score('pikachu')
    assert 6 == growlithe.get_score('arcanine', 'pikachu', 'ralts')

def test_preference_by_value():
    growlithe = get_growlithe()
    assert growlithe.preference_by_value(2).name == 'vulpix'
    assert growlithe.preference_by_value(-2).name == 'persian'
    assert growlithe.preference_by_value(40) == None