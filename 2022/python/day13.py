from utils import get_input
import json

ans_indices = [1, 7, 8, 10, 11, 18, 21, 24, 25, 26, 27, 28, 33, 35, 37, 42, 43, 45, 50, 52, 53, 55, 57, 58, 59, 61, 64, 66, 69, 70, 72, 73, 74, 77, 78, 79, 82, 83, 90, 92, 94, 96, 97, 103, 107, 108, 109, 112, 117, 118, 119, 120, 121, 123, 126, 131, 133, 134, 135, 137, 138, 139, 141, 142, 144, 145, 147, 148, 149]

def parse_input(input = get_input()):
    return [
        [json.loads(packet) for packet in pair.split('\n')]
        for pair in input.strip().split('\n\n')
    ]

def part1(input):
    '''
    Determine which pairs of packets are already in the right order.
    What is the sum of the indices of those pairs?
    '''

    indices = set()

    # Iterate through each pair of packets.
    for index, pair in enumerate(input):
        index += 1
        packet1, packet2 = pair
        
        left = None
        right = None

        # Compare the two packets from above.
        i = 0
        while True:
            assert type(packet1) == type(packet2) == list

            p1_ended_before_p2 = i == len(packet1) and i < len(packet2)
            p2_ended_before_p1 = i < len(packet1) and i == len(packet2)
            both_ended_at_same_time = i == len(packet1) == len(packet2)

            if p1_ended_before_p2:
                indices.add(index)
                break
            elif p2_ended_before_p1 or both_ended_at_same_time:
                break
            else:
                # Both lists still have values left in them.
                # So now need to compare those values

                if left is right is None:
                    left = packet1[i]
                    right = packet2[i]

                # If both values are integers
                if type(left) == type(right) == int:
                    pass

                # If both values are lists
                elif type(left) == type(right) == list:
                    pass

                # If exactly one value is an integer
                else: # different types
                    pass


        print(packet1)
        print(packet2)
        print()

    pass

def part2(input):
    pass

if __name__ == '__main__':
    # example_input = [
    #     [[1, 1, 3, 1, 1],
    #      [1, 1, 5, 1, 1]],

    #     [[[1], [2, 3, 4]],
    #      [[1], 4]],

    #     [[9],
    #      [[8, 7, 6]]],

    #     [[[4, 4], 4, 4],
    #      [[4, 4], 4, 4, 4]],

    #     [[7, 7, 7, 7],
    #      [7, 7, 7]],

    #     [[],
    #      [3]],

    #     [[[[]]],
    #      [[  ]]],

    #     [[1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
    #      [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]]
    # ]
    # part1(example_input)
    # part2(example_input)

    input = [[json.loads(packet) for packet in pair.split('\n')] for pair in get_input().strip().split('\n\n')]
    part1(input)
    part2(input)

#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################

# print("-"*50)
# print(ans_indices)
# print(sum(ans_indices))

# indices = []

# from collections import defaultdict
# from functools import cmp_to_key

# # with open('input.txt') as file:
# with open('2022/inputs/day13.txt') as file:
#     lines = [line.strip() for line in file.readlines()]

# def compare(a, b):
#     if type(a) == type(b) == int:
#         if a < b:
#             return -1
#         elif a > b:
#             return 1
#         else:
#             return 0
#     elif type(a) == type(b) == list:
#         n = len(a)
#         m = len(b)
#         res = 0
#         for i in range(min(n, m)):
#             res = compare(a[i], b[i])
#             if res:
#                 break
#         if res == 0:
#             if n < m:
#                 return -1
#             elif n > m:
#                 return 1
#             else: return 0
#     elif type(a) == int:
#         res = compare([a], b)
#     else:
#         res = compare(a, [b])
#     return res

# # Part 1
# d = defaultdict(list)
# ans = 0
# idx = 1
# key = 'left'
# for line in lines:
#     if not line:
#         continue
#     d[key] = eval(line)
#     if key == 'left':
#         key = 'right'
#     else:
#         key = 'left'
#         res = compare(d['left'], d['right'])
#         if res == -1:
#             ans += idx
#             indices.append(idx)
#         idx += 1

# print(indices)
# print(ans)

# # Part 2
# # d = defaultdict(list)
# # for i, line in enumerate(lines):
# #     if not line:
# #         continue
# #     d[i] = eval(line)
# # d[i+1] = [[2]]
# # d[i+2] = [[6]]
# # a = sorted(d.values(), key=cmp_to_key(compare))
# # i = a.index([[2]]) + 1
# # j = a.index([[6]]) + 1
# # print(i * j)