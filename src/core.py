#!/usr/bin/python3

import sys
import getopt
import random

# Random puzzle gen
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

def randomPuzzle(size):
    puzzle, empty = endPuzzle(size)
    print("Puzzle initial")
    display(puzzle)
    for i in range(1000):
        puzzle, empty = randSwapEmpty(puzzle, size, empty)
    #     display(puzzle)
    print("Puzzle mixed")
    display(puzzle)
    return puzzle

# Puzzle of file
def puzzle_of_file(filename):
    puzzle_size = 0
    puzzle = []

    fpuzzle = open(filename, "r")

    for fline in fpuzzle:
        if fline[0] == '#':
            continue

        if puzzle_size == 0:
            puzzle_size = int(fline)
            if puzzle_size <= 0 or puzzle_size > 99: # Change display if more
                raise Exception("puzzle_size " + str(puzzle_size))
        else:
            puzzle_line = [int(x) for x in fline.split()]
            if len(puzzle_line) != puzzle_size:
                raise Exception("puzzle_line " + str(puzzle_line))
            puzzle += [puzzle_line]

    fpuzzle.close()

    if len(puzzle) != puzzle_size:
        raise Exception("Invalid number of line")

    return (puzzle_size, puzzle)

def usage():
    print('{:s} [-h] [-r|-i <file>]'.format(sys.argv[0]))

def init():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hr:i:e:", ["rand", "help", "input=", "heuristic="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    puzzle_size = 0
    puzzle = None
    heuristic = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-i", "--input"):
            if puzzle_size != 0:
                usage()
                sys.exit()
            try:
                puzzle_size, puzzle = puzzle_of_file(arg)
            except Exception as err:
                print(str(err))
                sys.exit()
        elif opt in ("-r", "--rand"):
            if puzzle_size != 0:
                usage()
                sys.exit()
            try:
                puzzle_size = int(arg)
            except Exception as err:
                print(str(err))
                sys.exit()
            puzzle = randomPuzzle(puzzle_size)
        elif opt in ("-e", "--heuristic"):
            heuristic = arg
        else:
            usage()
            sys.exit(1)

    if puzzle is None:
        usage()
        sys.exit()

    return (puzzle_size, puzzle, heuristic)

def display(puzzle):
    s = ''
    for row in puzzle:
        for case in row:
            s += ' {:2d}'.format(case)
        s += '\n'
    print(s)
