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
Grid = list[Line]


def parse_raw_input(input: str) -> Grid:
    # input = """
    # ..@@.@@@@.
    # @@@.@.@.@@
    # @@@@@.@.@@
    # @.@@@@..@.
    # @@.@@@@.@@
    # .@@@@@@@.@
    # .@.@.@.@@@
    # @.@@@.@@@@
    # .@@@@@@@@.
    # @.@.@@@.@.
    # """
    return [[char for char in line.strip()] for line in input.strip().split(os.linesep)]


def can_access_roll(grid: Grid, i_line: int, i_space: int) -> bool:
    if grid[i_line][i_space] != ROLL_OF_PAPER:
        return False

    len_grid = len(grid)
    len_line = len(grid[0])

    line_prev = grid[i_line - 1] if i_line - 1 >= 0 else []
    line_here = grid[i_line]
    line_next = grid[i_line + 1] if i_line + 1 < len_grid else []

    i_space_prev = max(i_space - 1, 0)
    i_space_next = min(i_space + 2, len_line)

    line_prev_seg = line_prev[i_space_prev:i_space_next]
    line_here_seg = line_here[i_space_prev:i_space_next]
    line_next_seg = line_next[i_space_prev:i_space_next]

    # remove one @ from line_here_seg as it's the current space and
    # we dont want to account for that
    for i_char, char in enumerate(line_here_seg):
        if char == ROLL_OF_PAPER:
            del line_here_seg[i_char]
            break

    surrounding = line_prev_seg + line_here_seg + line_next_seg

    roll_count = surrounding.count(ROLL_OF_PAPER)

    can_access = roll_count < 4
    return can_access


def part1(grid: Grid) -> int:
    len_grid = len(grid)
    len_line = len(grid[0])
    return sum(
        int(can_access_roll(grid, i_line, i_space))
        for i_space in range(len_line)
        for i_line in range(len_grid)
    )


def part2(grid: Grid) -> int:
    answer = None
    return answer


def main():
    utils.handle(part1)  # 1505 (0.014733076095581055 seconds)
    utils.handle(part2)


if __name__ == "__main__":
    main()
