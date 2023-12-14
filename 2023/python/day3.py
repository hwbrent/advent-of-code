import os
import sys
import re
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2023/day/3
# Input URL:   https://adventofcode.com/2023/day/3/input

"""
--- Day 3: Gear Ratios ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.
It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.
"Aaah!"
You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.
The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.
The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)
Here is an example engine schematic:
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.
Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

--- Part Two ---

The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?

"""


def parse_raw_input(input: str):
    # key=xy coordinate, value=nested list of tuples of neighbouring coords
    symbols = {}

    # key=xy coordinate, value=the index of the Match object in 'matches'
    numbers = {}

    # Collection of unique re.Match objects. We need this so that we only
    # account for each number in the engine schematic once
    matches = []

    input = input.strip().split("\n")
    rows = input

    rows_range = range(0, len(rows))
    cols_range = range(0, len(rows[0]))

    for row_index, row in enumerate(rows):
        # Find all the part numbers in the row
        for result in re.finditer(r"\d+", row):
            # For each "column" that the part number spans, add an entry to
            # 'matches' with the Match object representing the number that
            # was found, and add an entry to 'numbers' which points to the
            # aforementioned unique Match object
            cols_spanned = tuple(range(*result.span()))
            for col in cols_spanned:
                if not result in matches:
                    matches.append(result)
                numbers[(row_index, col)] = len(matches) - 1

        for col_index, char in enumerate(row):
            # If the character is a number or an empty space (i.e. a full
            # stop), do nothing
            if char.isnumeric() or char == ".":
                continue

            surrounding_coords = []

            # Collect all the coordinates of the points neighbouring this
            # one.
            for i in range(-1, 2):
                surrounding_row_index = row_index + i
                if not row_index in rows_range:
                    continue

                for j in range(-1, 2):
                    surrounding_col_index = col_index + j
                    if not col_index in cols_range:
                        continue

                    if i == j == 0:
                        continue

                    surrounding_coords.append(
                        (surrounding_row_index, surrounding_col_index)
                    )

            symbols[(row_index, col_index)] = surrounding_coords

    return symbols, numbers, matches, input


def part1(input):
    symbols, numbers, matches, input = input

    total = 0

    for symbol, neighbours in symbols.items():
        # The indices of the Match objects whose numbers we have already
        # added to 'total'.
        part_numbers_added = []

        for neighbour in neighbours:
            # Check if one of the digits of a part number can be found
            # at this coord
            match_index = numbers.get(neighbour, None)
            if not match_index:
                continue

            # Check if the part number has already been accounted for
            # and added to 'total'
            if match_index in part_numbers_added:
                continue

            # Get the actual integer of the part number from the Match
            # object, and add it to 'total'
            number = int(matches[match_index][0])
            total += number

            # Record the fact that we just accounted for this specific
            # part number
            part_numbers_added.append(match_index)

    print(total)

    # 839370 -- too high


def part2(input):
    symbols, numbers, matches, input = input

    overall_total = 0

    for symbol_coord in symbols:
        # Check if the actual symbol character is an asterisk - if not, do
        # nothing
        symbol_row, symbol_col = symbol_coord
        symbol = input[symbol_row][symbol_col]
        if symbol != "*":
            continue

        gear_ratio = 1

        # The coordinates of the points surrounding this particular asterisk
        neighbours = symbols[symbol_coord]

        # A list of unique indices pointing to Match objects in 'matches'
        # whose values we have already factored into 'gear_ratio'
        part_numbers_added = []

        for neighbour in neighbours:
            # If this specific neighbour doesn't lie on a digit of one
            # of the part numbers, don't do anything
            match_index = numbers.get(neighbour, None)
            if not match_index:
                continue

            # If we've already accounted for this part number, do nothing
            if match_index in part_numbers_added:
                continue

            # Get the actual number that the Match object represents,
            # and use it to calculate this gear's gear ratio
            number = int(matches[match_index][0])
            gear_ratio *= number

            # Record the fact that we just accounted for this specific
            # part number
            part_numbers_added.append(match_index)

        # If this year doesn't have exactly two part numbers, it's not valid,
        # so don't add its gear ratio to the overall sum
        if len(part_numbers_added) != 2:
            continue

        overall_total += gear_ratio

    print(overall_total)


def main():
    raw_input = utils.get_raw_input()
    parsed_input = parse_raw_input(raw_input)

    part1(parsed_input)  # 522726
    part2(parsed_input)  # 81721933


if __name__ == "__main__":
    main()
