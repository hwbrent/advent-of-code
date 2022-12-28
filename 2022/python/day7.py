from utils import get_input
import copy
from collections import defaultdict
from pprint import PrettyPrinter
pp = PrettyPrinter(4)

'''
--- Day 7: No Space Left On Device ---

You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device

Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files). The outermost directory is called /. You can navigate around the filesystem, moving into or out of directories and listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

    cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
        cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
        cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
        cd / switches the current directory to the outermost directory, /.
    ls means list. It prints out all of the files and directories immediately contained by the current directory:
        123 abc means that the current directory contains a file named abc with size 123.
        dir xyz means that the current directory contains a directory named xyz.

Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)

Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a). These directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion. To do this, you need to determine the total size of each directory. The total size of a directory is the sum of the sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

    The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
    The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596), plus file i indirectly (a contains e which contains i).
    Directory d has total size 24933642.
    As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.

To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes. In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?
'''

def parse_input(raw_input) -> 'list':
    out = list()

    # Split by each command executed.
    # [1:] because entry[0] is whitespace.
    for entry in raw_input.split("$")[1:]:
        entry = entry.strip().split("\n")

        # Split the command into its operator and any argument.
        # After splitting, if the length of entry[0] is 1, the command had no
        # arguments. Else, it had arguments.
        entry[0] = entry[0].split()
        
        if len(entry) > 1:
            # Stuff was written to stdout.
            for index, subentry in enumerate(entry[1:]):
                index += 1
                entry[index] = entry[index].split()

                if entry[index][0].isnumeric():
                    # Means that entry[index][0] is the file size.
                    entry[index][0] = int(entry[index][0])
                else:
                    # Signifies that entry[index][0] is a directory.
                    assert(entry[index][0] == 'dir')
        else:
            assert(entry[0][0] == 'cd' or entry[0][0] == 'ls')
        
        out.append(entry)

    return out

def convert_path_list_to_string(path:'list[str]') -> 'str':
    copied = copy.deepcopy(path)
    '''
    Converts a `list` of `str` (representing a path within the file system)
    to a string representing how the file system `dict` would be indexed to
    get to that location.

    Example:
    ```python
    path = ['~', 'Documents', 'misc','durham']
    print(convert_path_list_to_string(path)) # -> ['~']['Documents']['misc']['durham']
    ```
    '''
    for index, entry in enumerate(copied):
        if type(entry) == str:
            copied[index] = f"['{entry}']"
        elif type(entry) == int:
            copied[index] = f"[{entry}]"
    return "".join(copied)

def convert_stdout_item(entry:'list'):
    '''
    e.g. ['dir', 'mtbt']
    e.g. [95962, 'mzvb']
    '''
    if entry[0] == 'dir':
        return {"type":"dir", "contents":{}}
    elif type(entry[0]) == int:
        return {"type":"file", "size": entry[0]}

def get_file_system(parsed_input:'list') -> 'dict':
    '''
    Convert the file system implied by the parsed_input and return it as a `dict`.

    This code is VERY sketchy - it uses `eval` and `exec` to get and set the value of
    a `dict` which eventually is returned from this function.

    Basically, the two main variables are `file_system` and `current_path`.

    ### `file_system`
    - Is a nested `dict`.
    - Each value has a key and a value (obviously)
        - The key is a string which is simply the name of the directory/file
        - If the value is meant to represent a directory, it is a nested `dict` which can
          contain other directories/files. If it's meant to represent a file, it is a number
          representing the file size.

    ### `current_path`
    - Points to a directory/file in the file system
    - It's stored as a list, but is converted by `convert_path_list_to_string` into a string which is used
      to access values in `file_system`.
    - Example:

    ```python
    current_path = ['/', 'Users', 'henrybrent', 'Downloads'] # i.e. /Users/henrybrent/Downloads
    convert_path_list_to_string(current_path) # ['/']['Users']['henrybrent']['Downloads']
    file_system['/']['Users']['henrybrent']['Downloads']
    {
        "/": {
            ...
            "Users": {
                ...
                "henrybrent": {
                    ...
                    "Downloads": {}
                    ...
                }
                ...
            },
            ...
        }
    }
    ```
    '''

    # A dict representing the file system in the parsed_input.
    file_system = dict()

    # The current location within `file_system`.
    current_path = []

    all_dirs = set()

    for entry in parsed_input:

        command = entry[0][0]
        assert command == 'cd' or command == 'ls'

        if command == 'cd':

            # The directory we're cd'ing into
            target_dir = entry[0][1]

            #####################
            ##### Handle cd #####
            #####################

            current_dir = eval(f'file_system{convert_path_list_to_string(current_path)}')

            if target_dir == "..":
                # Going UP into parent directory. So remove last value in `current_path`
                del current_path[-1]
            
            else:
                # Going DOWN into child directory. So add value to `current_path`
                current_path.append(target_dir)
                all_dirs.add(tuple(current_path))
                if not target_dir in current_dir.keys():
                    exec(f'file_system{convert_path_list_to_string(current_path)} = {{}}')

        elif command == 'ls':

            # Basically just need to check the items in stdout against the
            # contents of the current directory. If something appears in stdout
            # that isn't in the current directory, add it.
            stdout_items = entry[1:]

            current_dir = eval(f'file_system{convert_path_list_to_string(current_path)}')

            for item in stdout_items:

                # Example of a file --> [95962, 'mzvb']
                # Example of a dir  --> ['dir', 'sfjrs']
                assert len(item) == 2
                assert item[0] == 'dir' or type(item[0]) == int

                key = item[1]

                if not key in current_dir:
                    value = item[0] if (type(item[0]) == int) else dict()
                    exec(f'file_system{convert_path_list_to_string(current_path + [key])} = {value}')

    return file_system, all_dirs

''' ****************************************************************** '''

def part1(input):
    '''
    Find all of the directories with a total size of at most 100000.
    What is the sum of the total sizes of those directories?
    '''

    fs, all_dirs = get_file_system(input)

    def default_value():
        return 0

    dir_sizes = defaultdict(default_value)

    def get_dir_size(path) -> 'int':
        ''' Gets the size of the direcory located at `path`. '''
        dir = eval(f'{fs}{convert_path_list_to_string(list(path))}')
        total = 0
        # Iterate through the items in this directory.
        # If the entry is a file, add the size of the file to `total`.
        # If the entry is a directory, add the size of that directory to `total`.
        for k,v in dir.items():
            is_file = type(v) == int
            is_directory = type(v) == dict
            if is_file:
                total += v
            elif is_directory:
                child_path = (*path, k)
                total += dir_sizes[child_path]
        return total

    # Go up each level of the tree, starting from the bottom.
    # Calculate the size of every directory on each level and add it to `dir_paths`.
    tree_height = len(max(all_dirs, key=len))
    for level in reversed(range(1, tree_height+1)):
        for path in all_dirs:
            if len(path) != level:
                continue
            dir_size = get_dir_size(path)
            dir_sizes[path] = dir_size

    total = sum(value for value in dir_sizes.values() if value <= 100_000)
    print('Part 1 -->', total)

def part2(input):
    pass

''' ****************************************************************** '''

if __name__ == "__main__":
    input = parse_input(get_input())
    part1(input)
    part2(input)
