def part1(param): # 1 or 4 or 7 or 8
    validate = lambda x: (len(x) == 2 or len(x) == 4 or len(x) == 3 or len(x) == 7)
    return len([string for entry in param for string in entry[1] if validate(string)])

def get_wire_mappings(arr, number):
    """ Returns a list of the string mappings that could correspond to the parameter `number` """
    combos = {0: 6, 1: 2, 2: 5, 3: 5, 4: 4, 5: 5, 6: 6, 7: 3, 8: 7, 9: 6}
    return [string for string in arr if len(string) == combos[number]]

str_to_int = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9
}

def part2(param):
    total = 0
    for entry in param:
        wm, digits = entry
        mappings = {number: get_wire_mappings(wm, number) for number in range(10)}
        
        C_F = mappings[1][0] # 1 ==> CF
        A_C_F = mappings[7][0] # 7 ==> ACF
        
        A = [letter for letter in A_C_F if letter not in C_F][0] # top segment

        # now I have A, and C_F
        D_G = None
        for combo in mappings[3]: # 3 ==> ACDFG
            unknown_chars = [char for char in combo if not char in A_C_F] # will be length 2 if we're looking at the digit 2
            if len(unknown_chars) == 2:
                D_G = unknown_chars
            
        # can use C_F and D_G to work out B from get_wire_mappings(wm, 4)
        # 4 ==> BCDF
        B = [char for chars in mappings[4] for char in chars if not ((char in C_F) or (char in D_G))][0]

        # then you can use D_G and A and B to figure out F from get_wire_mappings(wm, 5)
        F = None
        for combo in mappings[5]: # 5 ==> ABDFG
            condition = lambda char: not ((char in D_G) or (char == A) or (char == B))
            unknown_chars = [char for char in combo if condition(char)]
            if len(unknown_chars) == 1:
                F = unknown_chars[0]
        # can use F and C_F to figure out C
        C = C_F[0] if (C_F[1] == F) else C_F[1]

        # now I know A,B,C,F, and D_G
        # I can get E from those and get_wire_mappings(wm, 6)
        E = None
        for combo in mappings[6]: # 6 ==> ABDEFG
            condition = lambda char: not ((char == A) or (char == B) or (char in D_G) or (char == F) or (char == C))
            unknown_chars = [char for char in combo if condition(char)]
            if len(unknown_chars) == 1:
                E = unknown_chars[0]

        # now I have A,B,C,E,F, and D_G, so I can get D from get_wire_mappings(wm, 4)
        condition = lambda char: not ((char == B) or (char == C) or (char == F))
        D = [char for combo in mappings[4] for char in combo if condition(char)][0]

        G = D_G[0] if D_G[1] == D else D_G[1]
        
        mappings2 = {
            A: "a",
            B: "b",
            C: "c",
            D: "d",
            E: "e",
            F: "f",
            G: "g"
        }
        
        translation = lambda digit: "".join(sorted([mappings2[char] for char in digit]))

        digit = int("".join([str(str_to_int[translation(digit)]) for digit in digits]))
        total += digit
    
    return total

def main():
    with open("./inputs/day8.txt") as infile:
        infile = [[left.split(), right.split()] for [left, right] in [line.split(" | ") for line in infile.read().strip().split("\n")]]
    
    print("Answer for part 1 =", part1(infile))
    print("Answer for part 2 =", part2(infile))

if __name__ == "__main__":
    main()
