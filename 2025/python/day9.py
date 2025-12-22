import os
import sys
from typing import Any
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2025/day/9
# Input URL:   https://adventofcode.com/2025/day/9/input


NumRow = int
NumCol = int

Tile = list[NumRow, NumCol]
Tiles = list[Tile]


def parse_raw_input(input: str) -> Tiles:
    input = """
    7,1
    11,1
    11,7
    9,7
    9,5
    2,5
    2,3
    7,3
    """
    return [
        [int(num) for num in line.strip().split(",")]
        for line in input.strip().split(os.linesep)
    ]


def part1(tiles: Tiles) -> int:
    answer = 0
    print(tiles)
    return answer


def part2(tiles: Tiles) -> int:
    answer = 0
    return answer


def main():
    utils.handle(part1)
    utils.handle(part2)


if __name__ == "__main__":
    main()
