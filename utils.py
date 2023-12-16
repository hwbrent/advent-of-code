import os
import sys
import datetime
import urllib.parse
import pathlib
import inspect
import time

import requests
import bs4
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# The "home page" as it were
# Seems to show the problems for the most recent year by default
AOC_BASE_URL = "https://adventofcode.com/"

# The number of the month of December
DECEMBER = 12

# The first year that they did AOC.
EARLIEST_YEAR = 2015

CHROMEDRIVER_PATH = "./chromedriver"

PYTHON_FILE_TEMPLATE = """
import os
import sys
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

# Enable imports from advent-of-code/utils.py
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
sys.path.append(root)

import utils

# Problem URL: {problem_url}
# Input URL:   {input_url}

\"\"\"
{title}

{part1_description}
\"\"\"


def parse_raw_input(input: str):
    return input


def part1(input):
    answer = None
    return answer


def part2(input):
    answer = None
    return answer


def main():
    raw_input = utils.get_raw_input()
    parsed_input = parse_raw_input(raw_input)

    utils.handle(part1(parsed_input), 1)
    utils.handle(part2(parsed_input), 2)


if __name__ == "__main__":
    main()
""".lstrip()

this_dir = os.path.dirname(__file__)


def get_most_recent_year() -> int:
    """
    Returns the recent year that AOC has taken place. i.e. if it's December
    of the current year, this function will return the current year. Otherwise,
    it returns the previous year/
    """
    now = datetime.datetime.now()
    year = now.year

    if now.month != DECEMBER:
        year -= 1

    return year


def is_valid_year(year: int) -> bool:
    return EARLIEST_YEAR <= year <= get_most_recent_year()


def is_valid_day(day: int) -> bool:
    return 1 <= day <= 25


def parse_args() -> tuple[int, int]:
    """
    Basically just checks the command-line arguments for any valid combination
    of year and/or day (or neither). If the arguments are valid, this returns
    a tuple of the form (year, day)
    """
    args = sys.argv[1:]

    now = datetime.datetime.now()

    year = None
    day = None

    match len(args):
        case 0:
            # Assume we want to generate a file for TODAY
            year = now.year
            day = now.day
        case 1:
            # First check if the argument is actually a number.
            # Then figure out if it's a year or a day
            number = args[0]

            if not number.isnumeric():
                raise Exception(
                    f"Argument must be a number. Received type: {type(number)}"
                )

            # Remove any leading zeroes
            number = number.lstrip("0")

            match len(number):
                case 4:
                    # The number must be a year.
                    # Now check that it's a valid year
                    number = int(number)
                    if not is_valid_year(number):
                        error_message = f"Year must be between {EARLIEST_YEAR} and {get_most_recent_year()}. Received: {number}"
                        raise Exception(error_message)

                    # Assume that the day is today
                    year = number
                    day = now.day
                case 1 | 2:
                    number = int(number)
                    if not is_valid_day(number):
                        error_message = (
                            f"Day must be between 1 and 25. Received: {number}"
                        )
                        raise Exception(error_message)

                    day = number
                    year = get_most_recent_year()
                case _:
                    raise Exception(
                        f"Invalid number of digits. Received: {len(number)}"
                    )

        case 2:
            # Either (year,day) or (day, year)
            num1, num2 = args[0:2]
            num1 = int(num1.lstrip("0"))
            num2 = int(num2.lstrip("0"))

            if is_valid_year(num1) and is_valid_day(num2):
                year = num1
                day = num2
            elif is_valid_year(num2) and is_valid_day(num1):
                year = num2
                day = num1
            else:
                error_message = f"Invalid arguments. Received: {num1}, {num2}"
                raise Exception(error_message)

        case _:
            error_message = (
                f"Invalid number of arguments: {len(args)}. Expected 0, 1 or 2"
            )
            raise Exception(error_message)

    return year, day


def urljoin(*args: tuple[str]) -> str:
    """
    Pretty much does the same thing as `urllib.parse.urljoin`, but this
    implementation lets you pass as many args as you want, rather than just
    two.
    """
    joined = args[0]
    for segment in args[1:]:
        # For some reason, if you don't do this weird stuff with the slash,
        # it replaces the last segment in the url rather than adding to it
        if not joined.endswith("/"):
            joined += "/"

        joined = urllib.parse.urljoin(joined, segment)

    return joined


