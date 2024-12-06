import os
import sys
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2024/day/6
# Input URL:   https://adventofcode.com/2024/day/6/input

"""
--- Day 6: Guard Gallivant ---

The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype suit manufacturing lab... in the year 1518! It turns out that having direct access to history is very convenient for a group of historians.
You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the lab.
Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?
You start by making a map (your puzzle input) of the situation. For example:
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...

The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.
Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

If there is something directly in front of you, turn right 90 degrees.
Otherwise, take a step forward.

Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):
....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:
....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:
....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...

This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):
....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..

By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:
....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..

In this example, the guard will visit 41 distinct positions on your map.
Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?
"""

Input = list[list[str]]


def parse_raw_input(input: str) -> Input:
    return [[char for char in line] for line in input.strip().split(os.linesep)]


CARET = "^"
OBSTACLE = "#"


# fmt: off
# row direction, column direction
UP    = (-1,  0)
DOWN  = ( 1,  0)
LEFT  = ( 0, -1)
RIGHT = ( 0,  1)
# fmt: on


def move(position, direction) -> tuple[int, int]:
    return (
        position[0] + direction[0],
        position[1] + direction[1],
    )


def turn(direction) -> tuple[int, int]:
    if direction == UP:
        return RIGHT
    if direction == RIGHT:
        return DOWN
    if direction == DOWN:
        return LEFT
    if direction == LEFT:
        return UP


def out_of_bounds(position, row_count, col_count):
    row_i, col_i = position

    row_invalid = row_i < 0 or row_i >= row_count
    col_invalid = col_i < 0 or col_i >= col_count

    return row_invalid or col_invalid


def at(position, input):
    row_i, col_i = position
    return input[row_i][col_i]


def get_visited(input: Input) -> set[tuple[int, int]]:
    """
    Returns the set of positions that the guard visits
    """
    visited = set()

    row_count = len(input)
    col_count = len(input[0])

    # Find the initial position of the guard.
    # Get the index of the row in which ^ appears, and the index of ^ within
    # the row
    row_i = next(i for i, row in enumerate(input) if CARET in row)
    col_i = input[row_i].index(CARET)
    position = (row_i, col_i)

    # record initial position in set
    visited.add(position)

    direction = UP  # left/right, up/down

    # i = 0
    while True:
        # print(i, visited)
        # i += 1

        # figure out what the next position will be
        next_pos = move(position, direction)

        # if the guard left the area, break
        if out_of_bounds(next_pos, row_count, col_count):
            break

        # if the guard is in front of an obstacle, turn, but don't move right
        # now, because she could also be blocked in the new direction, so
        # skip to the next loop to determine that
        if at(next_pos, input) == OBSTACLE:
            direction = turn(direction)
            continue

        position = next_pos
        visited.add(position)

    return visited


def part1(input: Input) -> int:
    positions = get_visited(input)
    return len(positions)


