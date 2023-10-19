"""
Hockey Team Statistics Scraper
===============================
Author: Udit Kumar Chatterjee
Email: quantumudit@gmail.com
===============================

This module provides functionality to scrape hockey team statistics from a web page,
parse the data, and write it to a CSV file. It includes the data class "Hockey" to
represent hockey team statistics, functions to fetch data, find the URL of the next page,
and recursively scrape and write statistics to a CSV file.


Functions:
----------
1. fetch_hockey_stats(): Fetches and extracts hockey team statistics from a web page.
2. get_next_page_url(): Finds and returns the URL of the next page based on the current page URL.
3. scrape_and_write_stats(): Scrapes and writes hockey team statistics to a CSV file.
"""

# Import necessary libraries
import os
from csv import DictWriter
from dataclasses import asdict, dataclass, fields
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urljoin

import httpx
from selectolax.parser import HTMLParser


@dataclass
class Hockey:
    """
    A data class representing hockey team statistics.

    Attributes:
        team_name: The name of the hockey team.
        year: The year for the statistics.
        wins: The number of games won.
        losses: The number of games lost.
        ot_losses: The number of overtime losses.
        win_pct: The winning percentage.
        goals_for: The total number of goals scored by the team.
        goals_against: The total number of goals conceded by the team.
        goals_diff: The goal differential (goals for - goals against).
        scrape_timestamp: The timestamp (UTC) of when the data was scraped.
    """
    team_name: str
    year: str
    wins: str
    losses: str
    ot_losses: str
    win_pct: str
    goals_for: str
    goals_against: str
    goals_diff: str
    scrape_timestamp: str


# setting up constants
ROOT_URL = "https://www.scrapethissite.com/"
USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
HEADERS = {"User-Agent": USER_AGENT, "accept-language": "en-US"}
TIMEOUT = 100

# ========== Utility Functions ========== #


def fetch_hockey_stats(page_url: str) -> List[Dict]:
    """
    Fetches hockey team statistics by sending an HTTP GET request
    to the page URL and parsing the HTML content.

    Args:
        page_url (str): The URL of the web page containing the hockey team statistics.

    Returns:
        List[Dict]: A list of dictionaries, each representing the statistics of a hockey team.
    """
    # Send an HTTP GET request to the page URL and parse the HTML content.
    response = httpx.get(page_url, headers=HEADERS, timeout=TIMEOUT)
    parsed_html = HTMLParser(response.text)

    hockey_stats = []

    # Extract statistics for each hockey team from the HTML table.
    all_rows = parsed_html.css("div#page table tbody tr.team")
    for row in all_rows:
        team_stats = Hockey(
            team_name=row.css_first("td.name").text().strip(),
            year=row.css_first("td.year").text().strip(),
            wins=row.css_first("td.wins").text().strip(),
            losses=row.css_first("td.losses").text().strip(),
            ot_losses=row.css_first("td.ot-losses").text().strip(),
            win_pct=row.css_first("td.pct").text().strip(),
            goals_for=row.css_first("td.gf").text().strip(),
            goals_against=row.css_first("td.ga").text().strip(),
            goals_diff=row.css_first("td.diff").text().strip(),
            scrape_timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        hockey_stats.append(asdict(team_stats))
    return hockey_stats


def get_next_page_url(current_page_url: str) -> Optional[str]:
    """
    Find and return the URL of the next page based on the current page URL by
    parsing the HTML content. Returns the URL if found; otherwise, returns None.

    Args:
        current_page_url (str): The URL of the current page.

    Returns:
        Optional[str]: The URL of the next page, or None if no next page is found.
    """
    # Send an HTTP GET request to the current page URL and parse the HTML content.
    response = httpx.get(current_page_url, headers=HEADERS, timeout=TIMEOUT)
    parsed_html = HTMLParser(response.text)
    try:
        # Find and extract the URL of the next page element from the pagination section.
        next_page_element = parsed_html.css_first(
            "ul.pagination li a[aria-label='Next']").attrs["href"]
        next_page_url = urljoin(ROOT_URL, next_page_element)
        return next_page_url
    except AttributeError:
        # If no 'Next' page link is found, return None
        return None


def scrape_and_write_stats(start_page_url: str, csv_object: DictWriter) -> Optional[str]:
    """
    Recursively scrape and write hockey team statistics to a CSV file from a series of web pages.

    Args:
        start_page_url (str): The URL of the starting page to begin the scraping.
        csv_writer (csv.DictWriter): The CSV writer to write the extracted data.

    Returns:
        Optional[str]: A message indicating the HTTP error in the scraping process.
    """
    try:
        # Fetch hockey team statistics from the current page.
        hockey_team_stats = fetch_hockey_stats(page_url=start_page_url)

        # Find the URL of the next page, if available.
        next_page_url = get_next_page_url(current_page_url=start_page_url)
    except httpx.HTTPError as http_error:
        return f"HTTP error occurred while fetching {start_page_url}: {http_error}"

    # Write the fetched statistics to the CSV file.
    csv_object.writerows(hockey_team_stats)
    if next_page_url is not None:
        # If a 'Next' page is found, recursively continue scraping.
        scrape_and_write_stats(
            start_page_url=next_page_url, csv_object=csv_object)

# ========== Web Scraping & Data Load ========== #


if __name__ == "__main__":
    START_PAGE_URL = "https://www.scrapethissite.com/pages/forms/?page_num=1&per_page=100"
    OUTPUT_DIR_PATH = "./data/raw/"
    FILE_NAME = "hockey_teams_raw.csv"
    COLUMN_NAMES = [field.name for field in fields(Hockey)]

    # Ensure the output directory exists, or create it if it doesn't.
    os.makedirs(OUTPUT_DIR_PATH, exist_ok=True)
    output_file_path = os.path.join(OUTPUT_DIR_PATH, FILE_NAME)

    # Open the CSV file for writing and write the header.
    with open(output_file_path, mode='w', encoding="utf-8", newline="") as f:
        csv_writer = DictWriter(f, fieldnames=COLUMN_NAMES)
        csv_writer.writeheader()

        print("Scraping in Progress...")
        start_time = datetime.now()

        # Start the scraping process.
        scrape_and_write_stats(
            start_page_url=START_PAGE_URL, csv_object=csv_writer)
        print("Scraping Completed...")
        end_time = datetime.now()
        scraping_time = end_time - start_time

        print(f"Times Elapsed in Scraping: {scraping_time}")
