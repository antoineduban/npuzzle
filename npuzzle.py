#!/bin/python3

import sys
import random
import time

sys.path.insert(0, 'src/')

import core
import solve

def isValid(p, puzzle_size):
    x, y = p
    return (x >= 0 and x < puzzle_size
        and y >= 0 and y < puzzle_size)

def randMove(p, puzzle_size):
    x0, y0 = p
    x = 0
    y = 0
    while not (isValid((x0+x, y0+y), puzzle_size)
        and ((x == 0 and y != 0) or (x != 0 and y == 0))):
        x = random.randint(-1, 1)
        y = random.randint(-1, 1)
    return (x0+x, y0+y)

def randSwapEmpty(puzzle, puzzle_size, empty):
    x0, y0 = empty
    x1, y1 = randMove(empty, puzzle_size)
    puzzle[x0][y0] = puzzle[x1][y1]
    puzzle[x1][y1] = 0
    return (puzzle, (x1, y1))

def endPuzzle(size):
    res = [ [(i+1)+(j*size) for i in range (size)] for j in range (size) ]
    res[size-1][size-1] = 0
    empty = (size-1, size-1)
    return (res, empty)

def main():
    (puzzle_size, puzzle, heuristic) = core.init()

    print("======================================")
    #puzzle_size = 5
    #res = [
    #    [  1,  5,  3,  4,  2],
    #    [ 16, 17, 18, 19,  6],
    #    [ 15, 24, 25, 20,  7],
    #    [ 14, 23, 22, 21,  8],
    #    [ 13, 12, 11, 10,  9],
    #]
    puzzle, empty = endPuzzle(puzzle_size)
    print("Puzzle initial")
    core.display(puzzle)
    for i in range(1000):
        puzzle, empty = randSwapEmpty(puzzle, puzzle_size, empty)
    #     core.display(puzzle)
    print("Puzzle mixed")
    core.display(puzzle)

    solve.solve(puzzle_size, puzzle)
    print("Puzzle solved")
    core.display(puzzle)

main()
