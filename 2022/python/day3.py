from utils import get_input
import string

if __name__ == "__main__":
    print('Part 1 -->', sum([sum([{letter: index+1 for index, letter in enumerate(string.ascii_lowercase + string.ascii_uppercase)}[char] for char in [set(char for char in arg) for arg in [rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:]]][0].intersection(*[set(char for char in arg) for arg in [rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:]]][1:])]) for rucksack in get_input().strip().split("\n")]))
    print('Part 2 -->', sum([sum([{letter: index+1 for index, letter in enumerate(string.ascii_lowercase + string.ascii_uppercase)}[char] for char in [set(char for char in arg) for arg in get_input().strip().split("\n")[x:x+3]][0].intersection(*[set(char for char in arg) for arg in get_input().strip().split("\n")[x:x+3]][1:])]) for x in range(0, len(get_input().strip().split("\n")), 3)]))
