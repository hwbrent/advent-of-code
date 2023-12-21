import os
import sys
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2023/day/10
# Input URL:   https://adventofcode.com/2023/day/10/input

"""
--- Day 10: Pipe Maze ---

You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.
You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.
The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.
Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).
The pipes are arranged in a two-dimensional grid of tiles:

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.
For example, here is a square loop of pipe:
.....
.F-7.
.|.|.
.L-J.
.....

If the animal had entered this loop in the northwest corner, the sketch would instead look like this:
.....
.S-7.
.|.|.
.L-J.
.....

In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.
Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:
-L|F7
7S-7|
L|7||
-L-J|
L|-JF

In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).
Here is a sketch that contains a slightly more complex main loop:
..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ

If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.
In the first example with the square loop:
.....
.S-7.
.|.|.
.L-J.
.....

You can count the distance each tile in the loop is from the starting point like this:
.....
.012.
.1.3.
.234.
.....

In this example, the farthest point from the start is 4 steps away.
Here's the more complex loop again:
..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here are the distances for each tile on that loop:
..45.
.236.
01.78
14567
23...

Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?
"""

compass_directions = ("north", "east", "south", "west")

connections = {
    "|": ("north", "south"),
    "-": ("east", "west"),
    "L": ("north", "east"),
    "J": ("north", "west"),
    "7": ("south", "west"),
    "F": ("south", "east"),
    ".": None,
    "S": compass_directions,
}

north = lambda row, col: (row - 1, col)
south = lambda row, col: (row + 1, col)
east = lambda row, col: (row, col + 1)
west = lambda row, col: (row, col - 1)

in_bounds = lambda row, row_range, col, col_range: (
    row in row_range and col in col_range
)


def parse_raw_input(input: str):
    input = input.strip().split("\n")

    row_range = range(0, len(input))
    col_range = range(0, len(input[0]))

    pipes = {}

    for row_i, row in enumerate(input):
        for col_i, tile in enumerate(row):
            if tile == ".":
                continue

            coord = (row_i, col_i)
            pipes[coord] = {
                "tile": tile,
                "directions": connections[tile],
                "neighbours": [],
            }

    ### Calculate the connections between other pipes ###
    for coord, pipe in pipes.items():
        tile = pipe["tile"]
        directions = pipe["directions"]
        neighbours = pipe["neighbours"]

        for direction in directions:
            # Get the neighbour based on the lambda function with the same
            # name above
            neighbour = globals()[direction](*coord)
            n_row, n_col = neighbour

            # Check if the neighbour is actually in the grid
            # if not (n_row in row_range and n_col in col_range):
            if not in_bounds(n_row, row_range, n_col, col_range):
                continue

            # The neighbour is ".", so do nothing
            if not neighbour in pipes:
                continue

            n_pipe = pipes[(n_row, n_col)]
            n_tile = n_pipe["tile"]
            n_directions = n_pipe["directions"]

            # If the neighbour is S, do nothing
            if n_tile == "S":
                continue

            # Check if the neighbour pipe connects in the direction of this
            # pipe
            opposite_direction = compass_directions[
                (compass_directions.index(direction) + 2) % len(compass_directions)
            ]
            if not opposite_direction in n_directions:
                continue

            neighbours.append({"direction": direction, "coord": neighbour})

    ### Figure out which type of pipe "S" is ###
    S_pipe = next(pipe for pipe in pipes.values() if pipe["tile"] == "S")
    n_compass_directions = tuple(sorted(n["direction"] for n in S_pipe["neighbours"]))
    S_shape = next(
        char
        for char, c_dirs in connections.items()
        if tuple(sorted(c_dirs)) == n_compass_directions
    )
    # print(S_shape)

    return input


def part1(input):
    answer = None
    return answer


def part2(input):
    answer = None
    return answer


def main():
    raw_input = utils.get_raw_input()
    parsed_input = parse_raw_input(raw_input)

    utils.handle(part1(parsed_input), 1)
    utils.handle(part2(parsed_input), 2)


if __name__ == "__main__":
    main()
