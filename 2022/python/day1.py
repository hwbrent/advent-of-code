if __name__ == '__main__':
    with open('2022/inputs/day1.txt') as f:
        f = f.read()
        print('Part 1 --> ', max([sum([int(x) if x.isnumeric() else 0 for x in elf.split("\n")]) for elf in f.split("\n\n")]))
        print('Part 2 --> ', sum(sorted([sum([int(x) if x.isnumeric() else 0 for x in elf.split("\n")]) for elf in f.split("\n\n")])[-3:]))