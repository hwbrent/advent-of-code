def part1():
    with open("./inputs/day2.txt") as file:
        file = file.read().split("\n")
        
        count = 0
        for entry in file:
            # e.g. 7-8 k: kkkkkkkf
            entry = entry.split()

            lower_bound, upper_bound = entry[0].split("-")
            letter = entry[1][0]
            password = entry[2]

            if int(lower_bound) <= password.count(letter) <= int(upper_bound):
                count += 1

        print(count)
            
def part2():
    with open("./inputs/day2.txt") as file:
        file = file.read().split("\n")

        count = 0
        for entry in file:
            # e.g. 7-8 k: kkkkkkkf
            entry = entry.split()

            lower_bound, upper_bound = entry[0].split("-")
            letter = entry[1][0]
            password = entry[2]

            condition1 = (password[ int(lower_bound) - 1 ] == letter)
            condition2 = (password[ int(upper_bound) - 1 ] == letter)

            if condition1 + condition2 == 1:
                count += 1
        
        print(count)

part2()