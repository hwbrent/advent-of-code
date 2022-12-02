def part1():
    with open("./inputs/day4.txt") as file:
        file = file.read().split("\n\n")
    
    count = 0
    for entry in file:
        entry.replace("\n", " ")
        entry = entry.split()
        # print(entry)
        # print("-")

        cid_fields = [field for field in entry if "cid" in field]

        condition1 = (len(entry) == 8)
        condition2 = (len(entry) == 7) and (len(cid_fields) == 0)

        if condition1 or condition2:
            count += 1
    
    print(count)

global_fields = [
    'byr',
    'cid',
    'ecl',
    'eyr',
    'hcl',
    'hgt',
    'iyr',
    'pid'
]

def part2():
    with open("./inputs/day4.txt") as file:
        file = file.read().split("\n\n")

    byr = lambda x: (len(x) == 4) and (1920 <= int(x) <= 2002)
    iyr = lambda x: (len(x) == 4) and (2010 <= int(x) <= 2020)
    eyr = lambda x: (len(x) == 4) and (2020 <= int(x) <= 2030)
    ecl = lambda x: (len(x) == 3) and (x in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])
    pid = lambda x: (len(x) == 9) and (not any([not char.isnumeric() for char in x]))
    
    def hgt(measurement, metric):
        if metric == "cm":
            return 150 <= int(measurement) <= 193
        if metric == "in":
            return 59 <= int(measurement) <= 76
    
    def hcl(colour = "#"):
        if colour[0] != "#":
            return False
        
        numbers = [*"0123456789"]
        letters = [*"abcdef"]
        
        if len(color[1:]) != 6:
            return False
        
        for char in colour[1:]:
            if not ((char in numbers) or (char in letters)):
                return False
        
        return True

    count = 0
    for entry in file:
        entry.replace("\n", " ")
        entry = entry.split()
        # print(entry)
        # print()
        pport_fields = sorted([x.split(":")[0] for x in entry])
        
        # print(sorted(pport_fields) == global_fields)
        if (pport_fields != global_fields) or (pport_fields != (global_fields[0:1] + global_fields[2:])):
            print(pport_fields)
            print(global_fields)
            print()
            # print("frick")
            continue


    


part1()
part2()