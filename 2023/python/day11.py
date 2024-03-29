import os
import sys
from pprint import PrettyPrinter
import itertools as it

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2023/day/11
# Input URL:   https://adventofcode.com/2023/day/11/input

"""
--- Day 11: Cosmic Expansion ---

You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.
He doesn't know anything about the missing machine parts; he's only visiting for this research project. However, he confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once he's done with today's observation analysis.
Maybe you can help him with the analysis to speed things up?
The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The image includes empty space (.) and galaxies (#). For example:
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....

The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.
Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.
In the above example, three columns and two rows contain no galaxies:
   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^

These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:
....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......

Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:
....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......

In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)
For example, here is one of the shortest paths between galaxies 5 and 9:
....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......

This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

Between galaxy 1 and galaxy 7: 15
Between galaxy 3 and galaxy 6: 17
Between galaxy 8 and galaxy 9: 5

In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.
Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?

--- Part Two ---

The galaxies are much older (and thus much farther apart) than the researcher initially estimated.

Now, instead of the expansion you did before, make each empty row or column one million times larger. That is, each empty row should be replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 empty columns.

(In the example above, if each empty row or column were merely 10 times larger, the sum of the shortest paths between every pair of galaxies would be 1030. If each empty row or column were merely 100 times larger, the sum of the shortest paths between every pair of galaxies would be 8410. However, your universe will need to expand far beyond these values.)

Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
"""


def parse_raw_input(input: str):
    return input.strip().split("\n")


GALAXY = "#"


def do(input, part: int) -> int:
    answer = 0

    # 999,999 because we want the row/column to be 1,000,000 times larger.
    # So to do that, we add 999,999 rows to the previous row, which results
    # in a total of 1,000,000 rows
    expansion_size = 1 if part == 1 else 999_999

    ### Figure out where the galaxies are ###
    galaxies = []
    for row_i, row in enumerate(input):
        for col_i, value in enumerate(row):
            if value != GALAXY:
                continue
            galaxies.append((row_i, col_i))

    ### Get all combinations of pairs of galaxies ###
    pairs = [x for x in it.combinations(galaxies, 2)]

    ### Figure out which rows and cols are empty ###
    row_length = len(input[0])
    empty_rows = tuple(i for i, row in enumerate(input) if not GALAXY in row)
    empty_cols = tuple(
        i for i in range(row_length) if not GALAXY in (row[i] for row in input)
    )

    ### Calculate the distances between the pairs of galaxies ###
    for galaxy1, galaxy2 in pairs:
        x1, y1 = galaxy1
        x2, y2 = galaxy2

        taxicab_distance = abs(x1 - x2) + abs(y1 - y2)

        ### Figure out how many expansions would have affected this distance

        x_range = range(min(x1, x2) + 1, max(x1, x2))
        y_range = range(min(y1, y2) + 1, max(y1, y2))

        for row_i in empty_rows:
            if not row_i in x_range:
                continue
            taxicab_distance += expansion_size
        for col_i in empty_cols:
            if not col_i in y_range:
                continue
            taxicab_distance += expansion_size

        answer += taxicab_distance

    return answer


def part1(input):
    return do(input, 1)


def part2(input):
    # 742306702870 - too high
    return do(input, 2)


def main():
    raw_input = utils.get_raw_input()
    #     raw_input = """...#......
    # .......#..
    # #.........
    # ..........
    # ......#...
    # .#........
    # .........#
    # ..........
    # .......#..
    # #...#.....
    # """
    parsed_input = parse_raw_input(raw_input)

    utils.handle(part1(parsed_input), 1)  # 9445168 (1.1920928955078125e-06 seconds)
    utils.handle(part2(parsed_input), 2)  # 742305960572 (9.5367431640625e-07 seconds)


if __name__ == "__main__":
    main()
