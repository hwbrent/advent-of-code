import copy

def counts(arr):
    out = [[0,0] for index in range(len(arr[0]))]
    for number in arr:
        for x in range(len(number)):
            bit = number[x]
            out[x][int(bit)] += 1
    return out

def part1(infile):
    gamma = [str(subarray.index(max(subarray))) for subarray in counts(infile)]
    epsilon = [str(subarray.index(min(subarray))) for subarray in counts(infile)]
    return int("".join(gamma), 2) * int("".join(epsilon), 2)

def part2(infile):

    def mcbs(nums, measure):
        def eval(subarray, measure):
            if subarray[0] > subarray[1]:
                return 0 if measure == "o2" else 1
            elif subarray[0] < subarray[1]:
                return 1 if measure == "o2" else 0
            else: # subarray[0] == subarray[1]
                return 1 if measure == "o2" else 0
        if measure == "o2":
            return [eval(subarray, "o2") for subarray in counts(nums)]
        else:
            return [eval(subarray, "co2") for subarray in counts(nums)]
            
    def get_rating(measure):
        inp = infile.copy()
        count = 0
        while len(inp) != 1:
            bits = mcbs2(inp, measure)
            relevant_bit = bits[count]
            relevant_nums = [num for num in inp if num[count] == str(relevant_bit)]
            inp = relevant_nums
            count += 1
        return inp[0]

    o2 = get_rating("o2")
    co2 = get_rating("co2")

    return int(o2, 2) * int(co2, 2)

def main():
    with open("./inputs/day3.txt") as infile:
        infile = infile.read().split("\n")[:-1]

    print("Answer for part 1 =", part1(infile))
    print("Answer for part 2 =", part2(infile))

if __name__ == "__main__":
    main()
