# SameGame-AI
Artificial Intelligence Project #1

### Methods that need to be implemented in class "Problem"
* path_cost - (Revision only) - function that calculates the cost of the path
* h - heuristic function


### Ideias for comparing function and for heuristic function
* For comparing function: order clusters from right to left, bottom to top, when
* they are found instead of when they are removed. This will allows to choose the
* clusters to remove when they draw on astar function, prioritizing the ones that
* need less concatenations, by choosing the one with highest column first

* For the heuristic function we count the number of pieces of each color, when 
* the program starts, save those values in the state and then try to remove smaller
* clusters first in order to generate bigger clusters that can be removed at once
* decreasing probability of shifts while making bigger clusters of other colors.
