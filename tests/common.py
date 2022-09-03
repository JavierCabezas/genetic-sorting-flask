from models.person import Person

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

def get_initialized_person(number_of_prefs :int) -> Person:
    if number_of_prefs == 2:
        return Person(EXAMPLE_MATRIX_2PREF)

def get_score_per_preferece_dict(number_of_prefs :int) -> dict:
	"""
	Returns a dict in the format {
		number_of_column_in_excel: score value,
		....
	}
	It starts counting from 1 (and, since the first column of the excel is unused, the first preference value has an index of 2)
	"""
	person_class = get_initialized_person(number_of_prefs)
	out = {}
	for i in range(number_of_prefs):
		out[i+2] = person_class.get_pref_score(i+1)
	for i in range(number_of_prefs):
		out[i+2+number_of_prefs] = person_class.get_pref_score(-1*(i+1))
	return out

