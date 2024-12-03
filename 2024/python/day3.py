import os
import sys
import re
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2024/day/3
# Input URL:   https://adventofcode.com/2024/day/3/input

"""
--- Day 3: Mull It Over ---

"Our computers are having issues, so I have no idea if we have any Chief Historians in stock! You're welcome to check the warehouse, though," says the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop. The Historians head out to take a look.
The shopkeeper turns to you. "Any chance you can see why our computers are having issues again?"
The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted. All of the instructions have been jumbled up!
It seems like the goal of the program is just to multiply some numbers. It does that with instructions like mul(X,Y), where X and Y are each 1-3 digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024. Similarly, mul(123,4) would multiply 123 by 4.
However, because the program's memory has been corrupted, there are also many invalid characters that should be ignored, even if they look like part of a mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.
For example, consider the following section of corrupted memory:
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
Only the four highlighted sections are real mul instructions. Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).
Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?
"""


def parse_raw_input(input: str) -> str:
    """
    Returns the input but with whitespace stripped off

    (The input is just one long line, so no need to split into lines or
    anything)
    """
    return input.strip()


def part1(input) -> int:
    """
    1. Create a regex pattern which targets the 'mul(<int>,<int>)' pattern,
       capturing the two numbers as groups
    2. Find each instance of that pattern
    3. For each instance, get the two captured groups, cast them to `int`s,
       multiply them together, and add that number to a running total
    """
    answer = 0
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.finditer(pattern, input)
    for match in matches:
        num1, num2 = int(match[1]), int(match[2])
        answer += num1 * num2
    return answer


def part2(input):
    """
    Pretty much the same as part 1, except we look for "do()" and "don't()"
    as well, and depending on which we find, we skip/proceed with doing the
    multiplication of the 'mul' values
    """

    MUL = "mul"
    DO = "do()"
    DONT = "don't()"

    answer = 0

    # The most recent instruction found.
    # True means "do()", False means "don't()"
    do = True

    # Get the patterns of "mul", "do()" and "don't()"
    patterns = (
        r"mul\((\d{1,3}),(\d{1,3})\)",  # for mul(<int,<int>)
        r"do\(\)",  # for do()
        r"don't\(\)",  # for don't()
    )

    # OR the patterns together into one big pattern.
    # A match will be found if it sees one of the three, meaning we have to
    # check each match to see which one it was
    pattern = f"(({patterns[0]})|({patterns[1]})|({patterns[2]}))"

    matches = re.finditer(pattern, input)
    for match in matches:
        # Get the string which was found.
        # It will either be "do()", "don't", or will start with "mul"
        string = match[0]

        if string.startswith(MUL):
            # If the most recent instruction was "don't()", we don't bother
            # with doing any multiplication
            if not do:
                continue

            # Get the ints within the "mul" instruction
            mul = re.match(patterns[0], string)
            num1, num2 = int(mul[1]), int(mul[2])

            # Add to the final answer
            answer += num1 * num2

        elif string == DO:
            # Set the flag to True
            do = True

        elif string == DONT:
            # Set the flag to False
            do = False

    return answer


def main():
    raw_input = utils.get_raw_input()
    parsed_input = parse_raw_input(raw_input)

    utils.handle(part1(parsed_input), 1)  # 170807108
    utils.handle(part2(parsed_input), 2)  # 74838033


if __name__ == "__main__":
    main()
