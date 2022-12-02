from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

test_arr_1 = [
    [1,1,1,1,1],
    [1,9,9,9,1],
    [1,9,1,9,1],
    [1,9,9,9,1],
    [1,1,1,1,1]
]

test_arr_2 = [
    [5,4,8,3,1,4,3,2,2,3],
    [2,7,4,5,8,5,4,7,1,1],
    [5,2,6,4,5,5,6,1,7,3],
    [6,1,4,1,3,3,6,1,4,6],
    [6,3,5,7,3,8,5,4,7,8],
    [4,1,6,7,5,2,4,6,4,5],
    [2,1,7,6,8,4,1,7,2,1],
    [6,8,8,2,8,8,1,1,3,4],
    [4,8,4,6,8,4,8,5,5,4],
    [5,2,8,3,7,5,1,5,2,6],
]

class Group:
    def __init__(self, group):
        self.group = [[Octopus(i, j, group[i][j]) for j in range(len(group[0]))] for i in range(len(group))]
        self.flashes = 0
        # self.already_flashed = []

    def check_coords(self, coords):
        return (0 <= coords[0] < len(self.group)) and (0 <= coords[1] < len(self.group[0]))
    
    """
    You can model the energy levels and flashes of light in steps. During a single step, the following occurs:
    - The energy level of each octopus increases by 1.
    - Any octopus with energy greater than 9 'flashes':
        - This increases the energy level of all adjacent octopuses by 1, including diagonally adjacent octopuses
        - If this causes an octopus' energy to be greater than 9, it also flashes
        - This continues as long as new octopuses keep having their energy level increased beyond 9
        - ** (An octopus can only flash at most once per step) **
    - Any octopus that flashed has its energy level set to 0
    """

    def step(self):
        self.group = [[octopus.step() for octopus in row] for row in self.group]
    
    def check_group(self):
        flashed = []
        for i in range(len(self.group)):
            for j in range(len(self.group[0])):
                octopus = self.group[i][j]
                if octopus.energy < 9:
                    continue
                flashed.append(octopus.coords)
                octopus.energy = 0
                for adj_i, adj_j in octopus.surrounding():
                    try:
                        self.group[adj_i][adj_j].step()
                    except IndexError:
                        # print(octopus.coords, "-->", adj_i, adj_j)
                        # raise IndexError
                        continue
        # flashed += [octopus.coords for row in self.group for octopus in row if octopus.energy > 9]
        for coord in flashed:
            self.flashes += 1
            i, j = coord
            self.group[i][j].energy = 0
        # pp.pprint(self.out(True))
                    
    def check_group2(self):
        # print("Called check_group")
        for i in range(len(self.group)):
            for j in range(len(self.group[0])):
                # print("checking", (i,j))
                octopus = self.group[i][j]
                if octopus.energy >= 10:
                    if [i,j] in self.already_flashed:
                        continue
                    # print("flashing", (i,j), " - energy value", octopus.energy)
                    self.already_flashed.append([i,j])
                    octopus.energy = 0
                    print("Flashed", (i,j))
                    pp.pprint(self.out(True))
                    self.flashes += 1
                    surrounding_coords = [coord for coord in octopus.surrounding() if self.check_coords(coord)]
                    # print(surrounding_coords, "-->", len(surrounding_coords))
                    for coord in surrounding_coords:
                        surrounding_octopus = self.group[coord[0]][coord[1]]
                        surrounding_octopus.step()
                        print("Stepped", tuple(surrounding_octopus.coords))
                        pp.pprint(self.out(True))
                        # print("stepped surrounding octopus:", surrounding_octopus.coords, "to energy level", surrounding_octopus.energy)
                    
                # print()
        self.already_flashed = []
    
    def out(self, to_return=False, ij=False):
        arr = [[octopus.energy for octopus in row] for row in self.group]
        if ij:
            arr = [[(str(self.group[i][j].energy) if i == ij[0] and j == ij[1] else self.group[i][j].energy) for j in range(len(self.group[0]))] for i in range(len(self.group))]
        if to_return:
            return arr
        else:
            print(arr)

class Octopus:
    def __init__(self, i, j, energy):
        self.coords = [i, j]
        self.energy = energy
    
    def step(self):
        self.energy += 1
        return self
    
    def surrounding(self):
        i, j = self.coords
        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                yield [i + a, j + b]
    
def part1(inp):
    inp = test_arr_2
    group = Group(inp)

    pp.pprint(group.out(True))
    for _ in range(1):
        group.step()
        group.check_group()
        # print("-")
    print()
    pp.pprint(group.out(True))

    return group.flashes

def part2(inp):
    pass

def main():
    with open("./inputs/day11.txt") as infile:
        infile = [[int(num) for num in string] for string in infile.read().strip().split("\n")]
    
    print("Answer for part 1 =", part1(infile))
    print("Answer for part 2 =", part2(infile))

if __name__ == "__main__":
    main()
