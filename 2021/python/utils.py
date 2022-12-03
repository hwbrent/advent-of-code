def get_input() -> 'str':
    '''
    Uses sys.argv[0] to automatically figure out which input you want and
    returns it as a string.
    '''
    import sys
    python_file_path = sys.argv[0]
    input_file_path = python_file_path\
        .replace("python", "inputs")\
        .replace("py", "txt")
    with open(input_file_path) as f:
        return f.read()

def fetch_and_save_inputs() -> 'None':
    import os
    import requests

    def get_url(day_number): return f'https://adventofcode.com/2021/day/{day_number}/input'
    def get_filename(day_number): return f'2021/inputs/day{day_number}.txt'

    for day_number in range(1,26):

        filename = get_filename(day_number)
        # if not os.path.exists(filename):
        if True:

            url = get_url(day_number)
            res = requests.get(url)

            with open(filename, "wb") as f:
                f.write(res.content)

    print('Done!')

if __name__ == "__main__":
    fetch_and_save_inputs()
