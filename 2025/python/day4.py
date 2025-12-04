import os
import sys
from typing import Literal
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2025/day/4
# Input URL:   https://adventofcode.com/2025/day/4/input

ROLL_OF_PAPER = "@"
EMPTY_SPACE = "."

Space = Literal[ROLL_OF_PAPER, EMPTY_SPACE]
Line = list[Space]
Input = list[Line]


def parse_raw_input(input: str) -> Input:
    input = """
    ..@@.@@@@.
    @@@.@.@.@@
    @@@@@.@.@@
    @.@@@@..@.
    @@.@@@@.@@
    .@@@@@@@.@
    .@.@.@.@@@
    @.@@@.@@@@
    .@@@@@@@@.
    @.@.@@@.@.
    """
    return [[char for char in line.strip()] for line in input.strip().split(os.linesep)]


def part1(input: Input) -> int:
    answer = None
    return answer


def part2(input: Input) -> int:
    answer = None
    return answer


def main():
    utils.handle(part1)
    utils.handle(part2)


if __name__ == "__main__":
    main()
