import os
import sys
from pprint import PrettyPrinter
import math

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2023/day/17
# Input URL:   https://adventofcode.com/2023/day/17/input

"""
--- Day 17: Clumsy Crucible ---

The lava starts flowing rapidly once the Lava Production Facility is operational. As you leave, the reindeer offers you a parachute, allowing you to quickly reach Gear Island.
As you descend, your bird's-eye view of Gear Island reveals why you had trouble finding anyone on your way up: half of Gear Island is empty, but the half below you is a giant factory city!
You land near the gradually-filling pool of lava at the base of your new lavafall. Lavaducts will eventually carry the lava throughout the city, but to make use of it immediately, Elves are loading it into large crucibles on wheels.
The crucibles are top-heavy and pushed by hand. Unfortunately, the crucibles become very difficult to steer at high speeds, and so it can be hard to go in a straight line for very long.
To get Desert Island the machine parts it needs as soon as possible, you'll need to find the best way to get the crucible from the lava pool to the machine parts factory. To do this, you need to minimize heat loss while choosing a route that doesn't require the crucible to go in a straight line for too long.
Fortunately, the Elves here have a map (your puzzle input) that uses traffic patterns, ambient temperature, and hundreds of other parameters to calculate exactly how much heat loss can be expected for a crucible entering any particular city block.
For example:
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533

Each city block is marked by a single digit that represents the amount of heat loss if the crucible enters that block. The starting point, the lava pool, is the top-left city block; the destination, the machine parts factory, is the bottom-right city block. (Because you already start in the top-left block, you don't incur that block's heat loss unless you leave that block and then return to it.)
Because it is difficult to keep the top-heavy crucible going in a straight line for very long, it can move at most three blocks in a single direction before it must turn 90 degrees left or right. The crucible also can't reverse direction; after entering each city block, it may only turn left, continue straight, or turn right.
One way to minimize heat loss is this path:
2>>34^>>>1323
32v>>>35v5623
32552456v>>54
3446585845v52
4546657867v>6
14385987984v4
44578769877v6
36378779796v>
465496798688v
456467998645v
12246868655<v
25465488877v5
43226746555v>

This path never moves more than three consecutive blocks in the same direction and incurs a heat loss of only 102.
Directing the crucible from the lava pool to the machine parts factory, but not moving more than three consecutive blocks in the same direction, what is the least heat loss it can incur?
"""


def parse_raw_input(input: str):
    return input.strip().split("\n")


def part1(input):
    answer = None

    # [row, column]
    start = [0, 0]
    end = [len(input), len(input[0])]

    current = [*start]

    # Movement rules:
    # - Can only move max three blocks in one direction before turning 90°
    #   degrees left/right
    # - Can't reverse direction

    ### Dijkstra ###
    # 1  function Dijkstra(Graph, source):
    # 2
    # 3      for each vertex v in Graph.Vertices:
    # 4          dist[v] ← INFINITY
    # 5          prev[v] ← UNDEFINED
    # 6          add v to Q
    # 7      dist[source] ← 0
    # 8
    # 9      while Q is not empty:
    # 10          u ← vertex in Q with min dist[u]
    # 11          remove u from Q
    # 12
    # 13          for each neighbor v of u still in Q:
    # 14              alt ← dist[u] + Graph.Edges(u, v)
    # 15              if alt < dist[v]:
    # 16                  dist[v] ← alt
    # 17                  prev[v] ← u
    # 18
    # 19      return dist[], prev[]

    # Initialization:
    # - Start at the initial node.
    # - Assign a tentative distance value to every node. Set it to zero for
    #   the initial node and infinity for all other nodes.
    # - Set the initial node as the current node.
    # Exploration:
    # - For the current node, consider all of its neighbors and calculate
    #   their tentative distances through the current node. Compare the newly
    #   calculated tentative distance to the current assigned value and
    #   assign the smaller one.
    # - After considering all neighbors of the current node, mark the current
    #   node as visited.
    # - If the destination node has been visited or if the smallest tentative
    #   distance among the nodes in the unvisited set is infinity, stop. The
    #   algorithm has finished.
    # Selection:
    # - Select the unvisited node with the smallest tentative distance, set
    #   it as the new "current node," and go back to step 2.
    # Termination:
    # - The algorithm stops when the destination node has been visited or
    #   when there are no more unvisited nodes.

    distances = {}

    for row_i, row in enumerate(input):
        for col_i, _ in enumerate(row):
            block = (row_i, col_i)
            distances[block] = 0 if block == tuple(start) else math.inf

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
