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
    # input = """
    # .......S.......
    # ...............
    # .......^.......
    # ...............
    # ......^.^......
    # ...............
    # .....^.^.^.....
    # ...............
    # ....^.^...^....
    # ...............
    # ...^.^...^.^...
    # ...............
    # ..^...^.....^..
    # ...............
    # .^.^.^.^.^...^.
    # ...............
    # """
    return [[value for value in row.strip()] for row in input.strip().split(os.linesep)]


def mark_position(manifold, row, col):
    if manifold[row][col] == EMPTY_SPACE:
        manifold[row][col] = BEAM


def part1(manifold: Manifold) -> int:
    answer = 0

    pos_start = next(
        [i_row, i_col]  # needs to be mutable
        for i_row, row in enumerate(manifold)
        for i_col, value in enumerate(row)
        if value == START
    )

    beams = [pos_start]

    while len(beams) > 0:

        # iterate over the beams
        i_beam = 0
        while i_beam < len(beams):
            beam = beams[i_beam]
            row, col = beam

            mark_position(manifold, row, col)

            space = manifold[row][col]

            # if the beam is currently on a splitter
            if space == SPLITTER:
                left_beam = [row, col - 1]
                right_beam = [row, col + 1]

                # account for duplicate, overlapping beams

                if left_beam in beams:
                    del beams[i_beam]
                else:
                    # repurpose the current beam, which is on the splitter,
                    # into the left beam
                    beams[i_beam] = left_beam

                # if we don't already have a beam where the right beam would
                # be, add it
                if not right_beam in beams:
                    beams.append(right_beam)

                answer += 1

            # if the beam is currently on the bottom row
            if row == len(manifold) - 1:
                # it's done moving, so remove it
                del beams[i_beam]
                continue

            # move the current beam down
            beam[0] += 1

            i_beam += 1

        print(os.linesep)
        for row in manifold:
            print(*row)
        print(os.linesep)

    return answer


def part2(manifold: Manifold) -> int:
    answer = 0
    return answer


def main():
    utils.handle(part1)
    utils.handle(part2)


if __name__ == "__main__":
    main()
