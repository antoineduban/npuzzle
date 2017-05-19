import copy
import time
from collections import defaultdict
import json
import time
import core

def manhattan(puzzle_size, puzzle):
    nbs = (puzzle_size * puzzle_size) - 1


    x = 0
    y = 0

def heuristic(puzzle_size, puzzle):
    finalScore = 0
#    manhattan(puzzle_size, puzzle)
    for x, row in enumerate(puzzle):
        for y, val in enumerate(row):
            if val != 0:
                xtarget = int((val-1) / puzzle_size)
                ytarget = int((val-1) % puzzle_size)
                finalScore += abs(xtarget - x) + abs(ytarget - y)
    return finalScore

def getLowestFScore(puzzle_size, openSet, fScore):
    lowest = 1000
    toReturn = None
    for s in openSet:
        #h = heuristic(puzzle_size, s)
        s_json = json.dumps(s)
        if fScore[s_json] < lowest:
        #if h < lowest:
            lowest = fScore[s_json]
            #lowest = h
            toReturn = s
    return toReturn

def isValid(x, y, puzzle_size):
    return (x >= 0 and x < puzzle_size
        and y >= 0 and y < puzzle_size)

def findEmptyCase(puzzle):
    for x, row in enumerate(puzzle):
        for y, case in enumerate(row):
            if case == 0:
                return (x, y)
    return None

def getNeighbors(puzzle_size, current):
    x0, y0 = findEmptyCase(current)

    tests = [
        (x0 + 1, y0),
        (x0 - 1, y0),
        (x0, y0 + 1),
        (x0, y0 - 1)
    ]

    newSets = []
    for test in tests:
        x, y = test
        if isValid(x, y, puzzle_size):
            newSet = copy.deepcopy(current)
            newSet[x0][y0] = newSet[x][y]
            newSet[x][y] = 0
            newSets.append(newSet)

    return newSets

def p(puzzle):
    for x, row in enumerate(puzzle):
        print(row)

    print()

def solve(puzzle_size, start):
    closedSet = []
    openSet = [start]
    cameFrom = {}
    gScore = defaultdict(lambda: 9999)
    gScore[json.dumps(start)] = 0
    fScore = defaultdict(lambda: 9999)
    fScore[json.dumps(start)] = heuristic(puzzle_size, start)

    while openSet:
        current = getLowestFScore(puzzle_size, openSet, fScore)
        if heuristic(puzzle_size, current) == 0:
            p(current)
            print("FINISHED")
            return 1
        openSet.remove(current)
        closedSet.append(current)
        neighbors = getNeighbors(puzzle_size, current)
        for s in neighbors:
            if s in closedSet:
                continue
            tentative_gScore = gScore[json.dumps(current)] + 1
            if s not in openSet:
                openSet.append(s)
            elif tentative_gScore >= gScore[json.dumps(s)]:
                continue
            cameFrom[json.dumps(s)] = current
            gScore[json.dumps(s)] = tentative_gScore
            fScore[json.dumps(s)] = gScore[json.dumps(s)] + heuristic(puzzle_size, s)

    print("FAILED")
    return -1
