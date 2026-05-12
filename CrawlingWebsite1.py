# ---------------------------------------
# WHAT THIS SCRIPT DOES
# ---------------------------------------
# This script scrapes data from:
# https://en.wikipedia.org/wiki/List_of_highest-grossing_films
#
# IMPORTANT DIFFERENCE:
# ---------------------------------------
# This page contains structured data in TABLES (not paragraphs),
# so we extract data using:
# - <table> → entire table
# - <tr>    → rows
# - <td>    → columns
#
# We extract:
# 1. Rank
# 2. Film Title
# 3. Worldwide Gross
# 4. Year
#
# ---------------------------------------
# LIBRARIES TO INSTALL (via PyCharm interface)
# ---------------------------------------
# Install:
# - requests
# - beautifulsoup4
# - lxml
# ---------------------------------------

import requests
from bs4 import BeautifulSoup

# URL of the Wikipedia page (table-based page)
url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"

# Header to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Send request to the website
response = requests.get(url, headers=headers, timeout=10)

# Raise error if request fails
response.raise_for_status()

# Parse HTML using lxml parser
soup = BeautifulSoup(response.text, "lxml")

# ---------------------------------------
# DIFFERENT PART: TABLE EXTRACTION
# ---------------------------------------

# Find the first table with class 'wikitable'
table = soup.find("table", {"class": "wikitable"})

# Extract all rows from the table
rows = table.find_all("tr")

print("Top Highest Grossing Films:\n")

# Loop through each row (skip header row)
for row in rows[1:]:

    # Extract all columns in the row
    cols = row.find_all("td")

    # ---------------------------------------
    # IMPORTANT FIX: CHECK COLUMN LENGTH
    # ---------------------------------------
    # Some rows do NOT have all columns (Wikipedia tables are messy)
    # If we directly use cols[6], it may crash (IndexError)
    # So we only process rows that have enough columns

    if len(cols) >= 3:

        # Extract basic columns safely
        rank = cols[0].text.strip()     # Column 1 → Rank
        title = cols[1].text.strip()    # Column 2 → Movie Title
        gross = cols[2].text.strip()    # Column 3 → Worldwide Gross

        # ---------------------------------------
        # IMPROVED LOGIC FOR YEAR
        # ---------------------------------------
        # Instead of hardcoding index (like cols[6]),
        # we take the LAST column dynamically
        # This avoids "index out of range" errors

        year = cols[-1].text.strip()

        # Print extracted data
        print(rank, "|", title, "|", gross, "|", year)

    else:
        # Skip rows that don't match expected structure
        continue