def part1(infile):
    start_coords = [0,0]
    for command in infile:
        direction, magnitude = command.split()
        if direction == "forward":
            start_coords[0] += int(magnitude)
        elif direction == "up":
            start_coords[1] -= int(magnitude)
        else:
            start_coords[1] += int(magnitude)
    return start_coords[0] * start_coords[1]

def part2(infile):
    aim = 0
    start_coords = [0,0]
    for command in infile:
        direction, magnitude = command.split()
        match direction:
            case "forward":
                start_coords[0] += int(magnitude)
                start_coords[1] += (aim * int(magnitude))
            case "up":
                aim -= int(magnitude)
            case "down":
                aim += int(magnitude)
    return start_coords[0] * start_coords[1]

def main():
    with open("./inputs/day2.txt") as infile:
        infile = infile.read().split("\n")[:-1]

    print("Answer for part 1 =", part1(infile))
    print("Answer for part 2 =", part2(infile))

if __name__ == "__main__":
    main()
    