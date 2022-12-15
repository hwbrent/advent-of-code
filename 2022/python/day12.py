from utils import get_input
import time
import copy
import string

import sys
sys.setrecursionlimit(10**6)

from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

# LINE_LENGTH = get_input().index('\n') + 1
LINE_LENGTH = 144
LETTERS = 'S' + string.ascii_lowercase + 'E'

def get_above(input, index) -> 'int':
    ''' Returns the index of the char directly above `index`. '''
    if index >= LINE_LENGTH:
        return index - LINE_LENGTH

def get_below(input, index):
    ''' Returns the index of the char directly below `index`. '''
    if index < len(input) - LINE_LENGTH:
        return index + LINE_LENGTH

def get_left(input, index):
    ''' Returns the index of the char directly to the left of `index`. '''
    if index != 0 and input[index - 1] != '\n':
        return index - 1

def get_right(input, index):
    ''' Returns the index of the char directly to the left of `index`. '''
    if index < len(input)-1 and input[index + 1] != '\n':
        # return input[index + 1]
        return index + 1

def is_eligible(input, i1,i2):
    ''' i1 is the index of the current value. i2 is the index of the option. '''

    if i2 is None:
        return False

    # the elevation of the destination square can be at most one higher than the elevation of your current square.
    # (This also means that the elevation of the destination square can be much lower than the elevation of your current square)
    c1, c2 = input[i1], input[i2]
    eligible_elevation_difference = LETTERS.index(c2) <= LETTERS.index(c1)+1

    return eligible_elevation_difference

def get_options(input,i):
    opts = [
        get_below(input, i),
        get_above(input, i),
        get_left(input, i),
        get_right(input, i)
    ]
    return [v for v in opts if is_eligible(input,i,v)]

''' ****************************************************************** '''

class Node:
    def __init__(self, index, char, opts, parent=None):
        self.index = index
        self.char = char
        self.opts = opts
        self.parent = parent

        self.visited = False

class BFS:
    '''
    ### Pseudocode:
    ```txt
    1  procedure BFS(G, root) is
    2      let Q be a queue
    3      label root as explored
    4      Q.enqueue(root)
    5      while Q is not empty do
    6          v := Q.dequeue()
    7          if v is the goal then
    8              return v
    9          for all edges from v to w in G.adjacentEdges(v) do
    10              if w is not labeled as explored then
    11                  label w as explored
    12                  w.parent := v
    13                  Q.enqueue(w)
    ```
    '''
    def __init__(self, input):
        self.node_info = self.__get_node_info(input)
        self.root = self.node_info[input.index('S')]

    def __get_node_info(self, input) -> 'dict':
        ''' 
        Basically just gets a dictionary of all the nodes in a graph
        
        -----

        Return value:
        ```python
        {
            ...
            37: {
                opts: [2, 88, 41, ...],
                visited: false
            }
            ...
        }
        ```
        '''
        info = {}
        for i, char in enumerate(input):
            if char == '\n':
                continue
            info[i] = {
                "char": input[i],
                "opts": get_options(input, i),
                "visited": False,
                "parent": None
            }
        return info

    def do(self):
        q = list()
        self.root['visited'] = True
        q.append(self.root)

        while len(q) != 0:
            v = q.pop(0)
            if v['char'] == 'E':
                return v
            for next_node in v['opts']:
                next_node = self.node_info[next_node]
                if not next_node['visited']:
                    next_node['visited'] = True
                    next_node['parent'] = v
                    q.append(next_node)

    def get_as_list(self):
        # out = []
        # end = self.do()
        # while not end['parent'] is None:
        #     out.append(end['parent'])
        pass

''' ****************************************************************** '''

if __name__ == "__main__":
    input = get_input().strip()

    example = '''Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi'''

    bfs = BFS(input)
    end = bfs.do()
    print(end)
