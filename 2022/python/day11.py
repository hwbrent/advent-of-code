from utils import get_input
import re
import math
import time
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

def parse_input(input):
    out = list()

    for index, monkey in enumerate(input.split("\n\n")):
        monkey = monkey.strip().split("\n")

        starting_items = [int(x) for x in re.findall(r'\d+', monkey[1])]

        # use `exec` wth this
        operation = monkey[2].strip() \
            .replace('Operation: ' , '') \
            .replace('new', 'value') \
            .replace('old', 'value')
        
        # Test details
        test_condition = int(re.search(r'\d+', monkey[-3])[0])
        true_case = int(re.search(r'\d+', monkey[-2])[0])
        false_case = int(re.search(r'\d+', monkey[-1])[0])

        out.append({
            'Starting items': starting_items,
            'Operation': operation,
            'Test': {
                'divisible by': test_condition,
                'true': true_case,
                'false': false_case
            }
        })

    return out

def part1(input):
    monkeys = parse_input(input)

    # Each value corresponds to the monkey with number equal to the index of the value.
    # i.e. times_inspected[2] holds the value for monkey 2
    times_inspected = [0 for _ in monkeys]

    for round in range(20):

        # Iterate through all the monkeys
        for monkey_index, monkey in enumerate(monkeys):

            times_inspected[monkey_index] += len(monkeys[monkey_index]['Starting items'])

            def get_val():
                return monkeys[monkey_index]["Starting items"][0]
            def set_val(v):
                monkeys[monkey_index]["Starting items"][0] = v

            # Not really "iterating" per se. More like working with the first element
            # of the list, then removing it, and repeating until there are no more
            # elements in the list to work with.
            while len(monkeys[monkey_index]["Starting items"]) != 0:

                # Update worry level per the operation provided.
                exec(monkey['Operation'].replace('value', f'monkeys[{monkey_index}]["Starting items"][0]'))

                # Divide worry level by 3 and round down to nearest integer.
                set_val(math.floor(get_val() / 3))

                # Do test and figure out which monkey to throw new worry level to.
                test_outcome = get_val() % monkey['Test']['divisible by'] == 0
                target_monkey = monkey['Test']['true'] if test_outcome == True else monkey['Test']['false']
                monkeys[target_monkey]["Starting items"].append(get_val())

                del monkeys[monkey_index]["Starting items"][0]

    times_inspected.sort()
    monkey_business_level = times_inspected[-2] * times_inspected[-1]
    print('Part 1 -->', monkey_business_level)

def part2(input):
    ''' Credit to this comment on Reddit: https://www.reddit.com/r/adventofcode/comments/zifqmh/comment/izuixs4/?utm_source=share&utm_medium=web2x&context=3 '''
    start = time.time()
    monkeys = parse_input(input)

    divisible_bys = [monkey['Test']['divisible by'] for monkey in monkeys]
    lcm = math.lcm(*divisible_bys)

    # Each value corresponds to the monkey with number equal to the index of the value.
    # i.e. times_inspected[2] holds the value for monkey 2
    times_inspected = [0 for _ in monkeys]

    for round in range(10_000):

        # Iterate through all the monkeys
        for monkey_index, monkey in enumerate(monkeys):

            times_inspected[monkey_index] += len(monkeys[monkey_index]['Starting items'])

            def get_val():
                return monkeys[monkey_index]["Starting items"][0]
            def set_val(v):
                monkeys[monkey_index]["Starting items"][0] = v

            # Not really "iterating" per se. More like working with the first element
            # of the list, then removing it, and repeating until there are no more
            # elements in the list to work with.
            while len(monkeys[monkey_index]["Starting items"]) != 0:

                # Update worry level per the operation provided.
                exec(monkey['Operation'].replace('value', f'monkeys[{monkey_index}]["Starting items"][0]'))

                # Reduce worry level to manageable level.
                # https://www.reddit.com/r/adventofcode/comments/zifqmh/comment/izuixs4/?utm_source=share&utm_medium=web2x&context=3
                set_val(
                    # math.floor(get_val() / 3)
                    # math.floor(math.log(get_val()))
                    # math.floor(math.sqrt(get_val()))
                    get_val() % lcm
                )

                # Do test and figure out which monkey to throw new worry level to.
                test_outcome = get_val() % monkey['Test']['divisible by'] == 0
                target_monkey = monkey['Test']['true'] if test_outcome == True else monkey['Test']['false']
                monkeys[target_monkey]["Starting items"].append(get_val())

                del monkeys[monkey_index]["Starting items"][0]

    times_inspected.sort()
    monkey_business_level = times_inspected[-2] * times_inspected[-1]
    # with math.log  --> 14400600004 --> too low
    # with math.sqrt --> 14400720005 --> too low

    finish = time.time()
    print(f'Part 2 --> {monkey_business_level} \t ({finish-start} seconds)')

''' ****************************************************************** '''

if __name__ == "__main__":
    input = get_input()

    example = '''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
    '''

    part1(input)
    part2(input) # (time: 11.930435180664062 seconds)
