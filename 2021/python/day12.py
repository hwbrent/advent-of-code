from utils import get_input

from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

def get_conns(cave_pairs: 'list[str,str]') -> 'dict[str:list]':
    ''' Returns a `dict` containing info on which caves are connected. '''

    conns = dict()

    def add_pair(cave1,cave2):
        if not cave1 in conns.keys():
            conns[cave1] = []
        conns[cave1].append(cave2)

    for cave1, cave2 in cave_pairs:
        add_pair(cave1,cave2)
        add_pair(cave2,cave1)
    
    return conns

def is_small(cave: 'str'):
    for char in cave:
        if char.isupper():
            return False
    return True

def part1(input):
    conns = get_conns(input)
    paths = []

    def recurse(cave, path=['start']):
        if cave == 'end':
            path.append('end')
            if not path in paths:
                paths.append(path)
            return
        else:
            for next_cave in conns[cave]:
                if not (next_cave in path and is_small(next_cave)):
                    recurse(next_cave, [*path, next_cave])

    recurse('start')

    print('Part 1 -->', len(paths))

def part2(input):
    pass

if __name__ == "__main__":
    input = [cave_pair.split('-') for cave_pair in get_input().strip().split("\n")]
    part1(input)
    part2(input)
