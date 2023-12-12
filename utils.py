import datetime
import urllib.parse
import requests

# The "home page" as it were
# Seems to show the problems for the most recent year by default
AOC_BASE_URL = "https://adventofcode.com/"

# The number of the month of December
DECEMBER = 12


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


def get_year_page_url(year: int = get_most_recent_year()) -> str:
    """
    Gets the URL for the most recent year of AOC if `year` is not specified,
    else gets the year specified by `year`.
    """
    year = str(year)

    url = urllib.parse.urljoin(AOC_BASE_URL, year)

    return url


def get_year_page_html(year: int = get_most_recent_year()) -> str:
    """
    Gets the HTML for the most recent year of AOC if `year` is not specified,
    else gets page for the the year specified by `year`.
    """

    url = get_year_page_url(year)

    response = requests.get(url)

    if not response.ok:
        error_message = f"{url} -- {response.status_code} -- {response.reason}"
        raise Exception(error_message)

    return response.text
