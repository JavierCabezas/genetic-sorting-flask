from models.matrix import Matrix
import common

def test_get_pref_score():
    matrix_class = common.get_initialized_matrix(number_of_prefs=2)
    assert matrix_class.get_pref_score(2)  == 4
    assert matrix_class.get_pref_score(1)  == 2
    assert matrix_class.get_pref_score(-2)  == -3
    assert matrix_class.get_pref_score(-1)  == -6

    matrix_class = common.get_initialized_matrix(number_of_prefs=4)
    assert matrix_class.get_pref_score(2)  == 4
    assert matrix_class.get_pref_score(1)  == 2
    assert matrix_class.get_pref_score(-2)  == -9
    assert matrix_class.get_pref_score(-1)  == -12

def test_matrix_column_to_pref_score():
    matrix_class = common.get_initialized_matrix(number_of_prefs=2)
    assert matrix_class.matrix_column_to_pref_score(2)  == 1
    assert matrix_class.matrix_column_to_pref_score(3)  == 2
    assert matrix_class.matrix_column_to_pref_score(4)  == -1
    assert matrix_class.matrix_column_to_pref_score(5)  == -2


    #Test exceptions!!
    matrix_class = common.get_initialized_matrix(number_of_prefs=4)
    assert matrix_class.matrix_column_to_pref_score(2)  == 1
    assert matrix_class.matrix_column_to_pref_score(3)  == 2
    assert matrix_class.matrix_column_to_pref_score(4)  == 3
    assert matrix_class.matrix_column_to_pref_score(5)  == 4
    assert matrix_class.matrix_column_to_pref_score(6)  == -1
    assert matrix_class.matrix_column_to_pref_score(7)  == -2
    assert matrix_class.matrix_column_to_pref_score(8)  == -3
    assert matrix_class.matrix_column_to_pref_score(9)  == -4