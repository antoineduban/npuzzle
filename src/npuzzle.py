#!/bin/python3

import core

def main():
    (puzzle_size, puzzle, heuristic) = core.init()
    print('puzzle_size {:d}\n'.format(puzzle_size))
    core.display(puzzle)

main()
