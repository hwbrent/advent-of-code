from utils import get_input
import re
import math
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
    '''
    • Starting items lists your worry level for each item the monkey is currently holding in the order they will be inspected.
    • Operation shows how your worry level changes as that monkey inspects an item. (An operation like new = old * 5 means that your worry level after the monkey inspected the item is five times whatever your worry level was before inspection.)
    • Test shows how the monkey uses your worry level to decide where to throw an item next.
        • If true shows what happens with an item if the Test was true.
        • If false shows what happens with an item if the Test was false.
    '''

    monkeys = parse_input(input)
    pp.pprint(monkeys)

    times_inspected = {i: 0 for i,_ in enumerate(monkeys)}

    for round in range(20):
        # if round != 0:
        #     break

        # Iterate through all the monkeys
        for monkey_index, monkey in enumerate(monkeys):

            times_inspected[monkey_index] += len(monkeys[monkey_index]['Starting items'])

            get_value_as_path = lambda item_index: f'monkeys[{monkey_index}]["Starting items"][{item_index}]'

            print('*'*30)
            print(monkey['Operation'])

            val_path = get_value_as_path(0)
            while len(eval(f'monkeys[{monkey_index}]["Starting items"]')) != 0:

                print(eval(val_path))

                # Update the value based on the operation in monkey['Operation'].
                operation = monkey['Operation'].replace('value', val_path)
                exec(operation)

                print(eval(val_path))

                # Divide by 3 and round down to nearest integer.
                div3_and_round = f'{val_path} = {math.floor(eval(val_path) / 3)}'
                exec(div3_and_round)

                print(eval(val_path))

                # Do test and figure out which monkey to throw new value to.
                test_outcome = eval(val_path) % monkey['Test']['divisible by'] == 0
                target_monkey = monkey['Test']['true'] if test_outcome == True else monkey['Test']['false']
                print('throw to monkey', target_monkey)
                exec(f'monkeys[{target_monkey}]["Starting items"].append({eval(val_path)})')

                exec(f'del {val_path}')
                print()

            # print(monkey['Starting items'])
            print()
    
        for monkey in monkeys:
            print(monkey['Starting items'])

        srtd = sorted(times_inspected.values())
        print(times_inspected)
        print(srtd)

        monkey_business_level = srtd[-2] * srtd[-1]
        print('Part 1 -->', monkey_business_level)

def part2(input):
    pass

''' ****************************************************************** '''

if __name__ == "__main__":
    # input = get_input()
    input = '''Monkey 0:
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
    part1(get_input())
    part2(input)
