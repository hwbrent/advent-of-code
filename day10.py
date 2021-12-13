def part1(inp):
    """
    A corrupted line is one where a chunk closes with the wrong character - that is, where the characters
    it opens and closes with do not form one of the four legal pairs listed above.
    """
    # Accepted chars:
    brackets = [
        ["(", ")"],
        ["[", "]"],
        ["{", "}"],
        ["<", ">"],
    ]
    for line in inp:
        flag = True
        for bracket_type in brackets:
            opening = bracket_type[0]
            closing = bracket_type[1]
            print(line.count(opening), "-", line.count(closing))
            if not line.count(opening) == line.count(closing):
                flag = False
        print()
            
    print(len(inp))

def part2(inp):
    pass

def main():
    with open("./inputs/day10.txt") as infile:
        infile = infile.read().strip().split("\n")
    
    print("Answer for part 1 =", part1(infile))
    print("Answer for part 2 =", part2(infile))

if __name__ == "__main__":
    main()
