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
	genetic_class = get_initialized_genetic(2, 2)
	assert genetic_class.get_sub_groups(sample_list_8) == [[1,2], [3,4], [5,6], [7,8]]
	assert genetic_class.get_sub_groups(sample_list_9) == [[1,2], [3,4], [5,6], [7,8], [9]]

	## Groups of 3
	genetic_class = get_initialized_genetic(2, 3)
	assert genetic_class.get_sub_groups(sample_list_8) == [[1,2,3], [4,5,6], [7,8]]
	assert genetic_class.get_sub_groups(sample_list_9) == [[1,2,3], [4,5,6], [7,8,9]]
	assert genetic_class.get_sub_groups(sample_list_10) == [[1,2,3], [4,5,6], [7,8,9], [10]]

	## Groups of 4
	genetic_class = get_initialized_genetic(2, 4)
	assert genetic_class.get_sub_groups(sample_list_7) == [[1,2,3,4], [5,6,7]]
	assert genetic_class.get_sub_groups(sample_list_8) == [[1,2,3,4], [5,6,7,8]]
	assert genetic_class.get_sub_groups(sample_list_9) == [[1,2,3,4], [5,6,7,8], [9]]

def test_groups_score():
	genetic_class = get_initialized_genetic(2, 3)
	assert 0 == genetic_class.get_groups_score([[1,2], [3,4], [5,6], [7,8]], genetic_class.person_class)
	assert 0 == genetic_class.get_groups_score([[2,5], [8,4], [1,6], [7,3]], genetic_class.person_class)