from utils import get_input

if __name__ == "__main__":
    print('Part 1 -->', next(x+4 for x in range(len(get_input().strip())-3) if len(get_input().strip()[x:x+4]) == len(set(char for char in get_input().strip()[x:x+4]))))
    print('Part 2 -->', next(x+14 for x in range(len(get_input().strip())-13) if len(get_input().strip()[x:x+14]) == len(set(char for char in get_input().strip()[x:x+14]))))