def part2(input: Input):
    """
    This is how a loop has to look:

     x
            x
    x
           x

    Corners of the rectangle:
    - Top left:
      - 1 above the top right
      - 1 to the right of the bottom left
    - Top right:
      - 1 below the top left
      - 1 to the right of the bottom right
    - Bottom left:
      - 1 above the bottom right
      - 1 to the left of the top left
    - Bottom right:
      - 1 below the bottom left
      - 1 to left of top right

    So each "corner" is 1 above/below another, and 1 left/right of another

    Each obstacle could be any of the four types of corner.

    Potential algorithm to get loops:
    - For each obstacle in the grid:
        - For each type of corner:
            - Find where the other two adjacent corners would be
              (i.e. if this corner is bottom right, we find the bottom left
              and top right)
            - If we can't find those, continue
            - If we can, use the distances between the three corners to
              figure out where the fourth corner should be
            - In theory, there shouldn't be a corner there already. Record
              that location as a place for a loop

    Then we have to confirm if the potential loops are loops that the guard
    could actually end up in. Algorithm:

    - For loop in loops:
        - For corner in loop:
            - Check if the coordinate is actually within the bounds of the
              input. If not, obviously this loop isn't valid
            - Check if the guard ever visited the correct side
              (e.g. if we're talking about the bottom left corner, the guard
              would have to have visited the square to the right of it,
              because she would then turn 90˚ and go up and hit the top
              left)
            - If yes, this loop is valid. Else, it's not
    """
    answer = 0

    # Get the coords of all the obstacles
    obstacles = [
        (row_i, col_i)
        for row_i, row in enumerate(input)
        for col_i, char in enumerate(row)
        if char == OBSTACLE
    ]

    # print(obstacles)

    for obstacle in obstacles:
        orow_i, ocol_i = obstacle  # 'o' prefix for 'obstacle'

        top_left = None
        top_right = None
        bottom_left = None
        bottom_right = None

        ###################################################
        ### Check if this obstacle is a top-left corner ###
        ###################################################
        # BL coordinates:
        # - col is one less than obstacle's
        # - row is some amount bigger than obstacle's
        bottom_left_candidates = [
            (row_i, col_i)
            for row_i, col_i in obstacles
            if col_i == ocol_i - 1 and row_i > orow_i
        ]
        # Top right coordinates:
        # - col is some amount bigger than obstacle's
        # - row is one more than obstacle's
        top_right_candidates = [
            (row_i, col_i)
            for row_i, col_i in obstacles
            if row_i == orow_i + 1 and col_i > ocol_i
        ]
        if len(bottom_left_candidates) > 0 and len(top_right_candidates) > 0:
            top_left = obstacle
            # top_right = something
            # bottom_left = something

            # top-right is 1 below bottom-right and 1 to the left of top-right
            # bottom_right = (bottom_left[0] + 1, top_right[1] - 1)

        ###################################################
        ### Check if this obstacle is a top-right corner ###
        ###################################################
        # top-left coordinates:
        # - row is one less than obstacle's
        # - col is some amount smaller than obstacle's
        top_left_candidates = [
            (row_i, col_i)
            for row_i, col_i in obstacles
            if row_i == orow_i - 1 and col_i < ocol_i
        ]
        # bottom right coordinates:
        # - col is 1 less than obstacle's
        # - row is some amount bigger than obstacle's
        bottom_right_candidates = [
            (row_i, col_i)
            for row_i, col_i in obstacles
            if col_i == ocol_i - 1 and row_i > orow_i
        ]
        if len(top_left_candidates) > 0 and len(bottom_right_candidates) > 0:
            top_right = obstacle
            # top_left = something
            # bottom_right = something

            # bottom-left is 1 above bottom-right and 1 to left of top-left
            # bottom_left = (bottom_right[0] - 1, top_left[1] - 1)

        ######################################################
        ### Check if this obstacle is a bottom-left corner ###
        ######################################################
        # Top-left coordinates:
        # - col is one more than obstacle's
        # - row is some amount smaller than obstacle's
        top_left_candidates = [
            (row_i, col_i)
            for row_i, col_i in obstacles
            if col_i == ocol_i + 1 and row_i < orow_i
        ]
        # Bottom-right coordinates:
        # - col is some amount bigger than obstacle's
        # - row is one more than obstacle's
        bottom_right_candidates = [
            (row_i, col_i)
            for row_i, col_i in obstacles
            if row_i == orow_i + 1 and col_i > ocol_i
        ]
        if len(top_left_candidates) > 0 and len(bottom_right_candidates) > 0:
            bottom_left = obstacle
            # top_left = something
            # bottom_right = something

            # top-right is 1 below top-left and 1 to the right of bottom-right
            # top_right = (top_left[0] - 1, bottom_right[1] + 1)

        #######################################################
        ### Check if this obstacle is a bottom-right corner ###
        #######################################################
        # Bottom-left coordinates:
        # - row is 1 less than obstacle's
        # - col is some amount smaller than obstacle's
        bottom_left_candidates = [
            (row_i, col_i)
            for row_i, col_i in obstacles
            if row_i == orow_i - 1 and col_i < ocol_i
        ]
        # Top-right coordinates:
        # - col is 1 bigger than obstacle's
        # - row is some amount smaller than obstacle's
        top_right_candidates = [
            (row_i, col_i)
            for row_i, col_i in obstacles
            if col_i == ocol_i + 1 and row_i < orow_i
        ]
        if len(bottom_left_candidates) > 0 and len(top_right_candidates) > 0:
            bottom_right = obstacle
            # bottom_left = something
            # top_right = something

            # top-left is 1 above bottom-left and 1 to the left of top-right
            # top_left = (bottom_left[0] - 1, top_right[1] - 1)

    return answer


def main():
    utils.handle(
        part1,
        #         """....#.....
        # .........#
        # ..........
        # ..#.......
        # .......#..
        # ..........
        # .#..^.....
        # ........#.
        # #.........
        # ......#...
        # """,
    )  # 5312 (0.0061991214752197266 seconds)
    utils.handle(part2)


if __name__ == "__main__":
    main()
