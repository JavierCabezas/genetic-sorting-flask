from models.individual import Individual

def test_get_score():
    growlithe = Individual(name='growlithe')
    growlithe.add_preference(name='arcanine', score=6)
    growlithe.add_preference(name='vulpix', score=4)
    growlithe.add_preference(name='meowth', score=-6)
    growlithe.add_preference(name='persian', score=-3)

    assert 10 == growlithe.get_score(['arcanine', 'vulpix'])
    assert -9 == growlithe.get_score(['meowth', 'persian'])
    assert 1 == growlithe.get_score(['arcanine', 'vulpix', 'meowth', 'persian'])
    assert 0 == growlithe.get_score(['growlithe'])
    assert 0 == growlithe.get_score(['pikachu'])
    assert 6 == growlithe.get_score(['arcanine', 'pikachu', 'ralts'])
