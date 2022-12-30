from utils import get_input
import copy
import itertools
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

# Puzzle description: https://adventofcode.com/2022/day/14
# Puzzle input:       https://adventofcode.com/2022/day/14/input

def parse(raw_input):
    # Generator which yields generators which yield tuples with x,y coordinates
    input = (
        (
        #   (     x coordinate       ,       y coordinate      )
            (int(coord.split(',')[0]), int(coord.split(',')[1]))
            for coord in line.split(" -> ")
        )
        for line in raw_input.strip().split('\n')
    )

    all_obstacles = set()

    for rock_line in input:
        for point1, point2 in itertools.pairwise(rock_line):
            assert point1 != point2

            # Add both points, and every point between point1 and point2, to all_obstacles
            all_obstacles.add(point1)
            all_obstacles.add(point2)

            # The axis (i.e. x or y) that differs between the points
            xory = 0 if point1[0] != point2[0] else 1
            magnitude = 1 if point2[xory] > point1[xory] else -1

            point1, point2 = list(point1), list(point2)
            while point1 != point2:
                point1[xory] += magnitude
                all_obstacles.add(tuple(point1))

    return all_obstacles

def directly_below(sand):
    x,y = sand
    return (x, y+1)
def below_left(sand):
    x,y = sand
    return (x-1, y+1)
def below_right(sand):
    x,y = sand
    return (x+1, y+1)

def is_blocked(all_obstacles, coord:'tuple'):
    ''' NB: `coord` should be a `tuple`. '''
    return coord in all_obstacles

def move_sand(current, new):
    current[0], current[1] = new[0], new[1]

def is_in_abyss(sand, lowest_obstacle):
    return sand[1] > lowest_obstacle

def part(part_no, input):
    '''
    Using your scan, simulate the falling sand.
    How many units of sand come to rest before sand starts flowing into the abyss below?
    '''
    all_obstacles = copy.deepcopy(input)

    lowest_obstacle = max(coord[1] for coord in all_obstacles)
    floor_height = 2 + lowest_obstacle

    units_of_sand = 0
    done = False
    while not done:

        # Simulate grain of sand falling down.
        # Sand falls from [500,0].
        sand = [500,0]
        while True:

            # Circumstances under which to stop placing sand.
            part1_stop_condition = part_no == 1 and is_in_abyss(sand, lowest_obstacle)
            part2_stop_condition = part_no == 2 and (500,0) in all_obstacles
            if part1_stop_condition or part2_stop_condition:
                done = True
                break

            # Check space below.
            # If there's something there, check the space below and left
            # If there's something there, check the space below and right
            # Else, come to rest at the current position and break.

            below = directly_below(sand)
            left = below_left(sand)
            right = below_right(sand)

            blocked_below = is_blocked(all_obstacles, below)
            blocked_left = is_blocked(all_obstacles, left)
            blocked_right = is_blocked(all_obstacles, right)

            completely_blocked = blocked_below and blocked_left and blocked_right
            on_floor = sand[1] == floor_height - 1

            if (part_no == 2 and on_floor) or completely_blocked:
                # Sand can't move any further.
                assert tuple(sand) not in all_obstacles
                all_obstacles.add(tuple(sand))
                break

            elif not blocked_below:
                move_sand(sand, below)
            elif not blocked_left:
                move_sand(sand, left)
            elif not blocked_right:
                move_sand(sand, right)

        units_of_sand += 1
    units_of_sand -= 1

    print(f'Part {part_no} --> {units_of_sand}')

if __name__ == '__main__':
    input = parse(get_input())
    part(1,input)
    part(2,input)
