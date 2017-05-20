#!/bin/python3

import sys

sys.path.insert(0, 'src/')

import core
import solve

def main():
    (size, start, end, heuristic) = core.init()

    print("======================================")
    #puzzle_size = 5
    #res = [
    #    [  1,  5,  3,  4,  2],
    #    [ 16, 17, 18, 19,  6],
    #    [ 15, 24, 25, 20,  7],
    #    [ 14, 23, 22, 21,  8],
    #    [ 13, 12, 11, 10,  9],
    #]
   #puzzle = [
   #    [ 1, 2, 3],
   #    [ 4, 5, 6],
   #    [ 7, 8, 0]
   #]

    solve.solve(size, start, end, heuristic)
    print("Puzzle solved")

main()
