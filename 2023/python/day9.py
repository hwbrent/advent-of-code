import os
import sys
import itertools as it
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2023/day/9
# Input URL:   https://adventofcode.com/2023/day/9/input

"""
--- Day 9: Mirage Maintenance ---

You ride the camel through the sandstorm and stop where the ghost's maps told you to stop. The sandstorm subsequently subsides, somehow seeing you standing at an oasis!
The camel goes to get some water and you stretch your neck. As you look up, you discover what must be yet another giant floating island, this one made of metal! That must be where the parts to fix the sand machines come from.
There's even a hang glider partially buried in the sand here; once the sun rises and heats up the sand, you might be able to use the glider and the hot air to get all the way up to the metal island!
While you wait for the sun to rise, you admire the oasis hidden here in the middle of Desert Island. It must have a delicate ecosystem; you might as well take some ecological readings while you wait. Maybe you can report any environmental instabilities you find to someone so the oasis can be around for the next sandstorm-worn traveler.
You pull out your handy Oasis And Sand Instability Sensor and analyze your surroundings. The OASIS produces a report of many values and how they are changing over time (your puzzle input). Each line in the report contains the history of a single value. For example:
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45

To best protect the oasis, your environmental report should include a prediction of the next value in each history. To do this, start by making a new sequence from the difference at each step of your history. If that sequence is not all zeroes, repeat this process, using the sequence you just generated as the input sequence. Once all of the values in your latest sequence are zeroes, you can extrapolate what the next value of the original history should be.
In the above dataset, the first history is 0 3 6 9 12 15. Because the values increase by 3 each step, the first sequence of differences that you generate will be 3 3 3 3 3. Note that this sequence has one fewer value than the input sequence because at each step it considers two numbers from the input. Since these values aren't all zero, repeat the process: the values differ by 0 at each step, so the next sequence is 0 0 0 0. This means you have enough information to extrapolate the history! Visually, these sequences can be arranged like this:
0   3   6   9  12  15
  3   3   3   3   3
    0   0   0   0

To extrapolate, start by adding a new zero to the end of your list of zeroes; because the zeroes represent differences between the two values above them, this also means there is now a placeholder in every sequence above it:
0   3   6   9  12  15   B
  3   3   3   3   3   A
    0   0   0   0   0

You can then start filling in placeholders from the bottom up. A needs to be the result of increasing 3 (the value to its left) by 0 (the value below it); this means A must be 3:
0   3   6   9  12  15   B
  3   3   3   3   3   3
    0   0   0   0   0

Finally, you can fill in B, which needs to be the result of increasing 15 (the value to its left) by 3 (the value below it), or 18:
0   3   6   9  12  15  18
  3   3   3   3   3   3
    0   0   0   0   0

So, the next value of the first history is 18.
Finding all-zero differences for the second history requires an additional sequence:
1   3   6  10  15  21
  2   3   4   5   6
    1   1   1   1
      0   0   0

Then, following the same process as before, work out the next value in each sequence from the bottom up:
1   3   6  10  15  21  28
  2   3   4   5   6   7
    1   1   1   1   1
      0   0   0   0

So, the next value of the second history is 28.
The third history requires even more sequences, but its next value can be found the same way:
10  13  16  21  30  45  68
   3   3   5   9  15  23
     0   2   4   6   8
       2   2   2   2
         0   0   0

So, the next value of the third history is 68.
If you find the next value for each history in this example and add them together, you get 114.
Analyze your OASIS report and extrapolate the next value for each history. What is the sum of these extrapolated values?

--- Part Two ---

Of course, it would be nice to have even more history included in your report. Surely it's safe to just extrapolate backwards as well, right?

For each history, repeat the process of finding differences until the sequence of differences is entirely zero. Then, rather than adding a zero to the end and filling in the next values of each previous sequence, you should instead add a zero to the beginning of your sequence of zeroes, then fill in new first values for each previous sequence.

In particular, here is what the third example history looks like when extrapolating back in time:

5  10  13  16  21  30  45
  5   3   3   5   9  15
   -2   0   2   4   6
      2   2   2   2
        0   0   0

Adding the new values on the left side of each sequence from bottom to top eventually reveals the new left-most history value: 5.

Doing this for the remaining example data above results in previous values of -3 for the first history and 0 for the second history. Adding all three new values together produces 2.

Analyze your OASIS report again, this time extrapolating the previous value for each history. What is the sum of these extrapolated values?
"""


def parse_raw_input(input: str):
    # return tuple(
    #     tuple(int(x) for x in line.strip()) for line in input.strip().split("\n")
    # )
    sequences = []

    for line in input.strip().split("\n"):
        seq = []
        for value in line.split():
            seq.append(int(value))
        sequences.append(seq)

    return sequences


def do(input, part: int):
    total = 0

    for sequence in input:
        diffs = []

        # Keep generating the sequence from the difference at each step
        seq = sequence
        while seq.count(0) != len(seq):
            diff = [v2 - v1 for v1, v2 in it.pairwise(seq)]
            diffs.append(diff)
            seq = diff

        diffs[-1].append(0)

        # "Extrapolate" each list
        # -2 to avoid the list of all zeroes that we just manually incremented
        for i in range(len(diffs) - 2, -1, -1):
            current_diff = diffs[i]
            prev_diff = diffs[i + 1]

            if part == 1:
                to_add = prev_diff[-1]
                add_to = current_diff[-1]
                diffs[i].append(add_to + to_add)
            elif part == 2:
                to_subtract = prev_diff[0]
                subtract_from = current_diff[0]
                diffs[i].insert(0, subtract_from - to_subtract)

        next_value = (
            sequence[-1] + diffs[0][-1] if part == 1 else sequence[0] - diffs[0][0]
        )
        total += next_value

    print(total)


def part1(input):
    do(input, 1)


def part2(input):
    do(input, 2)


def main():
    raw_input = utils.get_raw_input()
    #     raw_input = """0 3 6 9 12 15
    # 1 3 6 10 15 21
    # 10 13 16 21 30 45
    # """
    parsed_input = parse_raw_input(raw_input)

    part1(parsed_input)  # 2174807968
    part2(parsed_input)  # 1208


if __name__ == "__main__":
    main()
