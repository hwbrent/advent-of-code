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
"""


def parse_raw_input(input: str):
    symbols = {
        # e.g.:
        # (138, 105): {(138, 105), (139, 106), (137, 104)},
        # (138, 108): {(137, 107), (139, 109), (138, 108)},
        # (138, 115): {(138, 115), (137, 114), (139, 116)},
        # ...
    }
    numbers = {
        # e.g.:
        # (139, 52): 261,
        # (139, 53): 261,
        # (139, 54): 261,
        # (139, 84): 42,
        # (139, 85): 42}
        # ...
    }

    rows = input.strip().split("\n")
    rows_range = range(0, len(rows))
    cols_range = range(0, len(rows[0]))

    for row_index, row in enumerate(rows):
        # For each coord in this row where there's a number, add an entry to
        # 'numbers' saying what the full number is
        for result in re.finditer(r"\d+", row):
            num_str = result[0]
            num_int = int(num_str)
            cols_spanned = tuple(range(*result.span()))
            for col in cols_spanned:
                coord = (row_index, col)
                # numbers[coord] = num_str
                numbers[coord] = num_int

        for col_index, char in enumerate(row):
            if char.isnumeric() or char == ".":
                continue

            # Get the coordinates of every point surrounding this symbol

            surrounding_coords = []

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

    return symbols, numbers, input.strip()


def part1(input):
    symbols, numbers, input = input

    # print(pp.pprint(numbers))

    # pp.pprint(symbols)
    # for row in symbols:
    #     print(list(row))
    #     print()


def part2(input):
    pass


def main():
    raw_input = utils.get_raw_input()
    parsed_input = parse_raw_input(raw_input)

    part1(parsed_input)
    part2(parsed_input)


if __name__ == "__main__":
    main()
