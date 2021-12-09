class School:
    def __init__(self, array):
        self.school = [Fish(entry) for entry in array]
    
    def show(self):
        print([fish.timer for fish in self.school if fish.timer != 9])
    
    def out(self, with_nines=False):
        if not with_nines:
            return [fish.timer for fish in self.school if fish.timer != 9]
        else:
            return [fish.timer for fish in self.school]
    
    def add_day(self):
        aged_fish = [fish.age() for fish in self.school]
        new_fish = [Fish() for fish in self.school if fish.timer == 0]
        self.school = aged_fish + new_fish
        
class Fish:
    def __init__(self, timer=9):
        self.timer = timer
    
    def age(self):
        if self.timer in [7, 8, 9]:
            self.timer = self.timer - 1
        else:
            self.timer = (self.timer - 1) % 7
        return self

def part1(param):
    school = School(param)
    for _ in range(80):
        school.add_day()
    return len(school.out())

def part2(param):
    timers = {number: param.count(number) for number in range(9)}
    for day in range(256):
        zeroes = timers[0]
        timers[0] = 0
        for i in range(1, len(timers)):
            timers[i - 1] += timers[i]
            timers[i] = 0
        timers[6] += zeroes
        timers[8] += zeroes
    return sum(timers.values())

def main():
    with open("./inputs/day6.txt") as infile:
        infile = [int(number) for number in infile.read().strip().split(",")]

    print("Answer for part 1 =", part1(infile))
    print("Answer for part 2 =", part2(infile))

if __name__ == "__main__":
    main()