def get_problem_url(year: int, day: int) -> str:
    """
    Returns the URL for the problem for the given year and day
    """
    year = str(year)
    day = str(day)

    url = urljoin(AOC_BASE_URL, year, "day", day)

    return url


def get_problem_html(url: str) -> str:
    """
    Fetches the AOC problem located at `url` and returns the HTML as a
    string.
    """

    response = requests.get(url)
    response.raise_for_status()

    return response.text


def get_problem_title(html: str) -> str:
    """
    Given the problem page's HTML, this function extracts the problem
    title and returns it as a string
    """
    soup = bs4.BeautifulSoup(html, "html.parser")

    # The majority of the important text is in an <article> tag with
    # class="day-desc"
    article = soup.select("article.day-desc")[0]

    # The title is in an <h2> tag
    title = article.h2.text

    return title.strip()


def get_problem_description(html: str) -> list[dict]:
    """
    Given an HTML document in string format, this function extracts the
    problem description and returns it as a string, as it appears on the
    page itself.
    """

    soup = bs4.BeautifulSoup(html, "html.parser")

    # The majority of the text we want is contained within an
    # <article> tag with class="day-desc"
    article = soup.select("article.day-desc")[0]

    lines = []

    # Basically, to facilitate formatting we do later when generating the
    # python file, we want to decipher which parts of the description are
    # actually describing the problem, and which parts are in the code-block
    # thingies.
    for child in article.children:
        text = child.text

        # We get the title separately from the description, so ignore it
        # here
        if text == get_problem_title(html):
            continue

        # The actual english descriptions are in <p> tags
        obj = {"content": child.text, "is_english": child.name == "p"}
        lines.append(obj)

    return lines


def format_description(description: list[dict]) -> str:
    """
    Pretty much, this function truncates each line to be ~75 characters, in
    order to make the description easier to read once it's put into the
    generated python script
    """
    return "".join(line["content"] for line in description).strip()

    result = ""
    for line in description:
        is_english = line["is_english"]
        content = line["content"]

        # If the content is a chunk of code or something, don't do anything
        # to it. This could confuse me when reading it in the multiline
        # string in the python file
        if not is_english:
            result += content
            continue

        # We know the content is just a pure English sentence. So let's
        # shorten it to ~75 characters to make it easier to read.
        for i in range(74, len(content) + 1, 75):
            char = content[i]

            # If the character at the 75th position is a space, we can
            # replace the space with a newline worry-free
            if char == " ":
                # content[i] = "\n"
                content = content[:i] + "\n" + content[i + 1 :]
                continue

            # Else, we want to keep the line as close to 75 characters as
            # possible. So find the nearest space, and put the newline there

            left = content.rindex(" ", 0, i)
            right = content.index(" ", i)

            index_for_newline = min(left, right, key=lambda x: abs(i - x))
            content = (
                content[:index_for_newline] + "\n" + content[index_for_newline + 1 :]
            )

        result += content

    return result.strip()


def get_input_url(problem_url: str) -> str:
    input_url = urljoin(problem_url, "input")
    return input_url


def init_webdriver() -> webdriver.Chrome:
    """
    Initialises and returns a selenium webdriver
    """

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
    options.add_argument("--disable-gpu")  # Disable GPU acceleration in headless mode

    service = ChromeService(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(options=options, service=service)

    return driver


def authenticate_via_reddit(driver: webdriver.Chrome, problem_url: str) -> None:
    """
    Uses selenium to login with reddit credentials. This authenticates us
    and therefore lets us access the problems' inputs
    """
    driver.get(problem_url)

    # There is a link to the reddit auth page at the bottom of the page.
    # It's in an <a> tag with inner text [Reddit]
    anchor_tag = driver.find_element(By.LINK_TEXT, "[Reddit]")

    # Navigate to the reddit login page
    anchor_tag.click()

    # Find username and password input elements, and input values from .env
    load_dotenv()
    username_input = driver.find_element(By.ID, "loginUsername")
    REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
    username_input.send_keys(REDDIT_USERNAME)

    password_input = driver.find_element(By.ID, "loginPassword")
    REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
    password_input.send_keys(REDDIT_PASSWORD)

    # Click the login button
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()

    # Wait until we are redirected to the page where it asks if we want to
    # allow AOC to access our reddit account
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("https://www.reddit.com/api/v1/authorize"))

    # Click the "Allow" button
    allow_button = driver.find_element(By.CSS_SELECTOR, "input.allow")
    allow_button.click()

    # Wait until we are redirected back to the AOC problem page
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains(problem_url))

    # If there's no timeout error, the authentication was successful


