import os
import sys
from typing import Literal
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2025/day/7
# Input URL:   https://adventofcode.com/2025/day/7/input


START = "S"
SPLITTER = "^"
EMPTY_SPACE = "."
BEAM = "|"


Space = Literal[START, SPLITTER, EMPTY_SPACE]
Row = list[Space]
Manifold = list[Row]


def parse_raw_input(input: str) -> Manifold:
    input = """
    .......S.......
    ...............
    .......^.......
    ...............
    ......^.^......
    ...............
    .....^.^.^.....
    ...............
    ....^.^...^....
    ...............
    ...^.^...^.^...
    ...............
    ..^...^.....^..
    ...............
    .^.^.^.^.^...^.
    ...............
    """
    return [[value for value in row.strip()] for row in input.strip().split(os.linesep)]


def part1(manifold: Manifold) -> int:
    answer = 0
    # print(manifold)

    # splitters that the beam gets split on
    split_on = []

    splitters = [
        (i_row, i_col)
        for i_row, row in enumerate(manifold)
        for i_col, value in enumerate(row)
        if value == SPLITTER
    ]

    for splitter in splitters:
        # the beam will be split on this splitter if:
        # 1. the splitter is directly under S (with no other splitter in
        #    between)
        # 2. the splitter is directly down and one space to the left/right
        #    of another splitter which the beam is split on
        pass

    # print(splitters)

    return answer


def part2(manifold: Manifold) -> int:
    answer = 0
    return answer


def main():
    utils.handle(part1)
    utils.handle(part2)


if __name__ == "__main__":
    main()
