import sys
import re

def get_input() -> 'str':
    python_file_path = sys.argv[0]
    input_file_path = python_file_path\
        .replace("python", "inputs")\
        .replace("py", "txt")
    with open(input_file_path) as f:
        return f.read()
