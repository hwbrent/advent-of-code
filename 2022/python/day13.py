from utils import get_input
import json

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

    indices_of_pairs_in_right_order = set() # 1-indexed

    # ------------------------------

    def compare(packet1, packet2, index):
        assert type(packet1) == list
        assert type(packet2) == list

        # Keep incrementing i until one or neither of the packets has no values left
        i = 0
        while True:
            left_ran_out_first = (i == len(packet1) and i < len(packet2))
            right_ran_out_first = (i < len(packet1) and i == len(packet2))
            both_ran_out_at_same_time = (i == len(packet1) == len(packet2))

            if left_ran_out_first:
                # The inputs are in the right order.
                indices_of_pairs_in_right_order.add(index+1)
                return
            elif right_ran_out_first:
                # The inputs are not in the right order.
                return
            elif both_ran_out_at_same_time:
                # Continue checking the next part of the input.
                return
            
            else:
                left = packet1[i]
                right = packet2[i]

                both_ints = type(left) == type(right) == int
                both_lists = type(left) == type(right) == list
                one_int = not (both_ints or both_lists)

                if both_ints:
                    # print('both_ints')
                    # If both values are integers, the lower integer should come first.
                    # If the left integer is lower than the right integer, the inputs are in the right order.
                    # If the left integer is higher than the right integer, the inputs are not in the right order.
                    # Otherwise, the inputs are the same integer; continue checking the next part of the input.

                    if left < right:
                        # The inputs are in the right order.
                        indices_of_pairs_in_right_order.add(index+1)
                        return
                    elif left > right:
                        # The inputs are not in the right order.
                        return
                    elif left == right:
                        # Continue checking the next part of the input.
                        i += 1
                        continue

                elif both_lists:
                    # print('both_lists')
                    # If both values are lists, compare the first value of each list, then the second value, and so on.
                    # If the left list runs out of items first, the inputs are in the right order.
                    # If the right list runs out of items first, the inputs are not in the right order.
                    # If the lists are the same length and no comparison makes a decision about the order, continue checking the next part of the input.
                    compare(left,right,index)

                elif one_int:
                    # print('one_int')
                    # If exactly one value is an integer, convert the integer to a list which contains that integer as its only value, then retry the comparison.
                    # For example, if comparing [0,0,0] and 2, convert the right value to [2] (a list containing 2); the result is then found by instead comparing [0,0,0] and [2].
                    if type(left) == int:
                        compare([left], right, index)
                    elif type(right) == int:
                        compare(left, [right], index)

                i += 1

    # ------------------------------

    for i in range(len(input)):
        compare(*input[i], i)

    print(indices_of_pairs_in_right_order)
    print('Part 1 -->', sum(indices_of_pairs_in_right_order))

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

ans_indices = [1, 7, 8, 10, 11, 18, 21, 24, 25, 26, 27, 28, 33, 35, 37, 42, 43, 45, 50, 52, 53, 55, 57, 58, 59, 61, 64, 66, 69, 70, 72, 73, 74, 77, 78, 79, 82, 83, 90, 92, 94, 96, 97, 103, 107, 108, 109, 112, 117, 118, 119, 120, 121, 123, 126, 131, 133, 134, 135, 137, 138, 139, 141, 142, 144, 145, 147, 148, 149]
print("-"*50)
print(ans_indices)
print(sum(ans_indices))
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