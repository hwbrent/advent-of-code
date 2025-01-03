import os
import sys
import copy
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2024/day/10
# Input URL:   https://adventofcode.com/2024/day/10/input

"""
--- Day 10: Hoof It ---

You all arrive at a Lava Production Facility on a floating island in the sky. As the others begin to search the massive industrial complex, you feel a small nose boop your leg and look down to discover a reindeer wearing a hard hat.
The reindeer is holding a book titled "Lava Island Hiking Guide". However, when you open the book, you discover that most of it seems to have been scorched by lava! As you're about to ask how you can help, the reindeer brings you a blank topographic map of the surrounding area (your puzzle input) and looks up at you excitedly.
Perhaps you can help fill in the missing hiking trails?
The topographic map indicates the height at each position using a scale from 0 (lowest) to 9 (highest). For example:
0123
1234
8765
9876

Based on un-scorched scraps of the book, you determine that a good hiking trail is as long as possible and has an even, gradual, uphill slope. For all practical purposes, this means that a hiking trail is any path that starts at height 0, ends at height 9, and always increases by a height of exactly 1 at each step. Hiking trails never include diagonal steps - only up, down, left, or right (from the perspective of the map).
You look up from the map and notice that the reindeer has helpfully begun to construct a small pile of pencils, markers, rulers, compasses, stickers, and other equipment you might need to update the map with hiking trails.
A trailhead is any position that starts one or more hiking trails - here, these positions will always have height 0. Assembling more fragments of pages, you establish that a trailhead's score is the number of 9-height positions reachable from that trailhead via a hiking trail. In the above example, the single trailhead in the top left corner has a score of 1 because it can reach a single 9 (the one in the bottom left).
This trailhead has a score of 2:
...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9

(The positions marked . are impassable tiles to simplify these examples; they do not appear on your actual topographic map.)
This trailhead has a score of 4 because every 9 is reachable via a hiking trail except the one immediately to the left of the trailhead:
..90..9
...1.98
...2..7
6543456
765.987
876....
987....

This topographic map contains two trailheads; the trailhead at the top has a score of 1, while the trailhead at the bottom has a score of 2:
10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01

Here's a larger example:
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732

This larger example has 9 trailheads. Considering the trailheads in reading order, they have scores of 5, 6, 5, 3, 1, 3, 5, 3, and 5. Adding these scores together, the sum of the scores of all trailheads is 36.
The reindeer gleefully carries over a protractor and adds it to the pile. What is the sum of the scores of all trailheads on your topographic map?
"""


def parse_raw_input(input: str):
    return [
        [int(char) for char in row.strip()] for row in input.strip().split(os.linesep)
    ]


def get_trailheads(input) -> list[tuple]:
    """
    Returns a list of the coordinates of trailheads (zeros)
    """
    coords = []
    for row_i, row in enumerate(input):
        for col_i, num in enumerate(row):
            if num != 0:
                continue
            coord = (row_i, col_i)
            coords.append(coord)
    return coords


def get_above(coord) -> tuple[int, int]:
    """
    Gets the coordinate above `coord`
    """
    row, col = coord
    return (row - 1, col)


def get_below(coord) -> tuple[int, int]:
    """
    Gets the coordinate below `coord`
    """
    row, col = coord
    return (row + 1, col)


def get_left(coord) -> tuple[int, int]:
    """
    Gets the coordinate left of `coord`
    """
    row, col = coord
    return (row, col - 1)


def get_right(coord) -> tuple[int, int]:
    """
    Gets the coordinate right of `coord`
    """
    row, col = coord
    return (row, col + 1)


def get_num(coord, input) -> int:
    """
    Get the numeric value at the given `coord`
    """
    row, col = coord
    return input[row][col]


def in_range(coord, rows, cols) -> bool:
    """
    Returns a `bool` indicating whether the given `coord` is within the
    bounds of the input
    """
    row, col = coord
    return row in range(rows) and col in range(cols)


def visualise_trail(trail, input) -> None:
    """
    Prints `input` with the values corresponding to the coordinates in
    `trail` highlighted
    """
    # create a copy of the input to amend
    vis = copy.deepcopy(input)

    # for each row/col coordinate in 'trail', grab the value, and make it
    # green
    for coord in trail:
        row, col = coord
        # see: https://stackoverflow.com/a/287944
        vis[row][col] = "\033[92m" + str(vis[row][col]) + "\033[0m"

    # turn the 2d-list input into a string, and print it
    vis = os.linesep.join("".join(str(char) for char in row) for row in vis)
    print(os.linesep + vis + os.linesep)


def part1(input):
    rows = len(input)
    cols = len(input[0])

    trailheads = get_trailheads(input)

    # The unique 9-height positions reachable from each trailhead
    trailends = {trailhead: set() for trailhead in trailheads}

    def recurse(coord, head, trail=[]):
        trail = trail + [coord]

        # figure out the number of the current pos
        current_num = get_num(coord, input)

        # if we've reached the end of a trail, record the fact that this
        # 9 can be reached via this trailhead
        if current_num == 9:
            trailends[head].add(coord)
            # visualise_trail(trail, input)
            return

        # otherwise, continue moving along the trail

        # figure out the next number to move onto
        next_num = current_num + 1

        # get the surrounding coords
        surrounding = (
            get_above(coord),
            get_below(coord),
            get_left(coord),
            get_right(coord),
        )

        # figure out which of the surrounding coords can be moved to
        eligible = (
            entry
            for entry in surrounding
            if in_range(entry, rows, cols) and get_num(entry, input) == next_num
        )

        # recurse on the eligible surrounding coords
        for entry in eligible:
            recurse(entry, head, trail)

    # start recursing on the trailheads
    for head in trailheads:
        recurse(head, head)

    # add up the number of 9-height positions reachable from each trailhead
    answer = 0
    for heads in trailends.values():
        answer += len(heads)
    return answer


def part2(input):
    rows = len(input)
    cols = len(input[0])

    trailheads = get_trailheads(input)

    # for some reason i can't just use an integer here - 'recurse' can't access
    # it. so i have to use a list ???
    answer = [0]

    def recurse(coord, head, trail=[]):

        trail = trail + [coord]

        # figure out the number of the current pos
        current_num = get_num(coord, input)

        # if we've reached the end of a trail, increment the answer
        if current_num == 9:
            answer[0] += 1
            # visualise_trail(trail, input)
            return

        # otherwise, continue moving along the trail

        # figure out the next number to move onto
        next_num = current_num + 1

        # get the surrounding coords
        surrounding = (
            get_above(coord),
            get_below(coord),
            get_left(coord),
            get_right(coord),
        )

        # figure out which of the surrounding coords can be moved to
        eligible = (
            entry
            for entry in surrounding
            if in_range(entry, rows, cols) and get_num(entry, input) == next_num
        )

        # recurse on the eligible surrounding coords
        for entry in eligible:
            recurse(entry, head, trail)

    # start recursing on the trailheads
    for head in trailheads:
        recurse(head, head)

    return answer[0]


def main():
    utils.handle(
        part1,
        # """
        # 89010123
        # 78121874
        # 87430965
        # 96549874
        # 45678903
        # 32019012
        # 01329801
        # 10456732
        # """,
    )  # 459 (0.013190269470214844 seconds)
    utils.handle(part2)  # 1034 (0.012137889862060547 seconds)


if __name__ == "__main__":
    main()
