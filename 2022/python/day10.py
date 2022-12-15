from utils import get_input

# def part1(input):

#     x = 1
#     waiting = {
#         # cycle number: value to increment x by
#     }

#     total = 0

#     cycle = 0
#     while cycle <= 220:

#         # Check to see if there are any operations to handle.
#         if cycle < len(input):
#             line = input[cycle]

#             if line[0] == 'addx':
#                 value = int(line[1])

#                 waiting[cycle + 2] = value

#         # 20th, 60th, 100th, 140th, 180th, and 220th
#         if cycle in [19,59,99,139,179,219]:
#             signal_strength = cycle * x
#             total += signal_strength
#             print(cycle, x, signal_strength)

#         # Apply any changes from `waiting`.
#         if cycle in waiting:
#             x += waiting[cycle]

#         cycle += 1
    
#     print('Part 1 -->', total)
#     # 21893 - too high
#     # 21817 - too high

small_example = [
    ["noop"],
    ["addx", "3"],
    ["addx", "-5"],
]

bigger_example = [line.split() for line in '''addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
'''.strip().split("\n")] 

def part1(input):

    input = bigger_example

    x = 1
    waiting = {}

    cycle = 0
    # while cycle <= 5:
    while cycle < len(input) or len(waiting) != 0:

        if x in [21,19,18,16]:
            print(cycle)

        # Check to see if there is an actionable operation from the input that we need to schedule.
        if cycle < len(input):
            line = input[cycle]
            command = line[0]
            if command == "addx":
                value = int(line[1])
                waiting[cycle + 2] = value
        
        # Output signal strength
        if cycle in [19, 59, 99, 139, 179, 219]:
        # if cycle in [20, 60, 100, 140, 180, 220]:
            signal_strength = cycle * x
            # print(cycle, signal_strength)
        
        # Check `waiting` to see if there are operations we need to carry out now.
        if cycle in waiting:
            x += waiting[cycle]
            del waiting[cycle]
        
        cycle += 1
    
    # print('Part 1 -->', x)

def part2(input):
    pass

''' ****************************************************************** '''

if __name__ == "__main__":
    input = [line.split() for line in get_input().strip().split("\n")]
    part1(input)
    part2(input)