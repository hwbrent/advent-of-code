import os
import sys

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2023/day/1
# Input URL:   https://adventofcode.com/2023/day/1/input

"""
--- Day 1: Trebuchet?! ---

Something is wrong with global snow production, and you've been selected to
take a look. The Elves have even given you a map; on it, they've used stars
to mark the top fifty locations that are likely to be having problems.
You've been doing this long enough to know that to restore snow operations,
you need to check all fifty stars by December 25th.
Collect stars by solving puzzles.  Two puzzles will be made available on
each day in the Advent calendar; the second puzzle is unlocked when you complete
the first.  Each puzzle grants one star. Good luck!
You try to ask why they can't just use a weather machine ("not powerful
enough") and where they're even sending you ("the sky") and why your map looks
mostly blank ("you sure ask a lot of questions") and hang on did you just
say the sky ("of course, where do you think snow comes from") when you
realize that the Elves are already loading you into a trebuchet ("please hold
still, we need to strap you in").
As they're making the final adjustments, they discover that their calibration
document (your puzzle input) has been amended by a very young Elf who
was apparently just excited to show off her art skills. Consequently, the
Elves are having trouble reading the values on the document.
The newly-improved calibration document consists of lines of text; each line
originally contained a specific calibration value that the Elves now need
to recover. On each line, the calibration value can be found by combining
the first digit and the last digit (in that order) to form a single two-digit
number.
For example:
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15,
and 77. Adding these together produces 142.
Consider your entire calibration document. What is the sum of all of the
calibration values?

--- Part Two ---

Your calculation isn't quite right. It looks like some of the digits are
actually spelled out with letters: one, two, three, four, five, six, seven,
eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and
last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76.
Adding these together produces 281.

What is the sum of all of the calibration values?
"""


def parse_raw_input(input: str):
    return input.strip().split("\n")


def part1(input):
    total = 0

    def find_num(line: str) -> str:
        for char in line:
            if char.isnumeric():
                return char

    for line in input:
        digit1 = find_num(line)
        digit2 = find_num(line[::-1])

        num = int(digit1 + digit2)

        total += num

    print(total)


def part2(input):
    words = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
    digits = tuple(str(num) for num in range(10))

    indices = {}

    def add(line: str, seq: tuple) -> int:
        for entry in seq:
            if entry in line:
                earliest = line.index(entry)
                latest = line.rindex(entry)
                indices[entry] = (earliest, latest)

    total = 0

    for line in input:
        add(line, words)
        add(line, digits)

        # print(line, indices)

        earliest_index = len(line)
        latest_index = -1
        earliest_number = None
        latest_number = None

        for number, (early, late) in indices.items():
            if early < earliest_index:
                earliest_index = early
                earliest_number = number
            if late > latest_index:
                latest_index = late
                latest_number = number

        if earliest_number in words:
            earliest_number = str(words.index(earliest_number) + 1)
        if latest_number in words:
            latest_number = str(words.index(latest_number) + 1)

        total += int(earliest_number + latest_number)

        indices.clear()

    print(total)


def main():
    raw_input = utils.get_raw_input()
    parsed_input = parse_raw_input(raw_input)

    part1(parsed_input)  # 54708
    part2(parsed_input)  # 54087


if __name__ == "__main__":
    main()
