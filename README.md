# genetic-sorting-flask
Genetic algorithm to sort students into study-groups based on their preference

This is a small project in where I'll use a (sort of) genetic algorithm to create person-groups of a selectable size based on their preference. 
It takes a list of persons and their corresponding preferences (who they prefer to be grouped with and who they don't prefer to be grouped with) and then
auto-generates groups given those preferences.

## File to upload ##
It reads an Excel file which contains the person list and their preferences.

The columns have the following format

* A: Not used
* B: Person Name
* C: First option of person that you would prefer to be in a group with
* D: Second option of person that you would prefer to be in a group with
* E: First option of the student that you would NOT prefer to be in a group with
* F: Second option of the student that you would NOT prefer to be in a group with
The output of the algorithm is N groups of students of a specific size, given by the user in a form.

## How the score works ## 
For picking the best groups a "score" variable is created. This "score" is calculated by assigning a value to each of the "want to be in a group with" options 
(positive for the ones that you would like to and negative for the ones you don't). 
Each person, given by their persepective, has their score for everyone else in the group added up, of everyone else in the group and the total score is added up. 
So, for example, if Group 1 has the persons A, B and C. The total score is Score(B, from the perspective of A) + Score(C, from the perspective of A) + Score(A, from the perspective of B) + 
Score(C, from the perspective of B) + Score(A, from the perspective of C) + Score(B, from the perspective of C)

Finally, the total score of the solution is the sum of the scores of each of the individual groups.

## Algorithm: ##

The algorithm works by:

1) Randomly creates a group of students.
2) Randomly swaps a number of students.
3) If the score of the randomly created group is better than the current group it swaps the current group with the newly created one. 
If the score is the same then the standard deviation of each of the student sub-groups is calculated. 
If this value is lower than the one of the current solution, then this solution is considered greater and is swapped. 
The logic behind the standard deviation is that, even if the score is the same, having groups with similar score is preferable before 
having groups with a great dispersion of scores. (So teams with similar scores are prefered)
4) This is looped N times.

## How to run ##
Since this project is docker-based its trivial to run.

1) Build the project with docker-compose build
2) Run docker-compose up


## How to run the tests ##

1) When building the docker project make sure that the target on the docker-compose is debug (instead of prod)
2) Run docker-compose up
3) Run bash run_tests.sh

## Known issues so far ##
1) If two or more in the excel have exactly the same name the system will get confused and return inconsistent data.
2) There is absolutely no validation for the uploaded excel file.

## TO-DOs: ## 

### Features ### 
* Make create a way in how config files can be updated in case newly created configuration variables are created (right now you must delete the old config)
* Update all the tests with the new model
* Upload to aws
* (and the most important one) Make the software more flexible, so it can read n preferences and de-preferences from the Excel file.
* MyPy?
* Separete person from FileHandler classes

### Improvements ###
* Can we merge somehow the classes groupGroup and Group? I should think in how to avoid repeating code
* Is there a way in how to avoid using a dict (ew) in group.py?