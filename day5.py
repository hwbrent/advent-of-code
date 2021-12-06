from pprint import PrettyPrinter
pp = PrettyPrinter(indent = 4)

class Diagram:
    def __init__(self, coordinates):
        # Below comprehension takes points from ['10,11 -> 989,990'] to [[10, 11], [989, 990]]
        self.coordinates = [[[int(num) for num in coord.split(",")] for coord in entry.split(" -> ")] for entry in coordinates]
        all_y_coords = {coord[1] for pair in self.coordinates for coord in pair}
        all_x_coords = {coord[0] for pair in self.coordinates for coord in pair}
        self.top_left = [min(all_x_coords), max(all_y_coords)]
        self.top_right = [max(all_x_coords), max(all_y_coords)]
        self.bottom_left = [min(all_x_coords), min(all_y_coords)]
        self.bottom_right = [max(all_x_coords), min(all_y_coords)]

        number_of_rows = max(all_y_coords) - min(all_y_coords)
        number_of_columns = max(all_x_coords) - min(all_x_coords)
        self.grid = [[0 for x in range(number_of_rows)] for y in range(number_of_columns)]
    
    def process_line(self, line_coordinates):
        pass


def part1():
    with open("./inputs/day5.txt") as infile:
        infile = infile.read().split("\n")[:-1] # length 500
    
    diagram = Diagram(infile)
    pp.pprint(diagram.grid)

    for line in diagram.coordinates:
        x1, y1 = line[0]
        x2, y2 = line[1]
        if not ((x1 == x2) or (y1 == y2)):
            continue
        else:
            # print(line)
            continue
    

def part2():
    pass

if __name__ == "__main__":
    part1()
    part2()