def get_input_html(driver: webdriver.Chrome, input_url: str) -> str:
    """
    Fetches the page for the input for the given problem and returns it as
    a string.
    """
    driver.get(input_url)
    return driver.page_source


def __get_raw_input(html: str) -> str:
    """
    Given the HTML for the input page, this function extracts the actual
    input and returns it as a string.
    """
    soup = bs4.BeautifulSoup(html, "html.parser")
    inner_text = soup.get_text()
    return inner_text.strip()


def get_file_path(year: int, day: int, python: bool = True) -> str:
    """
    Returns the path of the input file for the given year and day
    """
    year = str(year)
    day = str(day)

    # Get the path of the year directory.
    # And if it doesn't exist, create it
    year_dir_path = os.path.join(this_dir, year)
    if not os.path.exists(year_dir_path):
        os.makedirs(year_dir_path)

    # Get the path of the next directory.
    # And if it doesn't exist, create it
    next_dir_name = "python" if python else "inputs"
    next_dir_path = os.path.join(year_dir_path, next_dir_name)
    if not os.path.exists(next_dir_path):
        os.makedirs(next_dir_path)

    # Get the name and path of the new file
    extension = "py" if python else "txt"
    file_name = f"day{day}.{extension}"
    file_path = os.path.join(next_dir_path, file_name)

    return file_path


def write_input_to_file(input: str, year: int, day: int) -> None:
    """
    This function writes the given input to a file in the 'inputs' directory
    """

    file_path = get_file_path(year, day, False)

    # Do the actual writing of the input to the file
    with open(file_path, "w") as f:
        f.write(input)


def generate_python_file(
    title: str, description: str, problem_url: str, input_url: str, year: int, day: int
) -> None:
    """
    This function generates a python file for the given problem
    """
    file_path = get_file_path(year, day)

    with open(file_path, "w") as f:
        # fmt: off
        formatted = PYTHON_FILE_TEMPLATE.format(
            problem_url=problem_url,
            input_url=input_url,
            title=title,
            part1_description=description,
        )
        # fmt: on
        f.write(formatted)


def get_raw_input() -> str:
    """
    Using some ChatGPT-suggested magic, this function figures out the path
    of the file it was called from, then using that info, returns the
    corresponding problem input
    """

    # Do some magic to figure out where this function was called from.
    # Thank you ChatGPT for this haha. No idea what this code is doing tbh
    file_path = inspect.getouterframes(inspect.currentframe(), 2)[1].filename

    # The .stem part gets rid of the file extension
    # e.g. "day13"
    file_name = pathlib.Path(file_path).stem

    inputs_dir_path = os.path.abspath(
        os.path.join(file_path, os.pardir, os.pardir, "inputs")
    )
    input_file_path = os.path.join(inputs_dir_path, f"{file_name}.txt")
    with open(input_file_path) as f:
        return f.read()


def handle(
    answer,
    part: int,
    message: str = "Part {part}:\t{answer}\t({duration} seconds)",
) -> None:
    start = time.time()
    end = time.time()
    duration = end - start
    print(message.format(part=part, answer=answer, duration=duration))


def main():
    year, day = parse_args()
    url = get_problem_url(year, day)

    html = get_problem_html(url)

    # Scrape the input. We have to use selenium to do this, because AOC
    # requires us to be authenticated in order to access the input, because
    # apparently each user's input is different. So we use selenium
    # to log in with reddit, then go to the page containing the input, then
    # save it
    driver = init_webdriver()
    authenticate_via_reddit(driver, url)
    input_url = get_input_url(url)
    input_html = get_input_html(driver, input_url)
    driver.quit()
    input_str = __get_raw_input(input_html)

    # Write the raw input string to a file
    write_input_to_file(input_str, year, day)

    # Generate the python file
    title = get_problem_title(html)
    description = get_problem_description(html)
    description = format_description(description)

    generate_python_file(title, description, url, input_url, year, day)


if __name__ == "__main__":
    main()
