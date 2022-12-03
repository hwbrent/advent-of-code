def part1(param):
    return min([sum([abs(num - point) for num in param]) for point in range(min(param), max(param) + 1)])

def part2(param):
    # really slow, but works
    return min([sum([sum(range(1, abs(num - point) + 1)) for num in param]) for point in range(min(param), max(param) + 1)])

def main():
    with open("./inputs/day7.txt") as infile:
        infile = [int(number) for number in infile.read().split(",")]
    
    print("Answer for part 1 =", part1(infile))
    print("Answer for part 2 =", part2(infile))

if __name__ == "__main__":
    main()
