import os
import sys
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2023/day/16
# Input URL:   https://adventofcode.com/2023/day/16/input

"""
--- Day 16: The Floor Will Be Lava ---

With the beam of light completely focused somewhere, the reindeer leads you deeper still into the Lava Production Facility. At some point, you realize that the steel facility walls have been replaced with cave, and the doorways are just cave, and the floor is cave, and you're pretty sure this is actually just a giant cave.
Finally, as you approach what must be the heart of the mountain, you see a bright light in a cavern up ahead. There, you discover that the beam of light you so carefully focused is emerging from the cavern wall closest to the facility and pouring all of its energy into a contraption on the opposite side.
Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid containing empty space (.), mirrors (/ and \), and splitters (| and -).
The contraption is aligned so that most of the beam bounces around the grid, but each tile on the grid converts some of the beam's light into heat to melt the rock in the cavern.
You note the layout of the contraption (your puzzle input). For example:
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....

The beam enters in the top-left corner from the left and heading to the right. Then, its behavior depends on what it encounters as it moves:

If the beam encounters empty space (.), it continues in the same direction.
If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the angle of the mirror. For instance, a rightward-moving beam that encounters a / mirror would continue upward in the mirror's column, while a rightward-moving beam that encounters a \ mirror would continue downward from the mirror's column.
If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter as if the splitter were empty space. For instance, a rightward-moving beam that encounters a - splitter would continue in the same direction.
If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams going in each of the two directions the splitter's pointy ends are pointing. For instance, a rightward-moving beam that encounters a | splitter would split into two beams: one that continues upward from the splitter's column and one that continues downward from the splitter's column.

Beams do not interact with other beams; a tile can have many beams passing through it at the same time. A tile is energized if that tile has at least one beam pass through it, reflect in it, or split in it.
In the above example, here is how the beam of light bounces around the contraption:
>|<<<\....
|v-.\^....
.v...|->>>
.v...v^.|.
.v...v^...
.v...v^..\
.v../2\\..
<->-/vv|..
.|<<<2-|.\
.v//.|.v..

Beams are only shown on empty tiles; arrows indicate the direction of the beams. If a tile contains beams moving in multiple directions, the number of distinct directions is shown instead. Here is the same diagram but instead only showing whether a tile is energized (#) or not (.):
######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..

Ultimately, in this example, 46 tiles become energized.
The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start by analyzing the current situation. With the beam starting in the top-left heading right, how many tiles end up being energized?
"""


def parse_raw_input(input: str):
    return input.strip().split("\n")


# Directions:
UP = [-1, 0]
DOWN = [1, 0]
LEFT = [0, -1]
RIGHT = [0, 1]


def part1(input):
    answer = None

    min_row = 0
    max_row = len(input[0]) - 1
    min_col = 0
    max_col = len(input) - 1

    beams = [
        {"coord": [0, 0], "direction": RIGHT},
    ]

    for beam in beams:
        ### Move the beam
        direction_row, direction_col = beam["direction"]
        beam["coord"][0] += direction_row
        beam["coord"][1] += direction_col

        coord_row, coord_col = beam["coord"]

        # Check if the beam is still in the area
        if (not (min_row <= coord_row <= max_row)) or (
            not (min_col <= coord_col <= max_col)
        ):
            beams.remove(beam)

        ### Check what the beam has collided with
        tile = input[coord_row][coord_col]

        match tile:
            case ".":
                continue
            case "/":
                continue
            case "\\":
                continue
            case "|":
                continue
            case "-":
                continue
            case _:
                continue

    return answer


def part2(input):
    answer = None
    return answer


def main():
    raw_input = utils.get_raw_input()
    # fmt: off
    raw_input = """
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
    # fmt: on
    parsed_input = parse_raw_input(raw_input)

    utils.handle(part1(parsed_input), 1)
    utils.handle(part2(parsed_input), 2)


if __name__ == "__main__":
    main()
