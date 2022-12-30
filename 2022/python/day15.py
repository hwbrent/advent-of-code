from utils import get_input
import re
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

# Puzzle description: https://adventofcode.com/2022/day/15
# Puzzle input:       https://adventofcode.com/2022/day/15/input

def parse(raw_input:'str'):
    sensors_to_beacons = dict()
    for line in raw_input.strip().split('\n'):

        coords_search = re.findall(r'-?\d+',line)
        assert len(coords_search) == 4

        sensor = (int(coords_search[0]), int(coords_search[1]))
        beacon = (int(coords_search[2]), int(coords_search[3]))
        sensors_to_beacons[sensor] = beacon

    return sensors_to_beacons

def distance(p1: 'tuple', p2: 'tuple'):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def get_distances(parsed_input:'dict') -> 'dict':
    distances = dict()
    for sensor, beacon in parsed_input.items():
        x1, y1 = sensor
        x2, y2 = beacon
        manhattan_distance = abs(x1-x2) + abs(y1-y2)
        distances[(sensor, beacon)] = manhattan_distance
    return distances

def nth_odd(n:'int') -> 'int':
    return (2*n) - 1

def part1(input):
    distances = get_distances(input)
    y = 2_000_000
    # y = 10
    ineligible_points = set()

    '''
    Logic:
    - For each sensor-beacon pair, figure out the distance from the sensor
      to beacon.
        - This tells us the area of coverage that the sensor has in which
          there cannot be another beacon.
    - Calculate whether any points on the y line specified would lie within
      the coverage of the sensor.
        - If it does, the number of ineligible points on the y line created
          by the sensor is equal to the nth odd number where n is the
          distance past the y line that the sensor covers.
        - You can use the x coordinate of the sensor and the nth odd number
          value to calculate the exact x coordinates that can't contain
          beacons (minus the poins which contain beacons themselves).
    '''

    for pair, distance in distances.items():
        sensor, _ = pair

        # The coverage in the y direction.
        # i.e. the y coordinates of the points within the search
        # radius of `sensor`.
        sensor_coverage_y = range(sensor[1] - distance, sensor[1] + distance + 1)

        if not y in sensor_coverage_y:
            continue

        # Distance between sensor and y line.
        diff = abs(sensor[1] - y) - 1
        # If we subtract this from `distance`, we can find out the number
        # and location of the positions on the y line which can't contain
        # beacons.
        number_of_ineligible_positions = nth_odd(distance - diff)

        # So there will be a line of points that can't contain beacons.
        # The middle of the line will have the same x coordinate as the sensor.
        # We can use this to find each point on the line.
        distance_either_side = int((number_of_ineligible_positions-1) / 2)

        for x_coord in range(sensor[0] - distance_either_side, sensor[0] + distance_either_side + 1):
            ineligible_points.add(x_coord)

        # print('sensor',sensor)
        # # print('beacon',beacon)
        # print('distance',distance)
        # print('sensor_coverage_y', sensor_coverage_y[0], sensor_coverage_y[-1])
        # print('y in sensor_coverage_y',y in sensor_coverage_y)
        # print('diff',diff)
        # print('number_of_ineligible_positions',number_of_ineligible_positions)
        # print('distance_either_side',distance_either_side)
        # print()

    # Remove any points in `ineligible_points` which contain beacons
    for beacon in input.values():
        beacon_x, beacon_y = beacon
        if beacon_y == y:
            ineligible_points.discard(beacon_x)

    print('Part 1 -->', len(ineligible_points))

def part2(input):
    print('Part 2 -->', None)

if __name__ == '__main__':
    input = parse(get_input())
#     input = parse('''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
# Sensor at x=9, y=16: closest beacon is at x=10, y=16
# Sensor at x=13, y=2: closest beacon is at x=15, y=3
# Sensor at x=12, y=14: closest beacon is at x=10, y=16
# Sensor at x=10, y=20: closest beacon is at x=10, y=16
# Sensor at x=14, y=17: closest beacon is at x=10, y=16
# Sensor at x=8, y=7: closest beacon is at x=2, y=10
# Sensor at x=2, y=0: closest beacon is at x=2, y=10
# Sensor at x=0, y=11: closest beacon is at x=2, y=10
# Sensor at x=20, y=14: closest beacon is at x=25, y=17
# Sensor at x=17, y=20: closest beacon is at x=21, y=22
# Sensor at x=16, y=7: closest beacon is at x=15, y=3
# Sensor at x=14, y=3: closest beacon is at x=15, y=3
# Sensor at x=20, y=1: closest beacon is at x=15, y=3
# ''')
    part1(input)
    part2(input)
