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


def parse_raw_input(input: str) -> tuple[list, list, int]:
    """
    Returns a tuple with the following values
    1. `list` of `list` of `int`s - the "reports" from the input
    2. `list` of `bool`s - whether each report in (1) is "safe"
    3. `int` - the number of reports from (1) which are safe

    We can tolerate a single bad level. So if there's one level which isn't
    in the acceptable range or causes the levels to not be all increasing
    or decreasing, we can remove that level and reevaluate

    Workflow:
    1. Evaluate initial report
    2. If the initial report is safe, continue
    3. Else, check which values are out of range, and which are causing the
       levels to not solely in/decrease
    4. If there's only offending level, remove it, and reevaluate the report
    """
    reports = []
    safeties = []
    safe_count = 0

    lines = input.strip().split("\n")
    for report in lines:
        # Get list of ints
        report = report.split()
        report = [int(level) for level in report]
        reports.append(report)

        # Do pairwise subtraction to figure out the differences between each
        # pair of "levels" in the report
        pairs = it.pairwise(report)
        diffs = [b - a for a, b in pairs]
        diff_count = len(diffs)

        # Figure out if all the differences are either increasing or
        # decreasing
        increasing = [d > 0 for d in diffs]
        decreasing = [d < 0 for d in diffs]
        all_increasing = increasing.count(True) == diff_count
        all_decreasing = decreasing.count(True) == diff_count
        all_increasing_or_decreasing = all_increasing or all_decreasing

        # Figure out if each difference is within the acceptable range
        # between 1 and 3
        diffs_in_range = all(1 <= abs(diff) <= 3 for diff in diffs)

        # Using the two bools, figure out if the report is "safe"
        # If initially safe, keep looping
        safe = all_increasing_or_decreasing and diffs_in_range
        if safe:
            safeties.append(safe)
            safe_count += 1
            continue

    return reports, safeties, safe_count


def part1(input: tuple[list, list, int]) -> int:
    """
    1. Evaluate    WHICH of the reports are "safe" (done in 'parse_raw_input')
    2. Evaluate HOW MANY of the reports are "safe" (done in 'parse_raw_input')
    """
    _, __, safe_count = input
    return safe_count


def part2(input):
    answer = None
    return answer


def main():
    raw_input = utils.get_raw_input()
    # fmt: off
    # raw_input = """"""
    # fmt: on
    parsed_input = parse_raw_input(raw_input)

    utils.handle(part1(parsed_input), 1)  # 572
    utils.handle(part2(parsed_input), 2)


if __name__ == "__main__":
    main()
