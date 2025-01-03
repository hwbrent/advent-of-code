import os
import sys
import copy
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2024/day/12
# Input URL:   https://adventofcode.com/2024/day/12/input

"""
--- Day 12: Garden Groups ---

Why not search for the Chief Historian near the gardener and his massive farm? There's plenty of food, so The Historians grab something to eat while they search.
You're about to settle near a complex arrangement of garden plots when some Elves ask if you can lend a hand. They'd like to set up fences around each region of garden plots, but they can't figure out how much fence they need to order or how much it will cost. They hand you a map (your puzzle input) of the garden plots.
Each garden plot grows only a single type of plant and is indicated by a single letter on your map. When multiple garden plots are growing the same type of plant and are touching (horizontally or vertically), they form a region. For example:
AAAA
BBCD
BBCC
EEEC

This 4x4 arrangement includes garden plots growing five different types of plants (labeled A, B, C, D, and E), each grouped into their own region.
In order to accurately calculate the cost of the fence around a single region, you need to know that region's area and perimeter.
The area of a region is simply the number of garden plots the region contains. The above map's type A, B, and C plants are each in a region of area 4. The type E plants are in a region of area 3; the type D plants are in a region of area 1.
Each garden plot is a square and so has four sides. The perimeter of a region is the number of sides of garden plots in the region that do not touch another garden plot in the same region. The type A and C plants are each in a region with perimeter 10. The type B and E plants are each in a region with perimeter 8. The lone D plot forms its own region with perimeter 4.
Visually indicating the sides of plots in each region that contribute to the perimeter using - and |, the above map's regions' perimeters are measured as follows:
+-+-+-+-+
|A A A A|
+-+-+-+-+     +-+
              |D|
+-+-+   +-+   +-+
|B B|   |C|
+   +   + +-+
|B B|   |C C|
+-+-+   +-+ +
          |C|
+-+-+-+   +-+
|E E E|
+-+-+-+

Plants of the same type can appear in multiple separate regions, and regions can even appear within other regions. For example:
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO

The above map contains five regions, one containing all of the O garden plots, and the other four each containing a single X plot.
The four X regions each have area 1 and perimeter 4. The region containing 21 type O plants is more complicated; in addition to its outer edge contributing a perimeter of 20, its boundary with each X region contributes an additional 4 to its perimeter, for a total perimeter of 36.
Due to "modern" business practices, the price of fence required for a region is found by multiplying that region's area by its perimeter. The total price of fencing all regions on a map is found by adding together the price of fence for every region on the map.
In the first example, region A has price 4 * 10 = 40, region B has price 4 * 8 = 32, region C has price 4 * 10 = 40, region D has price 1 * 4 = 4, and region E has price 3 * 8 = 24. So, the total price for the first example is 140.
In the second example, the region with all of the O plants has price 21 * 36 = 756, and each of the four smaller X regions has price 1 * 4 = 4, for a total price of 772 (756 + 4 + 4 + 4 + 4).
Here's a larger example:
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE

It contains:

A region of R plants with price 12 * 18 = 216.
A region of I plants with price 4 * 8 = 32.
A region of C plants with price 14 * 28 = 392.
A region of F plants with price 10 * 18 = 180.
A region of V plants with price 13 * 20 = 260.
A region of J plants with price 11 * 20 = 220.
A region of C plants with price 1 * 4 = 4.
A region of E plants with price 13 * 18 = 234.
A region of I plants with price 14 * 22 = 308.
A region of M plants with price 5 * 12 = 60.
A region of S plants with price 3 * 8 = 24.

So, it has a total price of 1930.
What is the total price of fencing all regions on your map?
"""


def parse_raw_input(input: str):
    return [[char for char in line.strip()] for line in input.strip().split(os.linesep)]


def in_range(coord, input) -> bool:
    row_count = len(input)
    col_count = len(input[0])

    row, col = coord
    return row in range(row_count) and col in range(col_count)


def get_type(coord, input) -> str:
    row, col = coord
    return input[row][col]


