import os
import sys
import time
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2024/day/11
# Input URL:   https://adventofcode.com/2024/day/11/input

"""
--- Day 11: Plutonian Pebbles ---

The ancient civilization on Pluto was known for its ability to manipulate spacetime, and while The Historians explore their infinite corridors, you've noticed a strange set of physics-defying stones.
At first glance, they seem like normal stones: they're arranged in a perfectly straight line, and each stone has a number engraved on it.
The strange part is that every time you blink, the stones change.
Sometimes, the number engraved on a stone changes. Other times, a stone might split in two, causing all the other stones to shift over a bit to make room in their perfectly straight line.
As you observe them for a while, you find that the stones have a consistent behavior. Every time you blink, the stones each simultaneously change according to the first applicable rule in this list:

If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.

No matter how the stones change, their order is preserved, and they stay on their perfectly straight line.
How will the stones evolve if you keep blinking at them? You take a note of the number engraved on each stone in the line (your puzzle input).
If you have an arrangement of five stones engraved with the numbers 0 1 10 99 999 and you blink once, the stones transform as follows:

The first stone, 0, becomes a stone marked 1.
The second stone, 1, is multiplied by 2024 to become 2024.
The third stone, 10, is split into a stone marked 1 followed by a stone marked 0.
The fourth stone, 99, is split into two stones marked 9.
The fifth stone, 999, is replaced by a stone marked 2021976.

So, after blinking once, your five stones would become an arrangement of seven stones engraved with the numbers 1 2024 1 0 9 9 2021976.
Here is a longer example:
Initial arrangement:
125 17

After 1 blink:
253000 1 7

After 2 blinks:
253 0 2024 14168

After 3 blinks:
512072 1 20 24 28676032

After 4 blinks:
512 72 2024 2 0 2 4 2867 6032

After 5 blinks:
1036288 7 2 20 24 4048 1 4048 8096 28 67 60 32

After 6 blinks:
2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2

In this example, after blinking six times, you would have 22 stones. After blinking 25 times, you would have 55312 stones!
Consider the arrangement of stones in front of you. How many stones will you have after blinking 25 times?
"""


def parse_raw_input(input: str):
    return [int(entry) for entry in input.strip().split()]


def blink(stones: list) -> None:
    """
    Does one pass over `stones`, amending it in-place
    """
    i = 0
    while i < len(stones):
        # print(i, len(stones))

        stone = stones[i]

        # if stone is 0, replace it with 1
        if stone == 0:
            stones[i] = 0
            i += 1
            continue

        # if stone has even number of digits, it's replaced by two stones:
        # 1. the left half of the digits
        # 2. the right half of the digits
        string = str(stone)
        length = len(string)
        if length % 2 == 0:
            midpoint = length // 2  # '//' so the result is an int
            left = string[:midpoint]
            right = string[midpoint:]

            stones[i] = left
            stones.insert(i + 1, right)

            i += 2  # skip 'right'
            continue

        # else, multiply by 2024
        stones[i] *= 2024
        i += 1


def part1(stones: list):

    # do 25 blinks
    total = 25
    for i in range(total):
        i = str(i).ljust(2, " ")
        print(f"{i} / {total}", end="")

        start = time.time_ns()
        blink(stones)
        end = time.time_ns()
        secs = (end - start) / 1_000_000_000

        print(f" - {secs} seconds")

    answer = len(stones)
    return answer


def part2(input):
    answer = None
    return answer


def main():
    utils.handle(part1)
    utils.handle(part2)


if __name__ == "__main__":
    main()
