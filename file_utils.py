import sys
import os
from argparse import ArgumentParser
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

CHROMEDRIVER_PATH = './chromedriver_mac64'
REDDIT_LOGIN_PAGE = 'https://adventofcode.com/auth/reddit'
AOC_LOGIN_PAGE = 'https://adventofcode.com/2022/auth/login'
AOC_BASE_URL = 'https://adventofcode.com/'

def get_env_variables() -> 'dict':
    ''' Gets and returns the data in `.env`. '''

    vars = {}

    with open('.env') as f:
        f = f.read().strip().split('\n')

    for entry in f:
        key, value = entry.split('=')
        vars[key] = value.replace("'", '')
    
    return vars

def get_file_path(year:'int', day:'int', input = False) -> 'str':
    assert type(year) == type(day) == int

    day_segment = f'day{day}' # e.g. 'day14'
    file_extension = '.txt' if input else '.py'
    return os.path.join(str(year), 'inputs' if input else 'python', day_segment + file_extension)

def create_python_file(file_path:'str', driver_url:'str', desc_string:'str' = None) -> 'None':
    assert file_path[-3:] == '.py'

    with open(file_path, 'w') as f:
        f.write(f"""from utils import get_input
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

{'' if desc_string is None else f"'''{os.linesep}{desc_string.strip()}'''"}

def part1(input):
    print('Part 1 -->', None)

def part2(input):
    print('Part 2 -->', None)

if __name__ == '__main__':
    input = get_input()
    part1(input)
    part2(input)
""")
    print(f'Successfully created python file at {file_path}!')

def create_input_txt_file(file_path:'str', input:'str') -> 'None':
    assert file_path[-4:] == '.txt'
    with open(file_path, 'w') as f:
        f.write(input)
    print(f'Successfully created input file at {file_path}!')

def get_arg_parser() -> 'ArgumentParser':
    parser = ArgumentParser(
        prog = 'AOC Data Scraper and File Creator',
        description = 'This program scrapes the data for the provided year and day, and creates a python and input file.',
        epilog = ''
    )
    parser.add_argument('year', type=int)
    parser.add_argument('day', type=int)
    parser.add_argument('--desc', action="store_true", default=False)
    return parser

def main() -> 'None':
    env = get_env_variables()
    args = get_arg_parser().parse_args()

    #####################################################################
    ### CHECK THAT FILES DON'T ALREADY EXIST FOR THE GIVEN YEAR & DAY ###
    #####################################################################
    
    year = int(sys.argv[1])
    day = int(sys.argv[2])

    python_file_path = get_file_path(year, day)
    input_file_path = get_file_path(year, day, input=True)

    python_file_exists = os.path.exists(python_file_path)
    input_file_exists = os.path.exists(input_file_path)
    files_already_exist = python_file_exists or input_file_exists
    
    if files_already_exist:
        print(
            'Python file' if python_file_exists else 'Input file',
            f'already exists for {year} and {day}. Quitting...'
        )
        sys.exit()

    ##############
    ### LOG IN ###
    ##############

    # print('Logging into Advent Of Code website...')

    options = webdriver.chrome.options.Options()
    # options.add_argument("headless")
    driver = webdriver.Chrome(
        executable_path = CHROMEDRIVER_PATH,
        options = options
    )

    driver.get(AOC_LOGIN_PAGE)
    login_page_link = driver.find_element(By.CSS_SELECTOR, 'a[href="/auth/reddit"]')
    login_page_link.click()

    username_input = driver.find_element(By.ID, 'loginUsername')
    username_input.send_keys(env['REDDIT_USERNAME'])

    password_input = driver.find_element(By.ID, 'loginPassword')
    password_input.send_keys(env['REDDIT_PASSWORD'])

    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()

    allow_button = None
    while allow_button is None:
        try:
            allow_button = driver.find_element(By.CSS_SELECTOR, 'input.fancybutton.newbutton.allow')
        except:
            continue

    allow_button.click()

    # print('Successfully logged into Advent Of Code website!')

    ##########################
    ### CREATE PYTHON FILE ###
    ##########################

    driver.get(f'{AOC_BASE_URL}{year}/day/{day}')

    # The description is a bunch of elements under an <article> with class 'day-desc'
    # These tags are <p> and <pre>. <pre> contains the code blocks
    day_desc = driver.find_element(By.CLASS_NAME, 'day-desc') # <article>
    children = day_desc.find_elements(By.XPATH, './child::*')
    desc_string = '\n\n'.join(child.text for child in children)

    create_python_file(python_file_path, driver.current_url, desc_string)

    #########################
    ### CREATE INPUT FILE ###
    #########################

    puzzle_input_link = driver.find_element(By.CSS_SELECTOR, 'a[href="15/input"]')
    puzzle_input_link.click()

    input = driver.find_element(By.TAG_NAME, 'pre').text
    create_input_txt_file(input_file_path, input)

    driver.quit()

if __name__ == '__main__':
    main()
