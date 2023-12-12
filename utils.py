import os
import sys
import datetime
import urllib.parse

import requests
import bs4
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By


# The "home page" as it were
# Seems to show the problems for the most recent year by default
AOC_BASE_URL = "https://adventofcode.com/"

# The number of the month of December
DECEMBER = 12

# The first year that they did AOC.
EARLIEST_YEAR = 2015

CHROMEDRIVER_PATH = "./chromedriver"


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


def get_problem_description(html: str) -> str:
    """
    Given an HTML document in string format, this function extracts the
    problem description and returns it as a string, as it appears on the
    page itself.
    """

    soup = bs4.BeautifulSoup(html, "html.parser")

    # The majority of the text we want is contained within an
    # <article> tag with class="day-desc"

    article = soup.select("article.day-desc")[0]

    # This gets all the inner text within the <article> and its subtree.
    # As it is, the formatting is pretty much perfect.
    text = article.text

    # The only issue is that the title appears on the same line as the first
    # paragraph. So we should fix that.
    title = article.h2.text.strip()
    title_with_newlines = title + "\n\n"
    text = text.replace(title, title_with_newlines)

    # Strip for good measure
    text = text.strip()

    return text


def get_problem_input_url(problem_url: str) -> str:
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


def authenticate_via_reddit(problem_html: str) -> None:
    """
    Uses selenium to login with reddit credentials. This authenticates us
    and therefore lets us access the problems' inputs
    """
    soup = bs4.BeautifulSoup(problem_html, "html.parser")

    # There is a link to the reddit auth page at the bottom of the page.
    # It's in an <a> tag with inner text [Reddit]
    anchor_tag = soup.find(lambda tag: tag.name == "a" and tag.text == "[Reddit]")
    href = anchor_tag["href"]
    full_url = urljoin(AOC_BASE_URL, href)

    # Init selenium webdriver
    driver = init_webdriver()

    # Navigate to the reddit login page
    driver.get(full_url)

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


def get_problem_input_file(input_url: str) -> str:
    """
    Fetches the input for the given problem and returns it as a string.
    """
    response = requests.get(input_url)
    if not response.ok:
        # Most likely we need to authenticate
        response.raise_for_status()

    return response.text


def main():
    year, day = parse_args()
    url = get_problem_url(year, day)

    html = get_problem_html(url)
    description = get_problem_description(html)

    authenticate_via_reddit(html)

    input_url = get_problem_input_url(url)
    input_file = get_problem_input_file(input_url)
    print(input_file)


if __name__ == "__main__":
    main()
