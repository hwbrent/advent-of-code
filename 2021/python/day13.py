from utils import get_input
import re
import copy
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

def get_dots(raw_dots):
    dots = list()
    for line in raw_dots.split("\n"):
        dots.append([int(num) for num in re.findall(r"\d+",line)])
    return dots

def get_folds(raw_folds):
    folds = list()
    for line in raw_folds.split("\n"):
        yorx = re.search(r"(y|x)",line)[0]
        num = int(re.search(r"\d+",line)[0])
        folds.append(
            (0 if yorx == 'x' else 1, num)
        )
    return folds

def part1(raw_dots, raw_folds):
    dots = get_dots(raw_dots)
    folds = get_folds(raw_folds)

    print(len(dots))

    dots_after = set()

    for fold_index, fold in enumerate(folds):
        if fold_index != 0:
            break

        xory, num = fold

        # fold UP for y --> any y value bigger than the fold line gets "reflected"
        # fold LEFT for x --> any x value bigger than the fold line gets "reflected"

        for dot_index, dot in enumerate(dots):

            if dot[xory] > num:

                print(dot,'\t', 'x' if xory == 0 else 'y','\t', num)
                diff = abs(dot[xory] - num)
                print(diff)

                dot[xory] = num - (dot[xory] - num)

                print(dot,'\t', 'x' if xory == 0 else 'y','\t', num)
                print()
            
            dots_after.add(tuple(dot))

    print('Part 1 -->', len(dots_after))

def part2(input):
    pass

if __name__ == "__main__":
    raw_dots, raw_folds = get_input().strip().split("\n\n")
    part1(raw_dots,raw_folds)
    part2(input)
