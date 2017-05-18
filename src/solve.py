import copy
import time
from collections import defaultdict
import json

WIDTH = 3


def heuristic(puzzle):
    finalScore = 0
    for x, row in enumerate(puzzle):
        for y, val in enumerate(row):
            if (val != 0):
                xtarget = int((val-1) / WIDTH)
                ytarget = int((val-1) % WIDTH)
                finalScore += abs(xtarget - x) + abs(ytarget - y)
    return finalScore

def getLowestFScore(openSet):
    lowest = 1000
    toReturn = None
    for s in openSet:
        if heuristic(s) < lowest:
            lowest = heuristic(s)
            toReturn = s
    return toReturn
        
def getNeighbors(current):
    xcoord = -1
    ycoord = -1
    newSets = []
    for x, row in enumerate(current):
        for y, val in enumerate(row):
            if val == 0:
                xcoord = x
                ycoord = y
                break
        if xcoord != -1:
            break
    if (xcoord + 1 < WIDTH): 
        newSet = copy.deepcopy(current)
        newSet[xcoord][ycoord] = newSet[xcoord + 1][ycoord]
        newSet[xcoord + 1][ycoord] = 0
        newSets.append(newSet)
    if (xcoord - 1 >= 0): 
        newSet = copy.deepcopy(current)
        newSet[xcoord][ycoord] = newSet[xcoord - 1][ycoord]
        newSet[xcoord - 1][ycoord] = 0
        newSets.append(newSet)
    if (ycoord + 1 < WIDTH): 
        newSet = copy.deepcopy(current)
        newSet[xcoord][ycoord] = newSet[xcoord][ycoord + 1]
        newSet[xcoord][ycoord + 1] = 0
        newSets.append(newSet)
    if (ycoord - 1 >= 0): 
        newSet = copy.deepcopy(current)
        newSet[xcoord][ycoord] = newSet[xcoord][ycoord - 1]
        newSet[xcoord][ycoord - 1] = 0
        newSets.append(newSet)
    return newSets

def p(puzzle):
    for x, row in enumerate(puzzle):
        print(row)

    print()


def solve(start):
    closedSet = []
    openSet = [start]
    cameFrom = {}
    gScore = defaultdict(lambda: 9999)
    gScore[json.dumps(start)] = 0
    fScore = defaultdict(lambda: 9999)
    fScore[json.dumps(start)] = heuristic(start)

    while openSet:
        current = getLowestFScore(openSet)
        if heuristic(current) == 0:
            print(current)
            print("FINISHED")
            return 1
        openSet.remove(current)
        closedSet.append(current)
        neighbors = getNeighbors(current)
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
            fScore[json.dumps(s)] = gScore[json.dumps(s)] + heuristic(s)

    print("FAILED")
    return -1
