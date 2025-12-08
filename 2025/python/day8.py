import os
import sys
from typing import Any
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2025/day/8
# Input URL:   https://adventofcode.com/2025/day/8/input


X = int
Y = int
Z = int
JunctionBox = tuple[X, Y, Z]
JunctionBoxes = list[JunctionBox]


def parse_raw_input(input: str) -> JunctionBoxes:
    input = """
    162,817,812
    57,618,57
    906,360,560
    592,479,940
    352,342,300
    466,668,158
    542,29,236
    431,825,988
    739,650,466
    52,470,668
    216,146,977
    819,987,18
    117,168,530
    805,96,715
    346,949,466
    970,615,88
    941,993,340
    862,61,35
    984,92,344
    425,690,689
    """
    return [
        [int(num) for num in line.strip().split(",")]
        for line in input.strip().split(os.linesep)
    ]


def part1(junction_boxes: JunctionBoxes) -> int:
    answer = 0
    print(junction_boxes)
    return answer


def part2(junction_boxes: JunctionBoxes) -> int:
    answer = 0
    return answer


def main():
    utils.handle(part1)
    utils.handle(part2)


if __name__ == "__main__":
    main()
