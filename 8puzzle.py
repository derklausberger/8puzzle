#!/usr/bin/env python

from random import randint
from numpy import empty
from time import time
from sys import stdout

# Checks if a number exists in an array by:
# Comparing each entry to a passed number
# until a given index is reached
def check_existence(state, rand_int, idx):
    for i in range(0, idx + 1):
        if i == idx:
            return False
        elif int(state[i]) == int(rand_int):
            return True

# Generates a state by:
# Defining an empty array with length 9
# Adding a random int from 0 to 8 to the array
# if the number isn't already in the array
# When finished, returns the array
def gen_state():
    state = empty(9)
    for i in range(0, 9):
        rand_int = randint(0, 8)
        while check_existence(state, rand_int, i):
            rand_int = randint(0, 8)
        state[i] = rand_int
    return state

# Prints the game by:
# Looping through the array and
# adding spaces and line breaks
def print_state(state):
    for i in range(0, 9):
        print(int(state[i]), end=" ")
        if (i + 1) % 3 == 0:
            print()
    print()

# Checks if a sequence of numbers in an array is solvable by:
# Comparing each element with all the elements that come after it
# Incrementing inv (inversions) if an element is found that is
# smaller than the current element and both are not equal to zero
def solvable(game_state):
    inv = 0
    for i in range(0, 9):
        for j in range(i, 9):
            if game_state[i] != 0 and game_state[j] != 0 and game_state[i] > game_state[j]:
                inv += 1

    if inv % 2 == 0:
        # print("Solvable")
        return True
    else:
        # print("Not Solvable")
        return False

# Calculates the hamming distance by:
# Incrementing the distance if a number is not 0 and
# is not at the index that is the same as the number
# 2 must be at index 2, 4 at 4
# Therefore, only works for the goal state
# 0 1 2 3 4 5 6 7 8 
def hamming(game_state):
    distance = 0
    for i in range(0, 9):
        if game_state[i] != 0 and game_state[i] != i:
            distance += 1

    # print("hamming distance:", distance)
    return distance

# Calculates the manhatten distance by:
# Incrementing the distance if an element is not equal to zero
# by adding the number of rows and columns that the element
# is away from its goal position
def manhatten(state):
    distance = 0
    for i in range(0, 9):
        if state[i] != 0:
	# columns
            distance += abs(int(i / 3) - int(state[i] / 3))
	# rows
            distance += int(abs(i % 3 - state[i] % 3))

    # print("manhatten distance:", distance)
    return distance

animation_text = "SOLVING..."
animation_idx = 0

def solve(curr_state, heuristic):
    global animation_idx

    states = {}
    distance = heuristic(curr_state)

    while distance != 0:
        #stdout.write(animation_text[animation_idx % len(animation_text)])
        #animation_idx += 1

        neighbors = {}
        zero_pos = 0
        for i in range(0, 9):
            if curr_state[i] == 0:
                zero_pos = i
                # print(zero_pos)
                break

        if zero_pos % 3 == 1:
            neighbors[len(neighbors)] = zero_pos + 1
            neighbors[len(neighbors)] = zero_pos - 1
        elif zero_pos % 3 == 2:
            neighbors[len(neighbors)] = zero_pos - 1
        elif zero_pos % 3 == 0:
            neighbors[len(neighbors)] = zero_pos + 1

        if int(zero_pos / 3) == 1:
            neighbors[len(neighbors)] = zero_pos - 3
            neighbors[len(neighbors)] = zero_pos + 3
        elif int(zero_pos / 3) == 2:
            neighbors[len(neighbors)] = zero_pos - 3
        elif int(zero_pos / 3) == 0:
            neighbors[len(neighbors)] = zero_pos + 3

        # Finds children and copies into states array
        for i in range(0, len(neighbors)):
            child = curr_state.copy()
            child[zero_pos] = curr_state[neighbors[i]]
            child[neighbors[i]] = 0
            if not states.get(str(child)):
                states[str(child)] = [child.copy(), False]

        # Compares the best state with the current state in the states array
	# If there is no best state (first iteration), sets it to this state
	# Else, if the current state is better than the best state regarding
	# the heuristic's distance, sets the best state to this state
        best_state = ""

        for state in states:
            if not states[state][1]:
                if best_state == "" or heuristic(states[state][0]) < heuristic(states[best_state][0]):
                    best_state = state

	# Changes the current number sequence to the best state
	# Recalculates the distance regarding the new state
	# When all children have been found, adds True in the key/value map (dictionary)
        curr_state = states[best_state][0].copy()
        distance = heuristic(curr_state)
        states[best_state][1] = True

        #if animation_idx % len(animation_text) == 0:
        #    stdout.write("\r")

    #stdout.write("\r")
    return len(states)
    # print_state(curr_state)

def main():
    start = time()

    for heuristic in ["hamming", "manhatten"]:
        sum = 0
        for i in range(0, 100):
            start_state = gen_state()
            while not solvable(start_state):
                start_state = gen_state()
            # print("hamming distance:", hamming(start_state))

            sum += solve(start_state, eval(heuristic))

            # print("solved game nr", i)
        end = time()
        print("time to solve 100 puzzles using", heuristic, "was", format(end - start, '.3f'), "seconds and the average number of expanded nodes was", int(sum / 100))

if name == "main":
    main()