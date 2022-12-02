from utils import get_input

if __name__ == '__main__':
    print('Part 1 --> ', max([sum([int(x) if x.isnumeric() else 0 for x in elf.split("\n")]) for elf in get_input().split("\n\n")]))
    print('Part 2 --> ', sum(sorted([sum([int(x) if x.isnumeric() else 0 for x in elf.split("\n")]) for elf in get_input().split("\n\n")])[-3:]))