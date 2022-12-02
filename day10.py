def part1(inp):
    inp = [
        "{([(<{}[<>[]}>{[]{[(<()>",
        "[[<[([]))<([[{}[[()]]]",
        "[{[{({}]{}}([{[{{{}}([]",
        "[<(<(<(<{}))><([]([]()",
        "<{([([[(<>()){}]>(<<{{"
    ]
    for line in inp:
        print(line.count("("), line.count(")"))
        print(line.count("["), line.count("]"))
        print(line.count("{"), line.count("}"))
        print()
    
    # pass

def part2(inp):
    pass

def main():
    with open("./inputs/day10.txt") as infile:
        infile = infile.read().strip().split("\n")
    
    print("Answer for part 1 =", part1(infile))
    print("Answer for part 2 =", part2(infile))

if __name__ == "__main__":
    main()
