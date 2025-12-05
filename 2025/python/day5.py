import os
import sys
from typing import Any
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2025/day/5
# Input URL:   https://adventofcode.com/2025/day/5/input

FreshIdRange = list[int, int]
FreshIdRanges = list[FreshIdRange]

AvailableId = int
AvailableIds = list[AvailableId]

Input = tuple[FreshIdRanges, AvailableIds]


def parse_raw_input(input: str) -> Input:
    input = """
    3-5
    10-14
    16-20
    12-18

    1
    5
    8
    11
    17
    32
    """

    fresh_id_ranges, available_ids = input.strip().split(2 * os.linesep)

    fresh_id_ranges = [
        [int(num) for num in line.strip().split("-")]
        for line in fresh_id_ranges.strip().split(os.linesep)
    ]

    available_ids = [int(num.strip()) for num in available_ids.split(os.linesep)]

    return fresh_id_ranges, available_ids


def part1(input: Input) -> int:
    answer = None
    print(input)
    return answer


def part2(input: Input) -> int:
    answer = None
    return answer


def main():
    utils.handle(part1)
    utils.handle(part2)


if __name__ == "__main__":
    main()
