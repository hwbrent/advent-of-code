import os
import sys
from pprint import PrettyPrinter
import itertools as it

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2023/day/14
# Input URL:   https://adventofcode.com/2023/day/14/input

"""
--- Day 14: Parabolic Reflector Dish ---

You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish attached to the side of another large mountain.
The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the shape of a parabolic reflector dish, each individual mirror seems to be pointing in slightly the wrong direction. If the dish is meant to focus light, all it's doing right now is sending it in a vague direction.
This system must be what provides the energy for the lava! If you focus the reflector dish, maybe you can go where it's pointing and use the light to fix the lava production.
Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes and pulleys to a large metal platform below the dish. The platform is covered in large rocks of various shapes. Depending on their position, the weight of the rocks deforms the platform, and the shape of the platform controls which ropes move and ultimately the focus of the dish.
In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets you tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while the cube-shaped rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks (your puzzle input). For example:
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....

Start by tilting the lever so all of the rocks will slide north as far as they will go:
OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....

You notice that the support beams along the north side of the platform are damaged; to ensure the platform doesn't collapse, you should calculate the total load on the north support beams.
The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the amount of load caused by each rock in each row is as follows:
OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1

The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.
Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support beams?
"""


def parse_raw_input(input: str):
    input = input.strip().split("\n")

    col_length = len(input[0])
    cols = [[row[i] for row in input] for i in range(col_length)]

    return cols


def part1(input):
    answer = 0

    height = len(input)

    for col in input:
        cubes = [i for i, value in enumerate(col) if value == "#"]

        # Prepend -1 to make it easier to get the section between the bottom
        # of the column and the first cube
        cubes.insert(0, -1)

        # Add last index of column to make sure that we account for the
        # section between the last cube and the end of the column
        cubes.append(height)

        for pair in it.pairwise(cubes):
            lower_index, upper_index = pair

            section = col[lower_index + 1 : upper_index]
            # print(section)

            rounded_count = section.count("O")
            if rounded_count == 0:
                continue

            cube_height = height - lower_index

            while rounded_count != 0:
                answer += cube_height - rounded_count
                rounded_count -= 1

        # print()

    # 115592 (too high)
    return answer


def part2(input):
    answer = None
    return answer


def main():
    raw_input = utils.get_raw_input()
    # fmt: off
    raw_input = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
    # fmt: on
    parsed_input = parse_raw_input(raw_input)

    utils.handle(part1(parsed_input), 1)
    utils.handle(part2(parsed_input), 2)


if __name__ == "__main__":
    main()
