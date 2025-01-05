from PIL import Image
import numpy as np

import os
import sys
import time
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2024/day/14
# Input URL:   https://adventofcode.com/2024/day/14/input

"""
--- Day 14: Restroom Redoubt ---

One of The Historians needs to use the bathroom; fortunately, you know there's a bathroom near an unvisited location on their list, and so you're all quickly teleported directly to the lobby of Easter Bunny Headquarters.
Unfortunately, EBHQ seems to have "improved" bathroom security again after your last visit. The area outside the bathroom is swarming with robots!
To get The Historian safely to the bathroom, you'll need a way to predict where the robots will be in the future. Fortunately, they all seem to be moving on the tile floor in predictable straight lines.
You make a list (your puzzle input) of all of the robots' current positions (p) and velocities (v), one robot per line. For example:
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3

Each robot's position is given as p=x,y where x represents the number of tiles the robot is from the left wall and y represents the number of tiles from the top wall (when viewed from above). So, a position of p=0,0 means the robot is all the way in the top-left corner.
Each robot's velocity is given as v=x,y where x and y are given in tiles per second. Positive x means the robot is moving to the right, and positive y means the robot is moving down. So, a velocity of v=1,-2 means that each second, the robot moves 1 tile to the right and 2 tiles up.
The robots outside the actual bathroom are in a space which is 101 tiles wide and 103 tiles tall (when viewed from above). However, in this example, the robots are in a space which is only 11 tiles wide and 7 tiles tall.
The robots are good at navigating over/under each other (due to a combination of springs, extendable legs, and quadcopters), so they can share the same tile and don't interact with each other. Visually, the number of robots on each tile in this example looks like this:
1.12.......
...........
...........
......11.11
1.1........
.........1.
.......1...

These robots have a unique feature for maximum bathroom security: they can teleport. When a robot would run into an edge of the space they're in, they instead teleport to the other side, effectively wrapping around the edges. Here is what robot p=2,4 v=2,-3 does for the first few seconds:
Initial state:
...........
...........
...........
...........
..1........
...........
...........

After 1 second:
...........
....1......
...........
...........
...........
...........
...........

After 2 seconds:
...........
...........
...........
...........
...........
......1....
...........

After 3 seconds:
...........
...........
........1..
...........
...........
...........
...........

After 4 seconds:
...........
...........
...........
...........
...........
...........
..........1

After 5 seconds:
...........
...........
...........
.1.........
...........
...........
...........

The Historian can't wait much longer, so you don't have to simulate the robots for very long. Where will the robots be after 100 seconds?
In the above example, the number of robots on each tile after 100 seconds has elapsed looks like this:
......2..1.
...........
1..........
.11........
.....1.....
...12......
.1....1....

To determine the safest area, count the number of robots in each quadrant after 100 seconds. Robots that are exactly in the middle (horizontally or vertically) don't count as being in any quadrant, so the only relevant robots are:
..... 2..1.
..... .....
1.... .....
           
..... .....
...12 .....
.1... 1....

In this example, the quadrants contain 1, 3, 4, and 1 robot. Multiplying these together gives a total safety factor of 12.
Predict the motion of the robots in your list within a space which is 101 tiles wide and 103 tiles tall. What will the safety factor be after exactly 100 seconds have elapsed?
"""

Position = list[int, int]
Velocity = list[int, int]
Pair = tuple[Position, Velocity]

Input = list[Pair]


def parse_raw_input(input: str) -> Input:
    input = input.strip()

    tups = []
    for line in input.split(os.linesep):
        line = line.strip()

        position, velocity = line.split(" ")

        position = position.replace("p=", "")
        velocity = velocity.replace("v=", "")

        position = position.split(",")
        velocity = velocity.split(",")

        position = list(map(int, position))
        velocity = list(map(int, velocity))

        tups.append((position, velocity))

    return tups


WIDTH = 101
HEIGHT = 103

# functions to help determine which quadrant a given coord is in. Facilitates
# 'get_safety_score'
WIDTH_MIDPOINT = WIDTH // 2
HEIGHT_MIDPOINT = HEIGHT // 2
left_of_centre = lambda x: x in range(0, WIDTH_MIDPOINT)
right_of_centre = lambda x: x in range(WIDTH_MIDPOINT + 1, WIDTH)
above_centre = lambda y: y in range(0, HEIGHT_MIDPOINT)
below_centre = lambda y: y in range(HEIGHT_MIDPOINT + 1, HEIGHT)

in_top_left = lambda x, y: left_of_centre(x) and above_centre(y)
in_top_right = lambda x, y: right_of_centre(x) and above_centre(y)
in_bottom_left = lambda x, y: left_of_centre(x) and below_centre(y)
in_bottom_right = lambda x, y: right_of_centre(x) and below_centre(y)


def get_safety_score(robots: Input) -> int:
    top_left = 0
    top_right = 0
    bottom_left = 0
    bottom_right = 0

    for robot in robots:
        position, _ = robot
        px, py = position

        if in_top_left(px, py):
            top_left += 1
        if in_top_right(px, py):
            top_right += 1
        if in_bottom_left(px, py):
            bottom_left += 1
        if in_bottom_right(px, py):
            bottom_right += 1

    return top_left * top_right * bottom_left * bottom_right


def part1(input: Input):
    # consts from problem description:
    SECONDS = 100  # basically the number of times we move each robot

    # make each pair move 100 times
    for pair in input:
        position, velocity = pair

        # get the position after 100 seconds
        position[0] += velocity[0] * SECONDS
        position[1] += velocity[1] * SECONDS

        # make the position wrap around
        position[0] %= WIDTH
        position[1] %= HEIGHT

    answer = get_safety_score(input)
    return answer


def part2(input: Input):
    answer = None

    DOWNLOADS_PATH = os.path.join("/", "Users", "henrybrent", "Downloads")

    # arbitrary number; i have no idea when the christmas tree will appear
    SECONDS = 10_000

    start_time = time.time()

    # for each 'second', save an image of the robots in their current
    # positions, and then move the robots
    for sec in range(SECONDS):

        # initialise an empty grid
        grid = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)

        # draw the robots' positions onto the grid
        for robot in input:
            (px, py), _ = robot
            grid[py, px] = 255

        # save the grid as an image
        img = Image.fromarray(grid)
        name = f"{sec}.png"
        print("Saving", name, time.time() - start_time)
        path = os.path.join(DOWNLOADS_PATH, "AoC Day 14", name)
        img.save(path)

        # move each robot
        for robot in input:
            position, velocity = robot
            position[0] += velocity[0]
            position[0] %= WIDTH
            position[1] += velocity[1]
            position[1] %= HEIGHT

    return answer


def main():
    utils.handle(part1)  # 209409792 (0.0018150806427001953 seconds)
    utils.handle(part2)


if __name__ == "__main__":
    main()
