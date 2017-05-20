#!/bin/python3

import sys

sys.path.insert(0, 'src/')

import core
import solve

def inversions(puzzle):
    total = 0
    for i in range(len(puzzle)):
        if puzzle[i] == 0:
            continue
        count = 0
        for j in range(i, len(puzzle)):
            if puzzle[i] > puzzle[j] and puzzle[j] != 0:
                count += 1
        total += count
    return total

def isSolvable(snailPuzzle, size, endDic):

    start = [c for row in snailPuzzle for c in row]
    endSnailPuzzle = [[0 for _ in range(size)] for _ in range(size)]
    for i, pt in endDic.items():
        x, y = pt
        endSnailPuzzle[x][y] = i
    end = [c for row in endSnailPuzzle for c in row]

    startInversions = inversions(start)
    endInversions = inversions(end)

    if size % 2 == 0:
        startInversions += start.index(0) // size
        endInversions += end.index(0) // size

    return startInversions % 2 == endInversions % 2

def main():
    (size, start, end, heuristic) = core.init()

    if not isSolvable(start, size, end):
        print("This puzzle is not solvable")
        sys.exit()

    nSelectedStates, nMaxStates, solution = solve.solve(size, start, end, heuristic)
    nStates, solution = solution
    print("Total number of states ever selected in open set: {:d}".format(nSelectedStates))
    print("Maximum number of states ever represented in memory at the same time: {:d}".format(nMaxStates))
    print("Number of moves required to solve the puzzle: {:d}".format(nStates))
    for state in solution:
        core.display(state)

main()
