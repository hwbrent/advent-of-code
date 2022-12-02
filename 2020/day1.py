# Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.
# In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces
# 1721 * 299 = 514579, so the correct answer is 514579. Of course, your expense report is much larger. Find the two
# entries that sum to 2020; what do you get if you multiply them together?

import re
import os

def part1():
    with open("./inputs/day1.txt") as file:
        file = file.read().split("\n")
        for x in range(len(file)):
            for y in range(len(file)):
                if x == y:
                    continue
                x_int = int(file[x])
                y_int = int(file[y])
                if x_int + y_int == 2020:
                    print(x_int*y_int)
                    return

def part2():
    with open("./inputs/day1.txt") as file:
        file = file.read().split("\n")
        for x in range(len(file)):
            for y in range(len(file)):
                for z in range(len(file)):
                    if (x == y) or (y == z) or (x == z):
                        continue
                    x_int = int(file[x])
                    y_int = int(file[y])
                    z_int = int(file[z])
                    # print(x_int)
                    # print(y_int)
                    # print(z_int)
                    if x_int + y_int + z_int == 2020:
                        print(x_int*y_int*z_int)
                        return

part2()