import numpy as np

import os
import sys
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2024/day/1
# Input URL:   https://adventofcode.com/2024/day/1/input

"""
--- Day 1: Historian Hysteria ---

The Chief Historian is always present for the big Christmas sleigh launch, but nobody has seen him in months! Last anyone heard, he was visiting locations that are historically significant to the North Pole; a group of Senior Historians has asked you to accompany them as they check the places they think he was most likely to visit.
As each location is checked, they will mark it on their list with a star. They figure the Chief Historian must be in one of the first fifty places they'll look, so in order to save Christmas, you need to help them get fifty stars on their list before Santa takes off on December 25th.
Collect stars by solving puzzles.  Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first.  Each puzzle grants one star. Good luck!
You haven't even left yet and the group of Elvish Senior Historians has already hit a problem: their list of locations to check is currently empty. Eventually, someone decides that the best place to check first would be the Chief Historian's office.
Upon pouring into the office, everyone confirms that the Chief Historian is indeed nowhere to be found. Instead, the Elves discover an assortment of notes and lists of historically significant locations! This seems to be the planning the Chief Historian was doing before he left. Perhaps these notes can be used to determine which locations to search?
Throughout the Chief's office, the historically significant locations are listed not by name but by a unique number called the location ID. To make sure they don't miss anything, The Historians split into two groups, each searching the office and trying to create their own complete list of location IDs.
There's just one problem: by holding the two lists up side by side (your puzzle input), it quickly becomes clear that the lists aren't very similar. Maybe you can help The Historians reconcile their lists?
For example:
3   4
4   3
2   5
1   3
3   9
3   3

Maybe the lists are only off by a small amount! To find out, pair up the numbers and measure how far apart they are. Pair up the smallest number in the left list with the smallest number in the right list, then the second-smallest left number with the second-smallest right number, and so on.
Within each pair, figure out how far apart the two numbers are; you'll need to add up all of those distances. For example, if you pair up a 3 from the left list with a 7 from the right list, the distance apart is 4; if you pair up a 9 with a 3, the distance apart is 6.
In the example list above, the pairs and distances would be as follows:

The smallest number in the left list is 1, and the smallest number in the right list is 3. The distance between them is 2.
The second-smallest number in the left list is 2, and the second-smallest number in the right list is another 3. The distance between them is 1.
The third-smallest number in both lists is 3, so the distance between them is 0.
The next numbers to pair up are 3 and 4, a distance of 1.
The fifth-smallest numbers in each list are 3 and 5, a distance of 2.
Finally, the largest number in the left list is 4, while the largest number in the right list is 9; these are a distance 5 apart.

To find the total distance between the left list and the right list, add up the distances between all of the pairs you found. In the example above, this is 2 + 1 + 0 + 1 + 2 + 5, a total distance of 11!
Your actual left and right lists contain many location IDs. What is the total distance between your lists?
"""


def parse_raw_input(input: str) -> tuple[np.ndarray, np.ndarray, dict]:
    """
    Returns a tuple wherein:
    - The first  value is the left-hand  list as a numpy array
    - The second value is the right-hand list as a numpy array
    - The third  value is a dict containing the number of times each number
      in the right-hand list appeared
    """
    lines = input.strip().split("\n")

    left_list = []
    right_list = []
    right_counts = {}

    for line in lines:
        left_str, right_str = line.split()
        left_int, right_int = int(left_str), int(right_str)
        left_list.append(left_int)
        right_list.append(right_int)

        # Increment the count in right_counts. If no entry for this number
        # exists, use a default of 0
        count = right_counts.get(right_int, 0)
        right_counts[right_int] = count + 1

    left_arr = np.array(left_list)
    right_arr = np.array(right_list)

    return np.sort(left_arr), np.sort(right_arr), right_counts


def part1(input):
    # 1. sort each from smallest to biggest (done in 'parse_raw_input')
    # 2. do pairwise diff
    # 3. get sum of diffs

    left, right, _ = input

    distances = abs(left - right)
    total_distance = sum(distances)

    return total_distance


def part2(input):
    """
    1. Figure out how many times each element in 'right' appears (done in
       'parse_raw_input')
    2. For each value in 'left', figure out how many times it appears in
       'right' by querying the dict from step 1, and multiply the value by
       that count
    3. Sum up the products
    """
    left, _, right_counts = input

    # Create a function which, given a number, gets that number's count in
    # 'right', and 'vectorise' it so that it can be applied to every entry
    # in a numpy array
    getter = lambda num: right_counts.get(num, 0)
    get_counts = np.vectorize(getter)

    # Apply the vectorised function to get a new array containing the number
    # of times each value in 'left' appears in 'right'
    left_counts = get_counts(left)

    # Get the sum of the two arrays multiplied pairwise
    similarity_score = np.sum(left * left_counts)

    return similarity_score


def main():
    raw_input = utils.get_raw_input()
    # fmt: off
    # raw_input = """"""
    # fmt: on
    parsed_input = parse_raw_input(raw_input)

    utils.handle(part1(parsed_input), 1)  # 1941353
    utils.handle(part2(parsed_input), 2)  # 22539317


if __name__ == "__main__":
    main()
