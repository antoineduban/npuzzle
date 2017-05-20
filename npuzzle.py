#!/bin/python3

import sys

sys.path.insert(0, 'src/')

import core
import solve

def main():
    (size, start, end, heuristic) = core.init()
    nSelectedStates, nMaxStates, solution = solve.solve(size, start, end, heuristic)
    nStates, solution = solution
    print("Total number of states ever selected in open set: {:d}".format(nSelectedStates))
    print("Maximum number of states ever represented in memory at the same time: {:d}".format(nMaxStates))
    print("Number of moves required to solve the puzzle: {:d}".format(nStates))
    for state in solution:
        core.display(state)

main()
