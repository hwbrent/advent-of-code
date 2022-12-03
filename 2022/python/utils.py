import sys

def get_input() -> 'str':
    ''' Uses `sys.argv[0]` to automatically figure out which input you want and returns it as a string. '''
    python_file_path = sys.argv[0]
    input_file_path = python_file_path\
        .replace("python", "inputs")\
        .replace("py", "txt")
    with open(input_file_path) as f:
        return f.read()
