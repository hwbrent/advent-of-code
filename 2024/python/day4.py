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


def parse_raw_input(input: str) -> list[str]:
    """
    Returns the raw input stripped of outer whitespace and split into lines
    """
    return input.strip().split(os.linesep)


def part1(input: str):
    answer = 0

    row_length = len(input[0])  # the number of columns (values in each row)
    row_count = len(input)  # the number of rows in the input

    for row_i, row in enumerate(input):
        for col_i, char in enumerate(row):
            if char == os.linesep:
                continue

            # get chars to:
            directions = [
                "",  # left
                "",  # right
                "",  # up
                "",  # down
                # diagonal:
                "",  # up & left
                "",  # up & right
                "",  # down & left
                "",  # down & right
            ]

            # get left
            left_index = col_i
            # move left until we hit the third neighbouring letter, or the
            # edge of the row
            while left_index >= 0 and left_index > col_i - 4:
                directions[0] += row[left_index]
                left_index -= 1

            # get right
            right_index = col_i
            # move right until we hit the third neighbouring letter, or the
            # edge of the row
            while right_index < row_length and right_index < col_i + 4:
                directions[1] += row[right_index]
                right_index += 1

            # get up
            up_index = row_i
            # move up until we hit the third neighbouring letter, or the
            # top row
            while up_index >= 0 and up_index > row_i - 4:
                directions[2] += input[up_index][col_i]
                up_index -= 1

            # get down
            down_index = row_i
            # move down until we hit the third neighbouring letter, or the
            # bottom row
            while down_index < row_count and down_index < row_i + 4:
                directions[3] += input[down_index][col_i]
                down_index += 1

            # get up & left
            up_left_index = (row_i, col_i)
            # move up & left until we hit the third neighbouring letter, or the
            # top row or left edge
            while (
                up_left_index[0] >= 0
                and up_left_index[0] > row_i - 4
                and up_left_index[1] >= 0
                and up_left_index[1] > col_i - 4
            ):
                directions[4] += input[up_left_index[0]][up_left_index[1]]
                up_left_index = (up_left_index[0] - 1, up_left_index[1] - 1)

            # get up & right
            up_index = row_i
            right_index = col_i
            while (
                up_index >= 0
                and up_index > row_i - 4
                and right_index < row_length
                and right_index < col_i + 4
            ):
                directions[5] += input[up_index][right_index]
                up_index -= 1
                right_index += 1

            # get down & left
            down_index = row_i
            left_index = col_i
            while (
                down_index < row_count
                and down_index < row_i + 4
                and left_index >= 0
                and left_index > col_i - 4
            ):
                directions[6] += input[down_index][left_index]
                down_index += 1
                left_index -= 1

            # get down & right
            down_index = row_i
            right_index = col_i
            while (
                down_index < row_count
                and down_index < row_i + 4
                and right_index < row_length
                and right_index < col_i + 4
            ):
                directions[7] += input[down_index][right_index]
                down_index += 1
                right_index += 1

            for direction in directions:
                if direction != "XMAS":
                    continue
                answer += 1

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