def visualise_region(region, input) -> None:
    """
    Shows the
    """

    # create a copy of the input to amend
    vis = copy.deepcopy(input)

    # for each row/col coordinate in 'region', grab the value, and make it
    # green
    for coord in region:
        row, col = coord
        # see: https://stackoverflow.com/a/287944
        vis[row][col] = "\033[92m" + vis[row][col] + "\033[0m"

    # we don't want to show the entire input because it's massive, so we show
    # the smallest possible rectangle containing the pattern
    row_coords = [coord[0] for coord in region]
    col_coords = [coord[1] for coord in region]
    min_row = min(row_coords)
    max_row = max(row_coords)
    min_col = min(col_coords)
    max_col = max(col_coords)
    # show any surrounding rows/cols
    if min_row != 0:
        min_row -= 1
    if min_col != 0:
        min_col -= 1
    if max_row != len(input):
        max_row += 1
    if max_col != len(input[0]):
        max_col += 1

    print()
    rows = vis[min_row : max_row + 1]
    for row in rows:
        vals = row[min_col : max_col + 1]
        print("".join(vals))
    print()


def part1(input):
    """
    Delineate the regions
    - Init a variable 'plot_regions' - a 2d list (same dimensions as 'input')
      to track which region each plot is in
    - For each plot:
      - For each surrounding plot:
        - If it has a group already, skip
        - If it doesn't have a group, and its type is the same as the current
          plot, add it to the current group

    Figure out each region's perimeter
    - For each region:
      - Init a 'group_perimeter' variable
      - For each plot within the region:
        - Figure out how many neighbours this plot has
        - If the number is not four, the plot is on the perimeter, so add
          the number of neighbours to 'group_perimeter'

    Figure out the price of each region's fencing
    - For each region:
      - Multiply its 'group_perimeter' by the number of plots in the region
        to get the price of the fencing, and increment 'overall_pricing' by
        that much
    """

    answer = None

    regions = []
    plot_regions = [[None for _ in row] for row in input]
    region_neighbours = {}  # key is coord, value is int

    has_no_region = lambda row, col: plot_regions[row][col] is None

    def check_surrounding(coord, region_num):
        row, col = coord

        # add the current coord to the region
        regions[region_num].append(coord)

        # mark the current value as being in a region
        plot_regions[row][col] = region_num

        # figure out which of the surrounding
        above = (row + 1, col)
        below = (row - 1, col)
        left = (row, col - 1)
        right = (row, col + 1)
        surrounding = (above, below, left, right)

        # function to check if 'x' is a valid neighbour of 'coord' (i.e.
        # is within the bounds of the input and is of the same type as
        # 'coord')
        is_neighbour = lambda x: in_range(x, input) and get_type(x, input) == get_type(
            coord, input
        )

        # record which neighbours 'coord' has
        neighbours = {
            "above": above if is_neighbour(above) else None,
            "below": below if is_neighbour(below) else None,
            "left": left if is_neighbour(left) else None,
            "right": right if is_neighbour(right) else None,
        }
        region_neighbours[coord] = neighbours

        # recurse on each neighbour which isn't already recorded as being in
        # a region (and therefore is in this region),
        eligible = (n for n in neighbours.values() if n and has_no_region(*n))
        for entry in eligible:
            check_surrounding(entry, region_num)

    # figure out the regions
    for row_i, row in enumerate(input):
        for col_i, _ in enumerate(row):
            # if this plot is in a region, skip it
            region = plot_regions[row_i][col_i]
            if not (region is None):
                continue

            # register a new region
            region_num = len(regions)
            regions.append([])

            # find the plots that form the new region
            coord = (row_i, col_i)
            check_surrounding(coord, region_num)

    # for region in regions:
    #     visualise_region(region, input)

    # figure out the perimeters of each region
    perimeters = []
    for region in regions:
        perimeter = 0
        for coord in region:
            # get the number of valid neighbours. if there are 4, that means
            # one on every side, so 'coord' isn't on the perimeter
            neighbours = [v for v in region_neighbours[coord].values() if not v is None]
            count = len(neighbours)
            if count == 4:
                continue

            # if a plot has one neighbour, that means it has three sides free
            perimeter += 4 - count

        perimeters.append(perimeter)

    total_price = 0
    for region, perimeter in zip(regions, perimeters):
        price = len(region) * perimeter
        total_price += price
    return total_price


def part2(input):
    answer = None
    return answer


def main():
    utils.handle(part1)  # 1421958 (0.09386968612670898 seconds)
    utils.handle(part2)


if __name__ == "__main__":
    main()
