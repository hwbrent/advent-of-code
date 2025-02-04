import os
import sys
from functools import cmp_to_key
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2024/day/5
# Input URL:   https://adventofcode.com/2024/day/5/input

"""
--- Day 5: Print Queue ---

Satisfied with their search on Ceres, the squadron of scholars suggests subsequently scanning the stationery stacks of sub-basement 17.
The North Pole printing department is busier than ever this close to Christmas, and while The Historians continue their search of this historically significant facility, an Elf operating a very familiar printer beckons you over.
The Elf must recognize you, because they waste no time explaining that the new sleigh launch safety manual updates won't print correctly. Failure to update the safety manuals would be dire indeed, so you offer your services.
Safety protocols clearly indicate that new pages for the safety manuals must be printed in a very specific order. The notation X|Y means that if both page number X and page number Y are to be produced as part of an update, page number X must be printed at some point before page number Y.
The Elf has for you both the page ordering rules and the pages to produce in each update (your puzzle input), but can't figure out whether each update has the pages in the right order.
For example:
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47

The first section specifies the page ordering rules, one per line. The first rule, 47|53, means that if an update includes both page number 47 and page number 53, then page number 47 must be printed at some point before page number 53. (47 doesn't necessarily need to be immediately before 53; other pages are allowed to be between them.)
The second section specifies the page numbers of each update. Because most safety manuals are different, the pages needed in the updates are different too. The first update, 75,47,61,53,29, means that the update consists of page numbers 75, 47, 61, 53, and 29.
To get the printers going as soon as possible, start by identifying which updates are already in the right order.
In the above example, the first update (75,47,61,53,29) is in the right order:

75 is correctly first because there are rules that put each other page after it: 75|47, 75|61, 75|53, and 75|29.
47 is correctly second because 75 must be before it (75|47) and every other page must be after it according to 47|61, 47|53, and 47|29.
61 is correctly in the middle because 75 and 47 are before it (75|61 and 47|61) and 53 and 29 are after it (61|53 and 61|29).
53 is correctly fourth because it is before page number 29 (53|29).
29 is the only page left and so is correctly last.

Because the first update does not include some page numbers, the ordering rules involving those missing page numbers are ignored.
The second and third updates are also in the correct order according to the rules. Like the first update, they also do not include every page number, and so only some of the ordering rules apply - within each update, the ordering rules that involve missing page numbers are not used.
The fourth update, 75,97,47,61,53, is not in the correct order: it would print 75 before 97, which violates the rule 97|75.
The fifth update, 61,13,29, is also not in the correct order, since it breaks the rule 29|13.
The last update, 97,13,75,29,47, is not in the correct order due to breaking several rules.
For some reason, the Elves also need to know the middle page number of each update being printed. Because you are currently only printing the correctly-ordered updates, you will need to find the middle page number of each correctly-ordered update. In the above example, the correctly-ordered updates are:
75,47,61,53,29
97,61,53,29,13
75,29,13

These have middle page numbers of 61, 53, and 29 respectively. Adding these page numbers together gives 143.
Of course, you'll need to be careful: the actual list of page ordering rules is bigger and more complicated than the above example.
Determine which updates are already in the correct order. What do you get if you add up the middle page number from those correctly-ordered updates?
"""

Rules = dict[tuple[set[str], set[str]]]
"""
a `dict`, where each key is a number that can appear in an update, and the
value is a tuple of two sets, where the first set contains the numbers
that should appear before this number, and the second set contains the
numbers that should appear after it

We use sets so that we can more easily check for overlap (`intersection`)
between the values in the rules and the actual values found in the updates
"""

Update = list[str]
Updates = list[Update]
"""
A `list` of `list`s of `str`s, where each `str` is numeric
"""

Input = tuple[Rules, Updates]


def parse_raw_input(input: str) -> Input:
    input = input.strip()

    # the two separate chunks of data
    raw_order_rules, raw_updates = input.split("\n\n")

    # each key will be a number, and each value will be a tuple of two lists,
    # where the first is the numbers that should appear before this number,
    # and the second is the numbers that should appear after this number
    rules = {}
    get_entry = lambda num: rules.get(num, (set(), set()))  # before/after

    for line in raw_order_rules.split("\n"):
        # each line is two numbers separated by a pipe.
        # if both numbers are in an update, the first number must appear
        # somewhere before the second
        before, after = line.split("|")

        # add 'after' to the set of numbers that should always be behind
        # 'before'
        entry__before = get_entry(before)
        entry__before[1].add(after)

        # add 'before' to the set of numbers that should always be in front
        # of 'after'
        entry__after = get_entry(after)
        entry__after[0].add(before)

        # add the updated entries back into 'rules'
        rules[before] = entry__before
        rules[after] = entry__after

    # each line is a comma-separated collection of integers (as strings)
    updates = [line.split(",") for line in raw_updates.split("\n")]

    return rules, updates


def is_incorrectly_ordered(update: Update, rules: Rules) -> bool:
    """
    Returns False if an 'update' is in the wrong order (and vice versa)
    according to 'rules'
    """
    for i, num in enumerate(update):
        # Get the surrounding values in the 'update' and put then into
        # corresponding sets
        update_before = set(update[:i])  # values before 'num'
        update_after = set(update[i + 1 :])  # values after 'num'

        # Get the orders that the rules dictate
        rule_before, rule_after = rules[num]

        # Check if there are any conflicts in terms of what the rules
        # expect versus what's actually in the data. We do this by finding
        # overlaps in the opposing sets of numbers (i.e. seeing if there
        # are any numbers from the 'before' set in 'rules' that appear
        # after 'num', and vice versa)
        overlap1 = rule_before.intersection(update_after)
        overlap2 = rule_after.intersection(update_before)

        # If the two sets have 1 or more entries, this entire 'update'
        # is invalid, so move onto the next 'update'
        overlap_count = len(overlap1) + len(overlap2)
        if overlap_count > 0:
            return True
    return False


def is_correctly_ordered(update: Update, rules: Rules) -> bool:
    """
    Returns True if an 'update' is in the wrong order (and vice versa)
    according to 'rules'
    """
    return not is_incorrectly_ordered(update, rules)


def get_middle_page_number(update: Update) -> int:
    """
    Given an 'update', this function finds the middle "page number" and
    returns it as an `int`
    """
    index = len(update) // 2
    string = update[index]
    integer = int(string)
    return integer


def part1(input: Input):
    rules, updates = input

    return sum(
        get_middle_page_number(update)
        for update in updates
        if is_correctly_ordered(update, rules)
    )


def part2(input):
    answer = 0

    rules, updates = input

    def compare(a, b):
        _, a_after = rules[a]
        b_before, _ = rules[b]
        if b in a_after:
            return -1
        if a in b_before:
            return 1
        return 0

    # Convert 'compare' so it can be passed as the 'key' callback to '.sort()'
    # or 'sorted()'
    sort_key = cmp_to_key(compare)

    for update in updates:
        # Skip updates already in order
        if is_correctly_ordered(update, rules):
            continue

        # Sort 'update' using 'compare'
        update.sort(key=sort_key)

        # Get the middle page number, and add it to answer
        answer += get_middle_page_number(update)

    return answer


def main():
    utils.handle(part1)  # 7365 (0.00547027587890625 seconds)
    utils.handle(part2)  # 5770 (0.00481104850769043 seconds)


if __name__ == "__main__":
    main()
