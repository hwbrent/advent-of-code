from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

class Board:
    def __init__(self, nested_array):
        self.rows = nested_array
        self.completed = False

    def columns(self):
        return [[row[index] for row in self.rows] for index in range(len(self.rows[0]))]
    
    def cross_off(self, target_number):
        # The original un-crossed-off entries are of type string
        # When they're crossed off, they're converted to integers
        # Kind of the opposite of what makes sense but oh well, it works
        for row in self.rows:
            count = 0
            while count < len(row):
                if row[count] == target_number:
                    row[count] = int(row[count])
                count += 1
        return self
    
    def check(self):
        for row in self.rows:
            if row == [int(entry) for entry in row]:
                self.completed = True
                break
        if self.completed:
            return True
        for column in self.columns():
            if column == [int(entry) for entry in column]:
                self.completed = True
                break
        return self.completed
    
    def score(self, last_number_called):
        if not self.completed:
            print("You melon, you haven't got a bingo yet")
        else:
            unmarked_entries = [int(entry) for row in self.rows for entry in row if type(entry) == str]
            return int(last_number_called) * sum(unmarked_entries)

def part1(drawn_numbers, boards):
    for number in drawn_numbers:
        index = 0
        for board in boards:
            board.cross_off(number)
            if board.check():
                return board.score(number)
            index += 1

def part2(drawn_numbers, boards):
    for number in drawn_numbers:
        index = 0
        while index < len(boards):
            board = boards[index]
            board.cross_off(number)
            if board.check():
                if len(boards) == 1:
                    return board.score(number)
                else:
                    del boards[index]
                    continue
            index += 1

def main():
    with open("./inputs/day4.txt") as infile:
        infile = infile.read().strip().split("\n\n")
    
    drawn_numbers = infile[0].split(",")
    boards = [ Board([row.split() for row in board.split("\n")]) for board in infile[1:] ]
    
    print("Answer for part 1 =", part1(drawn_numbers, boards))
    print("Answer for part 2 =", part2(drawn_numbers, boards))

if __name__ == "__main__":
    main()
