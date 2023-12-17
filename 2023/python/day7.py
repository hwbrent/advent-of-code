import os
import sys
import itertools as it

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: https://adventofcode.com/2023/day/7
# Input URL:   https://adventofcode.com/2023/day/7/input

"""
--- Day 7: Camel Cards ---

Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship. (At least it's a cool airship!) It drops you off at the edge of a vast desert and descends back to Island Island.
"Did you bring the parts?"
You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding a large camel.
"Did you bring the parts?" she asks again, louder this time. You aren't sure what parts she's looking for; you're here to figure out why the sand stopped.
"The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.
After riding a bit across the sands of Desert Island, you can see what look like very large rocks covering half of the horizon. The Elf explains that the rocks are all along the part of Desert Island that is directly above Island Island, making it hard to even get there. Normally, they use big machines to move the rocks and filter the sand, but the machines have broken down because Desert Island recently stopped receiving the parts they need to fix the machines.
You've already assumed it'll be your job to figure out why the parts stopped when she asks if you can help. You agree automatically.
Because the journey will take a few days, she offers to teach you the game of Camel Cards. Camel Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.
In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.
Every hand is exactly one type. From strongest to weakest, they are:

Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456

Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.
If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.
So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).
To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.
So, the first step is to put the hands in order of strength:

32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.

Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.
Find the rank of every hand in your set. What are the total winnings?

--- Part Two ---

To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

    32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
    KK677 is now the only two pair, making it the second-weakest hand.
    T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.

With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?
"""


def parse_raw_input(input: str):
    only_hands = []
    pairs = {}
    for line in input.strip().split("\n"):
        cards, bid = line.split()

        # cards = tuple(char for char in cards)
        bid = int(bid)

        only_hands.append(cards)
        pairs[cards] = int(bid)

    return only_hands, pairs


def counts(hand: str, part: int) -> list:
    label_counts = sorted(hand.count(card) for card in set(hand))

    if part == 1:
        return label_counts

    jokers = hand.count("J")

    # If we don't include (jokers == 5), when we encounter a hand with only
    # jokers, we encounter an error, because after you do label_counts.remove(jokers)
    # there will be no elements left in the list
    if (jokers == 0) or (jokers == 5):
        return label_counts

    # Remove the jokers, and turn them into whatever the most frequently
    # occuring label is
    label_counts.remove(jokers)

    max_occurring = label_counts.index(max(label_counts))
    label_counts[max_occurring] += jokers

    label_counts.sort()

    return label_counts


funcs = {
    # five of a kind
    # where all five cards have the same label: AAAAA
    "five of a kind": (lambda hand, part: counts(hand, part) == [5]),
    # four of a kind
    # where four cards have the same label and one card has a different label: AA8AA
    "four of a kind": (lambda hand, part: counts(hand, part) == [1, 4]),
    # full house
    # where three cards have the same label, and the remaining two cards share a different label: 23332
    "full house": (lambda hand, part: counts(hand, part) == [2, 3]),
    # three of a kind
    # where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    "three of a kind": (lambda hand, part: counts(hand, part) == [1, 1, 3]),
    # two pair
    # where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    "two pair": (lambda hand, part: counts(hand, part) == [1, 2, 2]),
    # one pair
    # where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    "one pair": (lambda hand, part: counts(hand, part) == [1, 1, 1, 2]),
    # high card
    # where all cards' labels are distinct: 23456
    "high card": (lambda hand, part: counts(hand, part) == [1, 1, 1, 1, 1]),
}


def get_labels(part: int):
    if part == 1:
        return ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    return ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


def get_hand_rank(hand: str, part: int) -> int:
    """
    Gets the strength of this hand purely in terms of the hand type
    """
    for index, (hand_type, hand_checker) in enumerate(funcs.items()):
        if hand_checker(hand, part):
            return hand_type, len(funcs) - index


def group(arr, key):
    arr2 = []
    for _, value in it.groupby(arr, key):
        group = list(value)
        if len(group) == 1:
            group = group[0]
        arr2.append(group)
    return arr2


def do(input, part) -> int:
    only_hands, pairs = input

    # print(only_hands)

    # First, sort by the strength of the hand solely
    only_hands.sort(key=lambda x: get_hand_rank(x, part)[1])

    # print(only_hands)

    # Group hands with same hand strength into lists, so that we can easily
    # iterate over the list to figure out the order between them
    only_hands = group(only_hands, key=lambda x: get_hand_rank(x, part)[1])

    # Sort by card suit
    for index, entry in enumerate(only_hands):
        if type(entry) != list:
            continue

        entry.sort(key=lambda x: tuple(len(x) - get_labels(part).index(c) for c in x))

        # print(only_hands[index])

        del only_hands[index]

        # We have to order them in reversed order so that they end up in
        # the list in the correct order
        for value in reversed(entry):
            only_hands.insert(index, value)

    total = 0

    # Now get each hand's bid, and multiply it by its rank, then add that to
    # our overall total
    for index, hand in enumerate(only_hands):
        bid = pairs[hand]
        total += (index + 1) * bid

    return total


def part1(input):
    print(do(input, 1))


def part2(input):
    print(do(input, 2))


def main():
    raw_input = utils.get_raw_input()
    #     raw_input = """32T3K 765
    # T55J5 684
    # KK677 28
    # KTJJT 220
    # QQQJA 483
    # """
    parsed_input = parse_raw_input(raw_input)

    part1(parsed_input)  # 252052080
    part2(parsed_input)  # 252898370


if __name__ == "__main__":
    main()
