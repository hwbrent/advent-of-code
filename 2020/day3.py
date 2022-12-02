def part1(movement = [3,1]):
    with open("./inputs/day3.txt") as file:
        file = file.read().split("\n")
    
    # print(file)

    current_position = [0,0]
    
    count = 0
    while current_position[1] < len(file):
        current_level = file[current_position[1]]

        obj = current_level[current_position[0]] # either "." or "#"
        if obj == "#":
            count += 1
        
        current_position[0] = (current_position[0] + movement[0]) % len(current_level)
        current_position[1] += movement[1]
    
    print(count)
    return count

def part2():
    with open("./inputs/day3.txt") as file:
        file = file.read().split("\n")
    
    traversals = [
        [1, 1],
        [3, 1],
        [5, 1],
        [7, 1],
        [1, 2]
    ]

    product = 1

    for traversal in traversals:
        product *= part1(traversal)
    
    print(product)
    
part1()
part2()