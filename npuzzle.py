#!/bin/python3

import sys

sys.path.insert(0, 'src/')

import core
import solve

def main():
    (puzzle_size, puzzle, heuristic) = core.init()
    print('puzzle_size {:d}\n'.format(puzzle_size))

    core.display(puzzle)
    solve.solve(puzzle_size, puzzle)

main()
