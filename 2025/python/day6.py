import os
import sys
from typing import Any
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2025/day/6
# Input URL:   https://adventofcode.com/2025/day/6/input

Operands = list[int]
Operator = str
Problem = tuple[Operands, Operator]
Problems = list[Problem]


def parse_raw_input(input: str) -> Problems:
    input = """
    123 328  51 64 
    45 64  387 23 
    6 98  215 314
    *   +   *   +  
    """

    rows = [row.split() for row in input.strip().split(os.linesep)]
    cols = [[row[col_number] for row in rows] for col_number in range(len(rows[0]))]

    problems = [
        ([int(num) for num in cols[i][:-1]], cols[i][-1]) for i in range(len(cols))
    ]

    return problems


def part1(problems: Problems) -> int:
    answer = 0
    return answer


def part2(problems: Problems) -> int:
    answer = 0
    return answer


def main():
    utils.handle(part1)
    utils.handle(part2)


if __name__ == "__main__":
    main()
