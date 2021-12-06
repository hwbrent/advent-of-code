def part1(infile):
    lower = 0
    upper = 1
    increase_count = 0
    while upper < len(infile):
        if int(infile[lower]) < int(infile[upper]):
            increase_count += 1
        lower += 1
        upper += 1
    return increase_count

def part2(infile):
    lower = 0
    upper = 3
    increase_count = 0
    prev_window = 0
    while upper < len(infile) + 1: # the +1 accounts for the fact that the element at index `upper` is left out of `window` 
        window = [int(number) for number in infile[lower:upper]]
        if sum(window) > prev_window:
            increase_count += 1
        prev_window = sum(window)
        lower += 1
        upper += 1
    return increase_count - 1

def main():
    with open("./inputs/day1.txt") as infile:
        infile = infile.read().split("\n")[:-1]

    print("Answer for part 1 =", part1(infile))
    print("Answer for part 2 =", part2(infile))

if __name__ == "__main__":
    main()
    