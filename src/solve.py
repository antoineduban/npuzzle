import copy
import time
from collections import defaultdict
import json
import time
import core

def getFinalCoords(puzzle_size, puzzle):
    nbs = (puzzle_size * puzzle_size) - 1
    
    x = 0
    y = 0
    lim = 0
    ret = {}
    count = 1
    while True:
        while x + 1 < puzzle_size - lim:
            ret[count] = [y,x]
            count += 1
            x += 1
        while y + 1< puzzle_size - lim:
            ret[count] = [y,x]
            count += 1
            y += 1
        while x - 1>= 0 + lim:
            ret[count] = [y,x]
            count += 1
            x -= 1
        while y - 1 >= 0 + lim:
            ret[count] = [y,x]
            count += 1
            y -= 1
        x += 1
        y += 1
        lim += 1
        if x >= puzzle_size - lim and y >= puzzle_size - lim:
                break
    return ret

def heuristic2(puzzle_size, puzzle, coords):
    finalScore = 0
    for x, row in enumerate(puzzle):
        for y, val in enumerate(row):
            if val != 0:
                xtarget = int((val-1) / puzzle_size)
                ytarget = int((val-1) % puzzle_size)
                finalScore += abs(xtarget - x) + abs(ytarget - y)
    return finalScore

def heuristic(puzzle_size, puzzle, coords):
    finalScore = 0
    for x, row in enumerate(puzzle):
        for y, val in enumerate(row):
            if val != 0:
                xtarget = coords[val][0]
                ytarget = coords[val][1]
                finalScore += abs(xtarget - x) + abs(ytarget - y)
    return finalScore

def getLowestFScore(puzzle_size, openSet, fScore):
    lowest = 1000
    toReturn = None
    for s_json, s in openSet.items():
        #h = heuristic(puzzle_size, s)
        #s_json = json.dumps(s)
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
    start_json = json.dumps(start)

    closedSet = {}
    openSet = {}
    openSet[start_json] = start
    cameFrom = {}
    gScore = defaultdict(lambda: 9999)
    gScore[start_json] = 0
    fScore = defaultdict(lambda: 9999)
    coords = getFinalCoords(puzzle_size, start)
    fScore[start_json] = heuristic(puzzle_size, start, coords)

    while openSet:
        current = getLowestFScore(puzzle_size, openSet, fScore)
        current_json = json.dumps(current)

        if heuristic(puzzle_size, current, coords) == 0:
            p(current)
            print("FINISHED")
            return 1
        del openSet[current_json]
        closedSet[current_json] = current
        neighbors = getNeighbors(puzzle_size, current)
        for s in neighbors:
            neighbor_json = json.dumps(s)
            if neighbor_json in closedSet:
                continue

            tentative_gScore = gScore[current_json] + 1
            if neighbor_json not in openSet:
                openSet[neighbor_json] = s
            elif tentative_gScore >= gScore[neighbor_json]:
                continue

            cameFrom[neighbor_json] = current
            gScore[neighbor_json] = tentative_gScore
            fScore[neighbor_json] = gScore[neighbor_json] + heuristic(puzzle_size, s, coords)

    print("FAILED")
    return -1
