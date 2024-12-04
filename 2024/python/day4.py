import os
import sys
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2024/day/4
# Input URL:   https://adventofcode.com/2024/day/4/input

"""
--- Day 4: Ceres Search ---

"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!
As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.
This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:
..X...
.SAMX.
.A..A.
XMAS.S
.X....

The actual word search will be full of letters instead. For example:
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX

In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:
....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX

Take a look at the little Elf's word search. How many times does XMAS appear?
"""


def parse_raw_input(input: str) -> str:
    """
    Returns the raw input stripped of outer whitespace
    """
    return input.strip()


def part1(input: str):
    answer = 0

    row_length = input.index(os.linesep)

    for i, char in enumerate(input):
        if char == os.linesep:
            continue

        # get elements to:
        # - left
        # - right
        # - above
        # - below
        # - diagonal:
        #   - up and left
        #   - up and right
        #   - down and left
        #   - down and right

        pass

    return answer


def part2(input):
    answer = None
    return answer


def main():
    raw_input = utils.get_raw_input()
    # fmt: off
    # raw_input = """"""
    # fmt: on
    parsed_input = parse_raw_input(raw_input)

    utils.handle(part1(parsed_input), 1)
    utils.handle(part2(parsed_input), 2)


if __name__ == "__main__":
    main()
