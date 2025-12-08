import os
import sys
import math
from numbers import Number
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
        tuple([int(num) for num in line.strip().split(",")])
        for line in input.strip().split(os.linesep)
    ]


def get_distance(box1: JunctionBox, box2: JunctionBox) -> float:
    # see: https://www.geeksforgeeks.org/maths/3d-distance-formula/
    x1, y1, z1 = box1
    x2, y2, z2 = box2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def part1(junction_boxes: JunctionBoxes) -> int:
    answer = 0

    distances: dict[JunctionBox, dict[JunctionBox, float]] = {}

    # calculate distance between every pair of
    for box1 in junction_boxes:
        for box2 in junction_boxes:
            if box1 == box2:
                continue

            if not box1 in distances:
                distances[box1] = {}

            if not box2 in distances:
                distances[box2] = {}

            rev_distance = distances[box2].get(box1)

            distance = (
                rev_distance
                if isinstance(rev_distance, Number)
                else get_distance(box1, box2)
            )

            distances[box1][box2] = distance
            distances[box2][box1] = distance

    pp.pprint(distances)

    return answer


def part2(junction_boxes: JunctionBoxes) -> int:
    answer = 0
    return answer


def main():
    utils.handle(part1)
    utils.handle(part2)


if __name__ == "__main__":
    main()
