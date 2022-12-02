def search(param, point):
    """ point is a list of two coordinates """
    basin_points = [point] # to track the points covered

    def recurse(recurse_param):
        above = check(param, recurse_param[0]-1, recurse_param[1], False)
        below = check(param, recurse_param[0]+1, recurse_param[1], False)
        left = check(param, recurse_param[0], recurse_param[1]-1, False)
        right = check(param, recurse_param[0], recurse_param[1]+1, False)
        
        def check_point(old_point, new_point):
            # new_point must be somewhere on the grid, and the value of new_point must be bigger than the value of old_point
            if new_point == False:
                return False
            old_point_value = int(param[old_point[0]][old_point[1]])
            new_point_value = int(param[new_point[0]][new_point[1]])
            return (old_point_value <= new_point_value < 9)

        to_check = [point for point in [above, below, left, right] if check_point(recurse_param, point)]

        for next_point in to_check:
            if not next_point in basin_points:
                basin_points.append(next_point)
                recurse(next_point)

    recurse(point)
    return len(basin_points)

def check(param, i,j, point_value = True):
    if (not 0 <= i < len(param)) or (not 0 <= j < len(param[0])):
        return False
    if point_value:
        return param[i][j]
    else:
        return [i,j]

def highlight(param, i, j):
    return [(param[i][col] if col != j else f"*${str(param[i][col])}*") for col in range(len(param[i]))]

def part1(param, risk_level = True):
    count = 0
    min_points = []
    for i in range(len(param)):
        for j in range(len(param[0])):
            adjacents = [
                check(param, i-1, j), # above 
                check(param, i+1, j), # below 
                check(param, i, j-1), # left
                check(param, i, j+1) # right
            ]
            bigger = [(int(val) > int(param[i][j])) for val in adjacents if val != False]
            if bigger == [True for val in bigger]:
                count += (int(param[i][j]) + 1)
                min_points.append([i,j])
    if risk_level:
        return count
    else:
        return min_points # for part 2

def part2(param):
    min_points = part1(param, False)
    basin_sizes = sorted(
        [search(param, point) for point in min_points]
    )
    return basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]

def main():
    with open("./inputs/day9.txt") as infile:
        infile = [[num for num in row] for row in infile.read().strip().split("\n")]
    
    print("Answer for part 1 =", part1(infile))
    print("Answer for part 2 =", part2(infile))

if __name__ == "__main__":
    main()
