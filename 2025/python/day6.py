import numpy as np

import os
import sys
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2025/day/6
# Input URL:   https://adventofcode.com/2025/day/6/input

Operands = np.ndarray
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

    print(repr(input))

    # remove any newlines from the left of the input, but not general
    # whitespace as it could affect the alignment of the numbers
    input = input.lstrip(os.linesep)

    # remove any whitespace at all from the right of the input. this will
    # only affect the operator line which doesnt make a difference
    input = input.rstrip()

    rows = input.split(os.linesep)
    pp.pprint(rows)

    # rows = input.split(os.linesep)
    # for row in rows:
    #     if row.strip() == "":
    #         continue
    #     print(row.split(" "))
    # pp.pprint(rows)
    quit()

    return problems


to_int = lambda x: int(x)
map_to_int = np.vectorize(to_int)


def part1(problems: Problems) -> int:
    answer = 0

    # for problem in problems:
    #     result = 0

    #     operands, operator = problem

    #     operands = map_to_int(operands)

    #     match operator:
    #         case "*":
    #             result = np.prod(operands)
    #         case "+":
    #             result = np.sum(operands)

    #     answer += result

    return answer


def part2(problems: Problems) -> int:
    answer = 0
    return answer


def main():
    utils.handle(part1)  # 5667835681547 (0.009466171264648438 seconds)
    utils.handle(part2)


if __name__ == "__main__":
    main()
