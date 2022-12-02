from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)
# upper = lambda x: "".join([letter.toUpper() for letter in x])

def part1(infile):
    all_caves = list(set([cave for pair in infile for cave in pair]))

    big_caves = [cave for cave in all_caves if cave == cave.upper()]
    small_caves = [cave for cave in all_caves if cave == cave.lower()]

    connections = {}

    for cave in all_caves:
        connections[cave] = []
        for entry in infile:
            if cave in entry:
                other_cave = [c for c in entry if c != cave][0]
                # print(cave, entry, other_cave)
                if not other_cave in connections[cave]:
                    connections[cave].append(other_cave)
    
    # print(connections)

    paths = []

    def recurse(current_cave, visited = "", print_ = False):
        '''
        If current_cave == "end", add `visited` to `paths, and return`

        Find the caves that are connected to current_cave -- i.e. get connections[current_cave]
        For each cave, if it's small and it's already been visited, remove it. If it hasn't been visited or it's a big cave, leave it
        Recurse on each of the remaining caves
        '''
        visited += f",{current_cave}"
        if print_: print(visited)
        if ("end" in visited) and ("start" in visited):
            paths.append(visited)
            return
        adjacent_caves = []
        for cave in connections[current_cave]:
            if not ((cave in small_caves) and (cave in visited)):
                adjacent_caves.append(cave)
        if print_: print("adjacent caves:", adjacent_caves)
        for next_cave in adjacent_caves:
            recurse(next_cave, visited)
        
    recurse("start")

    # pp.pprint(paths)
    return len(paths)

def part2(infile):
    all_caves = list(set([cave for pair in infile for cave in pair]))
    big_caves = [cave for cave in all_caves if cave == cave.upper()]
    small_caves = [cave for cave in all_caves if cave == cave.lower()]

    # adjacency graph:
    connections = {cave: [subcave for entry in infile for subcave in entry if (cave in entry) and (subcave != cave)] for cave in all_caves}
    
    paths = []
    def recurse(current, visited = ""):
        visited += f"{current},"
        print(visited)
        
        if "end," in visited:
            paths.append(visited)
            return
        
        counts = []
        
        for next in connections[current]:
            # if the cave is a big cave, it's fine
            # if the cave is a small cave:
                # if it'
            continue

    recurse("start")
    pp.pprint(paths)
    
    # print(all_caves)
    # pp.pprint(connections)

    return len(paths)

def main():
    with open("./inputs/day12.txt") as infile:
        infile = [entry.split("-") for entry in infile.read().strip().split("\n")]
    
    print("Answer for part 1 =", part1(infile))
    print("Answer for part 2 =", part2(infile))

if __name__ == "__main__":
    main()
