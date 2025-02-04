import os
import sys
import itertools as it
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2024/day/2
# Input URL:   https://adventofcode.com/2024/day/2/input

"""
--- Day 2: Red-Nosed Reports ---

Fortunately, the first location The Historians want to search isn't a long walk from the Chief Historian's office.
While the Red-Nosed Reindeer nuclear fusion/fission plant appears to contain no sign of the Chief Historian, the engineers there run up to you as soon as they see you. Apparently, they still talk about the time Rudolph was saved through molecular synthesis from a single electron.
They're quick to add that - since you're already here - they'd really appreciate your help analyzing some unusual data from the Red-Nosed reactor. You turn to check if The Historians are waiting for you, but they seem to have already divided into groups that are currently searching every corner of the facility. You offer to help with the unusual data.
The unusual data (your puzzle input) consists of many reports, one report per line. Each report is a list of numbers called levels that are separated by spaces. For example:
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9

This example data contains six reports each containing five levels.
The engineers are trying to figure out which reports are safe. The Red-Nosed reactor safety systems can only tolerate levels that are either gradually increasing or gradually decreasing. So, a report only counts as safe if both of the following are true:

The levels are either all increasing or all decreasing.
Any two adjacent levels differ by at least one and at most three.

In the example above, the reports can be found safe or unsafe by checking those rules:

7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.

So, in this example, 2 reports are safe.
Analyze the unusual data from the engineers. How many reports are safe?
"""


def is_safe(report: list[int]) -> bool:
    """
    Returns a bool indicating whether `report` is "safe", meaning:
    1. All of the pairwise differences are either increasing/decreasing
    2. All of the pairwise differences are >= 0 and <= 3
    """

    # Do pairwise subtraction to figure out the differences between each
    # pair of "levels" in the report
    pairs = it.pairwise(report)
    diffs = [b - a for a, b in pairs]

    # Figure out if all the differences are either increasing or
    # decreasing
    increasing = [d > 0 for d in diffs]
    decreasing = [d < 0 for d in diffs]

    # Figure out if each difference is within the acceptable range
    # between 1 and 3
    diffs_in_range = [1 <= abs(diff) <= 3 for diff in diffs]

    # The number of times False appears in each list. For the report to
    # be safe, the count has to be zero in ((1 OR 2) AND 3)
    counts = (
        increasing.count(False),
        decreasing.count(False),
        diffs_in_range.count(False),
    )

    # Figure out if the report is "safe"
    safe = (counts[0] == 0 or counts[1] == 0) and counts[2] == 0

    return safe


def parse_raw_input(input: str) -> tuple[int, int]:
    """
    Returns an tuple of length two with these values:
    1. int - the answer for part 1
    2. int - the answer for part 2
    """
    count_part1 = 0
    count_part2 = 0

    lines = input.strip().split("\n")
    for report in lines:
        # Get list of ints
        report = report.split()
        report = [int(level) for level in report]

        # check if the initial report is safe
        if is_safe(report):
            count_part1 += 1
            count_part2 += 1
            continue

        # Iterate over the report, and for each loop, remove the level at
        # that index, and check if the resulting report is safe
        for i, _ in enumerate(report):
            removed = report[:i] + report[i + 1 :]
            safe = is_safe(removed)
            if not safe:
                continue

            count_part2 += 1
            break

    return count_part1, count_part2


def part1(answers: tuple[int, int]) -> int:
    p1, _ = answers
    return p1


def part2(answers: tuple[int, int]) -> int:
    _, p2 = answers
    return p2


def main():
    utils.handle(part1)  # 572 (0.01081395149230957 seconds)
    utils.handle(part2)  # 612 (0.011951208114624023 seconds)


if __name__ == "__main__":
    main()
