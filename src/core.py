#!/usr/bin/python3

import sys
import getopt

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
    print('{:s} [-h] [-i <file>]'.format(sys.argv[0]))

def init():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:e:", ["help", "input=", "heuristic="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    puzzle_file = None
    heuristic = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-i", "--input"):
            puzzle_file = arg
        elif opt in ("-e", "--heuristic"):
            heuristic = arg
        else:
            usage()
            sys.exit(1)

    if puzzle_file is None:
        usage()
        sys.exit()

    try:
        (puzzle_size, puzzle) = puzzle_of_file(puzzle_file)
    except Exception as err:
        print(str(err))
        sys.exit()

    return (puzzle_size, puzzle, heuristic)

def display(puzzle):
    s = ''
    for row in puzzle:
        for case in row:
            s += ' {:2d}'.format(case)
        s += '\n'
    print(s)
