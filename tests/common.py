from typing import Dict, Optional, List
from models.group import Group
from models.matrix import Matrix
from models.individual import Individual
from models.preference import Preference

from random import randint

EXAMPLE_MATRIX_2PREF = [
    [None, 'Orion Mills', 'Aleeza Espinosa', ' - ', 'Carlie Burrows', 'Sarah Stewart'],
    [None, 'Kendal Carlson', 'Kelsey Smart', 'Declan Burns', 'Neive Savage', 'Sarah Stewart'],
    [None, 'Vienna Draper', 'Ricardo Senior', 'Orion Mills', 'Humayra Hook', 'Declan Burns'],
    [None, 'Atlas Webb', 'Sana Galindo', 'Harvie Dickens', 'Humayra Hook', 'Aleeza Espinosa'],
    [None, 'Ricardo Senior', 'Hanifa Mccarthy', 'Orion Mills', 'Sarah Stewart', 'Carlie Burrows'],
    [None, 'Sarah Stewart', ' - ', ' - ', 'Hanifa Mccarthy', 'Carlie Burrows'],
    [None, 'Alesha Hatfield', 'Sana Galindo', 'Lucie Banks', 'Carlie Burrows', ' - '],
    [None, 'Hanifa Mccarthy', ' - ', ' - ', 'Sarah Stewart', 'Carlie Burrows'],
    [None, 'Aneurin Parkes', 'Aleeza Espinosa', 'Jamie Ray', 'Humayra Hook', ' - '],
    [None, 'Aleeza Espinosa', 'Orion Mills', 'Aneurin Parkes', 'Carlie Burrows', 'Humayra Hook'],
    [None, 'Sana Galindo', 'Declan Burns', 'Luna Mccormick', 'Humayra Hook', 'Sarah Stewart'],
    [None, 'Declan Burns', 'Luna Mccormick', 'Kelsey Smart', 'Neive Savage', ' - '],
    [None, 'Jamie Ray', 'Aleeza Espinosa', 'Harvie Dickens', 'Clarissa Guthrie', 'Carlie Burrows'],
    [None, 'Harvie Dickens', 'Jamie Ray', 'Sana Galindo', ' - ', 'Sarah Stewart'],
    [None, 'Lucie Banks', ' - ', ' - ', ' - ', ' - '],
    [None, 'Kelsey Smart', 'Luna Mccormick', 'Kendal Carlson', 'Neive Savage', 'Humayra Hook'],
    [None, 'Luna Mccormick', 'Kendal Carlson', 'Declan Burns', 'Neive Savage', ' - '],
    [None, 'Neive Savage', 'Atlas Webb', 'Hanifa Mccarthy', ' - ', ' - '],
    [None, 'Zayne Dejesus', ' - ', ' - ', ' - ', ' - '],
    [None, 'Clarissa Guthrie', ' - ', ' - ', ' - ', ' - '],
    [None, 'Darren Obrien', ' - ', ' - ', ' - ', ' - '],
    [None, 'Humayra Hook', ' - ', ' - ', ' - ', ' - '],
    [None, 'Carlie Burrows', ' - ', ' - ', ' - ', ' - ']
]

def generate_matrix_of_size(number_of_prefs :int) -> list:
    number_of_persons = randint(5, 55)
    matrix = []
    for person in range(number_of_persons):
        person_name = chr(person+65)
        row = [None, person_name]
        for pref_type in ['preferences', 'de_preferences']:
            for pref_number in range(1, number_of_prefs+1):
                probability_of_having_preference = 35 + 100/pref_number #35+50 is the max, then its goes down
                random_person_to_add = chr(randint(5, 55) + 65)
                if random_person_to_add != person_name and randint(0, 100) >= probability_of_having_preference:
                    row.append(random_person_to_add)
                else:
                    row.append(' - ')
        matrix.append(row)

    return matrix

def get_initialized_matrix(number_of_prefs :int) -> Matrix:
    matrix = EXAMPLE_MATRIX_2PREF if number_of_prefs == 2 else generate_matrix_of_size(number_of_prefs=number_of_prefs)
    return Matrix(matrix, number_of_preferences=number_of_prefs)

