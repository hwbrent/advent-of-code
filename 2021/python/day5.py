from pprint import PrettyPrinter
import math
pp = PrettyPrinter(indent=4)
# import numpy as np

class Grid:
    def __init__(self, line_objs): # line_objs => array of [[x1, y2], [x2, y2]]
        all_x = [entry for line in line_objs for entry in line.get_axis_coordinates("x")]
        all_y = [entry for line in line_objs for entry in line.get_axis_coordinates("y")]
        self.grid = [ # each nested array is a row, so it'll need to be of length max(all_x) - min(all_x)
            [0 for x in range(max(all_x) + 1)] for y in range(max(all_y) + 1)
        ]
    
    def process_flat_line(self, line): # line => [[x1, y2], [x2, y2]]
        flat_direction = line.direction()
        if flat_direction == "x": # x value doesn't change, y does
            x = line.points[0][0]
            span = sorted(line.get_axis_coordinates("y"))
            for y in range(span[0], span[1] + 1):
                self.grid[y][x] += 1
        if flat_direction == "y": # y doesn't change, x does
            y = line.points[0][1]
            span = sorted(line.get_axis_coordinates("x"))
            for x in range(span[0], span[1] + 1):
                self.grid[y][x] += 1
    
    def overlaps(self, threshold):
        count = 0
        for row in self.grid:
            for value in row:
                if value >= threshold:
                    count += 1
        return count

class Line:
    def __init__(self, line): # line => [[x1, y2], [x2, y2]]
        self.points = line

    def is_flat(self):
        [x1, y1], [x2, y2] = self.points
        return (x1 == x2) or (y1 == y2)
    
    def direction(self):
        x1 = self.points[0][0]
        x2 = self.points[1][0]
        if x1 == x2:
            return "x" # the line is a flat vertical line
        else: # y1 == y2
            return "y" # the line is a flat horizontal line
        
    def get_axis_coordinates(self, axis): # axis => "x" or "y"
        [x1, y1], [x2, y2] = self.points
        if axis == "x":
            return [x1, x2]
        else: # axis == "y":
            return [y1, y2] 

class Grid2(Grid):
    def process_diagonal_line(self, line):
        direction = line.diagonal_direction()
        current_point, end_point = line.points
        while current_point != end_point:
            x, y = current_point
            self.grid[y][x] += 1
            current_point[0] += direction[0]
            current_point[1] += direction[1]
        x, y = current_point
        self.grid[y][x] += 1

class Line2(Line):
    def is_diagonal(self):
        [x1, y1], [x2, y2] = self.points
        return abs(x2 - x1) / abs(y2 - y1) == 1

    def diagonal_direction(self):
        [x1, y1], [x2, y2] = self.points
        if (x1 > x2) and (y1 < y2):
            return [-1, 1]
        elif (x1 < x2) and (y1 < y2):
            return [1, 1]
        elif (x1 > x2) and (y1 > y2):
            return [-1, -1]
        else: # if (x1 < x2) and (y1 > y2):
            return [1, -1]

def part1(lines):
    line_objs = [Line(line) for line in lines if Line(line).is_flat()]
    grid = Grid(line_objs)
    for line in line_objs:
        grid.process_flat_line(line)
    return grid.overlaps(2)
    
def part2(lines):
    line_objs = [Line2(line) for line in lines]
    grid = Grid2(line_objs)
    for line in line_objs:
        if line.is_flat():
            grid.process_flat_line(line)
        elif line.is_diagonal():
            grid.process_diagonal_line(line)
        else:
            continue
    return grid.overlaps(2)

def main():
    with open("./inputs/day5.txt") as infile:
        infile = infile.read().split("\n")[:-1] # length 500
    
    lines = [
        [
            [
                int(number) for number in entry.split(",")
            ] for entry in subarray.split(" -> ")
        ] for subarray in infile
    ]

    print("Answer for part 1 =", part1(lines))
    print("Answer for part 2 =", part2(lines))

if __name__ == "__main__":
    main()
