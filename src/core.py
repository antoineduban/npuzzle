#!/usr/bin/python3

import sys
import getopt
import random

def getFinalCoords(puzzle_size):
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
    try: 
        del ret[puzzle_size * puzzle_size]
    except:
        pass
    return ret

def findEmpty(puzzle):
    for x, row in enumerate(puzzle):
        for y, case in enumerate(row):
            if case == 0:
                return (x, y)
    return None

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

def randomPuzzle(size):
    end = getFinalCoords(size)

    puzzle = [[int(0) for _ in range(size)] for _ in range(size)]

    for k, v in end.items():
        x, y = v
        puzzle[x][y] = k

    empty = findEmpty(puzzle)
    x, y = empty
    puzzle[x][y] = 0

    print("Puzzle initial")
    print("Empty ", empty)
    display(puzzle)
    for _ in range(1000):
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
    print('{:s} [-h] [-r|-i <file>] [-e euclidian|manhattan|misplaced]'.format(sys.argv[0]))

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
            if heuristic != "manhattan" and heuristic != "euclidian" and heuristic != "misplaced":
                usage()
                sys.exit(1)
        else:
            usage()
            sys.exit(1)

    if puzzle is None:
        usage()
        sys.exit()
    if heuristic == None:
        heuristic = "manhattan"
    end = getFinalCoords(puzzle_size)
    return (puzzle_size, puzzle, end, heuristic)

def display(puzzle):
    s = ''
    for row in puzzle:
        for case in row:
            s += ' {:2d}'.format(case)
        s += '\n'
    print(s)
