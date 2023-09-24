from utils import get_input
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Puzzle description: https://adventofcode.com/2022/day/10
# Puzzle input:       https://adventofcode.com/2022/day/10/input


def parse(raw_input):
    for line in raw_input.strip().split("\n"):
        line = line.split()
        if len(line) == 2:
            line[1] = int(line[1])
        yield line


def check_add(cycle, X):
    return cycle * X if cycle % 40 == 20 else 0


def pixel(cycle, X):
    X_range = range(X - 1, X + 2)
    pixel_row_index = (cycle % 40) - 1
    pixel_char = "#" if pixel_row_index in X_range else "."
    prefix = "\n" if cycle % 40 == 1 else ""
    return prefix + pixel_char


def part1(input):
    X = 1
    cycle = 1

    signal_strengths_total = 0

    crt = ""

    for line in input:
        if line[0] == "noop":

            signal_strengths_total += check_add(cycle, X)
            crt += pixel(cycle, X)

            cycle += 1

        elif line[0] == "addx":

            signal_strengths_total += check_add(cycle, X)
            crt += pixel(cycle, X)

            cycle += 1

            signal_strengths_total += check_add(cycle, X)
            crt += pixel(cycle, X)
            X += line[1]

            cycle += 1

    signal_strengths_total += check_add(cycle, X)

    print(f"\nPart 1 --> {signal_strengths_total}")

    print("\nPart 2 \u2193\n", crt, "\n")


# fmt: off
examples = (
    "noop\naddx 3\naddx -5\n",
    "addx 15\naddx -11\naddx 6\naddx -3\naddx 5\naddx -1\naddx -8\naddx 13\naddx 4\nnoop\naddx -1\naddx 5\naddx -1\naddx 5\naddx -1\naddx 5\naddx -1\naddx 5\naddx -1\naddx -35\naddx 1\naddx 24\naddx -19\naddx 1\naddx 16\naddx -11\nnoop\nnoop\naddx 21\naddx -15\nnoop\nnoop\naddx -3\naddx 9\naddx 1\naddx -3\naddx 8\naddx 1\naddx 5\nnoop\nnoop\nnoop\nnoop\nnoop\naddx -36\nnoop\naddx 1\naddx 7\nnoop\nnoop\nnoop\naddx 2\naddx 6\nnoop\nnoop\nnoop\nnoop\nnoop\naddx 1\nnoop\nnoop\naddx 7\naddx 1\nnoop\naddx -13\naddx 13\naddx 7\nnoop\naddx 1\naddx -33\nnoop\nnoop\nnoop\naddx 2\nnoop\nnoop\nnoop\naddx 8\nnoop\naddx -1\naddx 2\naddx 1\nnoop\naddx 17\naddx -9\naddx 1\naddx 1\naddx -3\naddx 11\nnoop\nnoop\naddx 1\nnoop\naddx 1\nnoop\nnoop\naddx -13\naddx -19\naddx 1\naddx 3\naddx 26\naddx -30\naddx 12\naddx -1\naddx 3\naddx 1\nnoop\nnoop\nnoop\naddx -9\naddx 18\naddx 1\naddx 2\nnoop\nnoop\naddx 9\nnoop\nnoop\nnoop\naddx -1\naddx 2\naddx -37\naddx 1\naddx 3\nnoop\naddx 15\naddx -21\naddx 22\naddx -6\naddx 1\nnoop\naddx 2\naddx 1\nnoop\naddx -10\nnoop\nnoop\naddx 20\naddx 1\naddx 2\naddx 2\naddx -6\naddx -11\nnoop\nnoop\nnoop"
)
# fmt: on


if __name__ == "__main__":
    input = parse(get_input())
    # input = parse(examples[0])
    # input = parse(examples[1])
    part1(input)
