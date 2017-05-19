import copy
from blist import *
import time
from collections import defaultdict
import json
import time

from operator import itemgetter

import core

def heuristic2(puzzle_size, puzzle, end):
    finalScore = 0
    for x, row in enumerate(puzzle):
        for y, val in enumerate(row):
            if val != 0:
                xtarget = int((val-1) / puzzle_size)
                ytarget = int((val-1) % puzzle_size)
                finalScore += abs(xtarget - x) + abs(ytarget - y)
    return finalScore

def heuristic(puzzle_size, puzzle, end):
    finalScore = 0
    for x, row in enumerate(puzzle):
        for y, val in enumerate(row):
            if val != 0:
                xtarget = end[val][0]
                ytarget = end[val][1]
                finalScore += abs(xtarget - x) + abs(ytarget - y)
    return finalScore

def getLowestFScore(puzzle_size, openSet, fScore):
    lowest = 1000
    toReturn = None
    for s_json, s in openSet.items():
        if fScore[s_json] < lowest:
            lowest = fScore[s_json]
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

def deepcopy(current):
    l = []
    for i in current:
        l.append(list(i))
    return l

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
            newSet = deepcopy(current)
            newSet[x0][y0] = newSet[x][y]
            newSet[x][y] = 0
            newSets.append(newSet)

    return newSets

def p(puzzle):
    for x, row in enumerate(puzzle):
        print(row)

    print()

def insert(a, x):
    keyfunc = lambda v: v[1]
    lo = 0
    hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if keyfunc(a[mid]) < keyfunc(x):
            lo = mid+1
        else:
            hi = mid
    a.insert(lo, x)


def solve(puzzle_size, start, end):
    p(start)
    start_json = json.dumps(start)

    start_fScore = heuristic(puzzle_size, start, end)

    closedSet = {}
    openSet = blist([(start, start_fScore)])
    openSetHash = {}
    openSetHash[json.dumps(start)] = start
    cameFrom = {}
    gScore = defaultdict(lambda: 9999)
    gScore[start_json] = 0
    fScore = defaultdict(lambda: 9999)
    fScore[start_json] = start_fScore

    while openSet:
        current, h = openSet[0]
        current_json = json.dumps(current)

        if heuristic(puzzle_size, current, end) == 0:

            p(current)
            print(gScore[current_json])
            print("FINISHED")
            return 1

        openSet.pop(0)
        del openSetHash[current_json]
        closedSet[current_json] = current
        for neighbor in getNeighbors(puzzle_size, current):
            neighbor_json = json.dumps(neighbor)
            if neighbor_json in closedSet:
                continue

            tentative_gScore = gScore[current_json] + 1
            if not neighbor_json in openSetHash:
                cameFrom[neighbor_json] = current
                gScore[neighbor_json] = tentative_gScore
                fScore[neighbor_json] = (
                    gScore[neighbor_json] +
                    heuristic(puzzle_size, neighbor, end)
                )
                insert(openSet, (neighbor, fScore[neighbor_json]))
                openSetHash[neighbor_json] = neighbor
            elif tentative_gScore >= gScore[neighbor_json]:
                continue

    print("FAILED")
    return -1
