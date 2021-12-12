"""
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg

0: abcefg
1: cf
2: acdeg
3: acdfg
4: bcdf
5: abdfg
6: abdefg
7: acf
8: abcdefg
9: abcdfg
"""
validate = lambda x: (len(x) == 2 or len(x) == 4 or len(x) == 3 or len(x) == 7)

def part1(param):
    # 1 or 4 or 7 or 8
    valid_output_values = [string for entry in param for string in entry[1] if validate(string)]
    return len(valid_output_values)

def get_wire_mappings(arr, number):
    combos = {0: 6, 1: 2, 2: 5, 3: 5, 4: 4, 5: 5, 6: 6, 7: 3, 8: 7, 9: 6}
    return [string for string in arr if len(string) == combos[number]]
    
def part2(param):
    """
    The unique signal patterns correspond to the ten different ways the submarine tries to render a digit
    using the current wire/segment connections
    """
    # valid_output_values = [string for entry in param for string in entry[1] if validate(string)]
    for entry in param:
        wm, digits = entry
        # unique mappings
        C_F = get_wire_mappings(wm, 1)[0]
        A_C_F = get_wire_mappings(wm, 7)[0]
        
        A = [letter for letter in A_C_F if letter not in C_F][0] # the top segment
        '''
        Now that we have the top segment, we can begin to work out the other correct segments
        
        We can find out segment F by looking at 2 - since 2 contains the segments A and C but not F, whichever
        letter is in A_C_F but not in get_wire_mappings(wm, 2) is F, which also tells us what C is
        '''

        for combo in get_wire_mappings(wm, 3):
            print([letter for letter in combo if letter in A_C_F])

        continue
        
def main():
    with open("./inputs/day8.txt") as infile:    
        infile = infile.read().strip().split("\n")
        infile = [line.split(" | ") for line in infile]
        infile = [[left.split(), right.split()] for [left, right] in infile]
    
    # print("Answer for part 1 =", part1(infile))
    print("Answer for part 2 =", part2(infile))

if __name__ == "__main__":
    main()
