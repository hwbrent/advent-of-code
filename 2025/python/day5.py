import os
import sys
from copy import deepcopy
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2025/day/5
# Input URL:   https://adventofcode.com/2025/day/5/input

FreshIdRange = list[int, int]
FreshIdRanges = list[FreshIdRange]

AvailableId = int
AvailableIds = list[AvailableId]

Input = tuple[FreshIdRanges, AvailableIds]


def parse_raw_input(input: str) -> Input:
    # input = """
    # 3-5
    # 10-14
    # 16-20
    # 12-18

    # 1
    # 5
    # 8
    # 11
    # 17
    # 32
    # """

    fresh_id_ranges, available_ids = input.strip().split(2 * os.linesep)

    fresh_id_ranges = [
        [int(num) for num in line.strip().split("-")]
        for line in fresh_id_ranges.strip().split(os.linesep)
    ]

    available_ids = [int(num.strip()) for num in available_ids.split(os.linesep)]

    return fresh_id_ranges, available_ids


def part1(input: Input) -> int:
    answer = 0

    fresh_id_ranges, available_ids = input

    for available_id in available_ids:
        for fresh_id_range in fresh_id_ranges:
            lower_incl, upper_incl = fresh_id_range
            if available_id in range(lower_incl, upper_incl + 1):
                answer += 1
                break

    return answer


def part2(input: Input) -> int:
    answer = 0

    fresh_id_ranges, _ = input

    # merge ranges that overlap.
    # doing this means we dont have to worry about the same id being
    # accounted for in multiple different ranges

    sorted_ranges = sorted(fresh_id_ranges, key=lambda x: x[0])
    merged_ranges = deepcopy(sorted_ranges)
    i = 0
    while i < len(merged_ranges) - 1:
        r1 = merged_ranges[i]
        r2 = merged_ranges[i + 1]

        r1_lower, r1_upper = r1
        r2_lower, r2_upper = r2

        if r1_upper >= r2_lower:
            # we're combining two ranges into one, so get rid of one of the
            # preexisting ranges
            del merged_ranges[i + 1]

            new_lower = r1_lower  # at most the same as r2_lower. no need to compare
            new_upper = max(r1_upper, r2_upper)
            merged_ranges[i] = [new_lower, new_upper]
        else:
            i += 1

    # for each range, get the number of ids in the range by subtracting the
    # upper bound from the lower bound
    for fresh_id_range in merged_ranges:
        lower, upper = fresh_id_range
        ids_in_range = upper + 1 - lower
        answer += ids_in_range

    return answer


def main():
    utils.handle(part1)
    utils.handle(part2)


if __name__ == "__main__":
    main()
