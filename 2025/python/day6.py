import numpy as np

import os
import sys
import itertools as it
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
    #     input = """
    # 123 328  51 64
    #  45 64  387 23
    #   6 98  215 314
    # *   +   *   +
    #     """

    # remove any newlines from the left of the input, but not general
    # whitespace as it could affect the alignment of the numbers
    input = input.lstrip(os.linesep)

    # remove any whitespace at all from the right of the input. this will
    # only affect the operator line which doesnt make a difference
    input = input.rstrip()

    rows = input.split(os.linesep)

    # get the indices of the operators. this is where each column starts
    operator_row = rows[-1]
    operator_indices = [i for i, char in enumerate(operator_row) if char.strip()]

    # obviously the last column ends at the end of the line. so add the index of the
    # end of the line so that we can calculate the final range
    operator_indices.append(len(rows[0]))

    # configure each col's bounds to start at the index of the current
    # operator and end at the index before the next operator
    col_bounds = list(it.pairwise(operator_indices))

    problems = []
    for lower, upper in col_bounds:
        operands = [row[lower:upper] for row in rows]

        operator = operands.pop().strip()

        problem = [operands, operator]

        problems.append(problem)

    return problems


to_int = lambda x: int(x.strip())
map_to_int = np.vectorize(to_int)


def do_operation(operands: Operands, operator: Operator) -> int:
    operands = map_to_int(operands)
    match operator:
        case "*":
            return np.prod(operands)
        case "+":
            return np.sum(operands)
    return 0


def part1(problems: Problems) -> int:
    return sum(do_operation(*problem) for problem in problems)


def part2(problems: Problems) -> int:
    answer = 0

    for problem in problems[::-1]:
        old_operands, operator = problem

        old_operands = [s.replace(" ", "0") for s in old_operands]

        # get new operands by reading each operand right to left and using
        # each digit
        new_operands = []
        length = len(old_operands[0])
        for i in range(length - 1, -1, -1):  # right to left
            num_str = "".join([operand[i] for operand in old_operands])

            num_str = num_str.rstrip("0")  # ?

            if num_str != "":
                new_operands.append(num_str)

        result = do_operation(new_operands, operator)

        answer += result

    return answer


def main():
    utils.handle(part1)  # 5667835681547 (0.009466171264648438 seconds)
    utils.handle(part2)  # 9434900032651 (0.026433944702148438 seconds)


if __name__ == "__main__":
    main()
