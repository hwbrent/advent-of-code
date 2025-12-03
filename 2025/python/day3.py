import os
import sys
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2025/day/3
# Input URL:   {input_url}

"""
--- Day 3: Lobby ---

You descend a short staircase, enter the surprisingly vast lobby, and are quickly cleared by the security checkpoint. When you get to the main elevators, however, you discover that each one has a red light above it: they're all offline.

"Sorry about that," an Elf apologizes as she tinkers with a nearby control panel. "Some kind of electrical surge seems to have fried them. I'll try to get them online soon."

You explain your need to get further underground. "Well, you could at least take the escalator down to the printing department, not that you'd get much further than that without the elevators working. That is, you could if the escalator weren't also offline."

"But, don't worry! It's not fried; it just needs power. Maybe you can get it running while I keep working on the elevators."

There are batteries nearby that can supply emergency power to the escalator for just such an occasion. The batteries are each labeled with their joltage rating, a value from 1 to 9. You make a note of their joltage ratings (your puzzle input). For example:

987654321111111
811111111111119
234234234234278
818181911112111

The batteries are arranged into banks; each line of digits in your input corresponds to a single bank of batteries. Within each bank, you need to turn on exactly two batteries; the joltage that the bank produces is equal to the number formed by the digits on the batteries you've turned on. For example, if you have a bank like 12345 and you turn on batteries 2 and 4, the bank would produce 24 jolts. (You cannot rearrange batteries.)

You'll need to find the largest possible joltage each bank can produce. In the above example:

    In 987654321111111, you can make the largest joltage possible, 98, by turning on the first two batteries.
    In 811111111111119, you can make the largest joltage possible by turning on the batteries labeled 8 and 9, producing 89 jolts.
    In 234234234234278, you can make 78 by turning on the last two batteries (marked 7 and 8).
    In 818181911112111, the largest joltage you can produce is 92.

The total output joltage is the sum of the maximum joltage from each bank, so in this example, the total output joltage is 98 + 89 + 78 + 92 = 357.

There are many batteries in front of you. Find the maximum joltage possible from each bank; what is the total output joltage?

--- Part Two ---

The escalator doesn't move. The Elf explains that it probably needs more joltage to overcome the static friction of the system and hits the big red "joltage limit safety override" button. You lose count of the number of times she needs to confirm "yes, I'm sure" and decorate the lobby a bit while you wait.

Now, you need to make the largest joltage by turning on exactly twelve batteries within each bank.

The joltage output for the bank is still the number formed by the digits of the batteries you've turned on; the only difference is that now there will be 12 digits in each bank's joltage output instead of two.

Consider again the example from before:

987654321111111
811111111111119
234234234234278
818181911112111

Now, the joltages are much larger:

    In 987654321111111, the largest joltage can be found by turning on everything except some 1s at the end to produce 987654321111.
    In the digit sequence 811111111111119, the largest joltage can be found by turning on everything except some 1s, producing 811111111119.
    In 234234234234278, the largest joltage can be found by turning on everything except a 2 battery, a 3 battery, and another 2 battery near the start to produce 434234234278.
    In 818181911112111, the joltage 888911112111 is produced by turning on everything except some 1s near the front.

The total output joltage is now much larger: 987654321111 + 811111111119 + 434234234278 + 888911112111 = 3121910778619.

What is the new total output joltage?
"""

Input = list[list[int]]


def parse_raw_input(input: str) -> Input:
    # input = """
    # 987654321111111
    # 811111111111119
    # 234234234234278
    # 818181911112111
    # """
    return [
        [int(battery) for battery in bank.strip()]
        for bank in input.strip().split(os.linesep)
    ]


def part1(batteries: Input) -> int:
    answer = 0

    for bank in batteries:
        # the joltage is basically just the biggest 2-digit number possible
        # from the batteries in the bank

        digit1 = max(bank[:-1])
        digit1_index = bank.index(digit1)

        digit2 = max(bank[digit1_index + 1 :])

        joltage = int(str(digit1) + str(digit2))

        answer += joltage

    return answer


def part2(batteries: Input) -> int:
    answer = 0

    JOLTAGE_DIGIT_COUNT = 12

    for bank in batteries:
        # print(bank)

        len_bank = len(bank)

        # this is the joltage value of the bank. we build it up by
        # concatenating digits and then converting to an int
        joltage_str = ""

        search_start_index = 0
        for joltage_digit_index in range(JOLTAGE_DIGIT_COUNT):
            # basically at every iteration, we just want to find the biggest
            # digit possible to add to 'joltage_digits' - this will result in
            # the joltage being the largest possible

            # we can only search for the max digit up to a certain point in
            # 'bank' because we need to reserve digits for subsequent joltage
            # digits to search+use.
            # if this is the 12th digit, we don't need to reserve digits.
            # if this is the 11th digit, we need to reserve 1 digit.
            # if this is the 10th digit, we need to reserve 2 digits.
            # etc

            digit_number = joltage_digit_index + 1

            num_digits_to_reserve = JOLTAGE_DIGIT_COUNT - digit_number
            search_end_index_incl = (
                len_bank - num_digits_to_reserve
            )  # up to, but not at

            search_area = bank[search_start_index:search_end_index_incl]

            reserved = bank[search_end_index_incl:]
            len_reserved = len(reserved)

            # grab the largest digit numerically in the available search
            # area and stick it on the end of the joltage number
            biggest_digit = max(search_area)
            joltage_str += str(biggest_digit)

            # ensure that the search area in the next iteration begins from
            # the digit after the one we just used in the joltage
            search_start_index = (
                search_start_index + search_area.index(biggest_digit) + 1
            )

            # print(
            #     "    ",
            #     digit_number,
            #     search_area,
            #     [reserved, len_reserved],
            #     biggest_digit,
            # )

        joltage = int(joltage_str)

        # print("    ", joltage)

        answer += joltage

        # break

    return answer


def main():
    utils.handle(part1)  # 17316           (0.003820180892944336 seconds)
    utils.handle(part2)  # 171741365473332 (0.005300045013427734 seconds)


if __name__ == "__main__":
    main()