def get_score_per_preferece_dict(number_of_prefs :int) -> dict:
    """
    Returns a dict in the format {
        number_of_column_in_excel: score value,
        ....
    }
    It starts counting from 1 (and, since the first column of the excel is unused, the first preference value has an index of 2)
    """
    person_class = get_initialized_matrix(number_of_prefs)
    out = {}
    for i in range(number_of_prefs):
        out[i+2] = person_class.get_pref_score(i+1)
    for i in range(number_of_prefs):
        out[i+2+number_of_prefs] = person_class.get_pref_score(-1*(i+1))
    return out

def create_individual(name:str = 'Individual', *preferences: Dict) -> Individual:
    individual = Individual(name=name)
    for preference in preferences:
        individual.add_preference(name=preference['name'], score=preference['score'], preference=preference['preference'])
    return individual

def create_group(*individuals: Individual):
    group = Group()
    for individual in individuals:
        group.add_member(individual=individual)
    return group


def get_individual(name_of_individual: str):
    #For some reason I decided to invent a rivarly between the pika line and the nido line, I dunno.
    if name_of_individual == 'nidoking':
        return create_individual('nidoking',
            {'name':'nidoqueen', 'score':10, 'preference': 1},
            {'name':'nidoran', 'score':4, 'preference' : 2},
            {'name':'pikachu', 'score':-6, 'preference' : -1},
            {'name':'raichu', 'score':-3, 'preference': -2}
        )
    if name_of_individual == 'nidoqueen':
        return create_individual('nidoqueen',
            {'name':'nidoran', 'score':8, 'preference': 1},
            {'name':'nidoking', 'score':6, 'preference': 2},
            ##Intentionally this preference is left blank
            {'name':'pichu', 'score':-3, 'preference' : -2},
        )
    if name_of_individual == 'nidoran':
        return create_individual('nidoran', 
            {'name':'nidoking', 'score':6, 'preference': 1},
            {'name':'nidoqueen', 'score':4, 'preference': 2},
            ##Intentionally this preference is left blank
            ##Intentionally this preference is left blank
        )
    if name_of_individual == 'raichu':
        return create_individual('raichu',
            {'name':'pikachu', 'score':6, 'preference': 1},
            {'name':'pichu', 'score':4, 'preference': 2},
            {'name':'nidoking', 'score':-6, 'preference': -1},
            ##Intentionally this preference is left blank
        )
    if name_of_individual == 'pichu':
        return create_individual('pichu',
            {'name':'pikachu', 'score':6, 'preference': 1},
            {'name':'raichu', 'score':4, 'preference': 2},
            {'name':'nidoking', 'score':-6, 'preference': -1},
            {'name':'nidorino', 'score':-4, 'preference': -2},
        )
    if name_of_individual == 'pikachu':
        return create_individual('pikachu',
            {'name':'pichu', 'score':6, 'preference': 1},
            {'name':'raichu', 'score':4, 'preference': 2},
            ##Intentionally this preference is left blank
            ##Intentionally this preference is left blank
        )
    if name_of_individual == 'pachirisu':
        return create_individual('pachirisu',
            {'name':'pichu', 'score':6, 'preference': 1},
            {'name':'pikachu', 'score':4, 'preference': 2},
            ##Intentionally this preference is left blank
            {'name':'raichu', 'score':-4, 'preference': -2},
        )
    if name_of_individual == 'plusle':
        return create_individual('plusle',
            {'name':'minum', 'score':6, 'preference': 1},
            {'name':'pichu', 'score':4, 'preference': 2},
            ##Intentionally this preference is left blank
            ##Intentionally this preference is left blank
        )
    if name_of_individual == 'minum':
        return create_individual('minum',
            {'name':'plusle', 'score':6, 'preference': 1},
            {'name':'pichu', 'score':4, 'preference': 2},
            ##Intentionally this preference is left blank
            ##Intentionally this preference is left blank
        )
    if name_of_individual == 'ditto':
        return create_individual('ditto',
            ##Intentionally this preference is left blank
            ##Intentionally this preference is left blank
            ##Intentionally this preference is left blank
            ##Intentionally this preference is left blank
        )

