import os
import sys
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2025/day/2
# Input URL:   https://adventofcode.com/2025/day/2/input

"""
--- Day 2: Gift Shop ---

You get inside and take the elevator to its only other stop: the gift shop. "Thank you for visiting the North Pole!" gleefully exclaims a nearby sign. You aren't sure who is even allowed to visit the North Pole, but you know you can access the lobby through here, and from there you can access the rest of the North Pole base.

As you make your way through the surprisingly extensive selection, one of the clerks recognizes you and asks for your help.

As it turns out, one of the younger Elves was playing on a gift shop computer and managed to add a whole bunch of invalid product IDs to their gift shop database! Surely, it would be no trouble for you to identify the invalid product IDs for them, right?

They've even checked most of the product ID ranges already; they only have a few product ID ranges (your puzzle input) that you'll need to check. For example:

11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124

(The ID ranges are wrapped here for legibility; in your input, they appear on a single long line.)

The ranges are separated by commas (,); each range gives its first ID and last ID separated by a dash (-).

Since the young Elf was just doing silly patterns, you can find the invalid IDs by looking for any ID which is made only of some sequence of digits repeated twice. So, 55 (5 twice), 6464 (64 twice), and 123123 (123 twice) would all be invalid IDs.

None of the numbers have leading zeroes; 0101 isn't an ID at all. (101 is a valid ID that you would ignore.)

Your job is to find all of the invalid IDs that appear in the given ranges. In the above example:

    11-22 has two invalid IDs, 11 and 22.
    95-115 has one invalid ID, 99.
    998-1012 has one invalid ID, 1010.
    1188511880-1188511890 has one invalid ID, 1188511885.
    222220-222224 has one invalid ID, 222222.
    1698522-1698528 contains no invalid IDs.
    446443-446449 has one invalid ID, 446446.
    38593856-38593862 has one invalid ID, 38593859.
    The rest of the ranges contain no invalid IDs.

Adding up all the invalid IDs in this example produces 1227775554.

What do you get if you add up all of the invalid IDs?
"""

Input = list[str, str]


def parse_raw_input(input: str) -> Input:
    # input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
    return [pair.split("-") for pair in input.strip().split(",")]


def part1(input: Input):
    answer = 0
    for first_id, last_id in input:

        # pad to ensure the numbers are the same length
        length1 = len(first_id)
        length2 = len(last_id)
        max_length = max(length1, length2)
        first_id = first_id.rjust(max_length, "0")
        last_id = last_id.rjust(max_length, "0")

        # brute force
        first_num = int(first_id)
        last_num = int(last_id)

        full_range = range(first_num, last_num + 1)
        for id in full_range:
            id = str(id)
            length = len(id)
            first_half = id[: length // 2]
            second_half = id[length // 2 :]
            if first_half == second_half:
                # print("    ", [first_num, last_num], "*", id)
                answer += int(id)
            else:
                # print("    ", [first_num, last_num], id)
                pass

    return answer


def part2(input):
    answer = 0
    for first_id, last_id in input:

        # pad to ensure the numbers are the same length
        length1 = len(first_id)
        length2 = len(last_id)
        max_length = max(length1, length2)
        first_id = first_id.rjust(max_length, "0")
        last_id = last_id.rjust(max_length, "0")

        # brute force
        first_num = int(first_id)
        last_num = int(last_id)

        full_range = range(first_num, last_num + 1)
        for id in full_range:
            id = str(id)

            # cant repeat if it's bigger than half the length of the entire
            # id
            max_substring_length = len(id) // 2
            for substring_length in range(1, max_substring_length + 1):
                # split the number up into substrings of length 'substring_length'
                substrings = set()
                first_idx = 0
                last_idx = substring_length
                while last_idx < len(id):
                    substring = id[first_idx:last_idx]
                    substrings.add(substring)
                    first_idx += substring_length
                    last_idx += substring_length

                if len(substrings) == 1:
                    answer += int(substring)

    return answer


def main():
    utils.handle(part1)  # 54234399924 (0.9478640556335449 seconds)
    utils.handle(part2)


if __name__ == "__main__":
    main()
