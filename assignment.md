# Assignment

## Brief

Write the Python codes for the following questions.

## Instructions

Paste the answer as Python in the answer code section below each question.

### Question 1

Question: The scraping of `https://www.scrapethissite.com/pages/forms/` in the last section assumes a hardcoded (fixed) no of pages. Can you improve the code by removing the hardcoded no of pages and instead use the `»` button to determine if there are more pages to scrape? Hint: Use a `while` loop.

```python
def parse_and_extract_rows(soup: BeautifulSoup):
    """
    Extract table rows from the parsed HTML.

    Args:
        soup: The parsed HTML.

    Returns:
        An iterator of dictionaries with the data from the current page.
    """
    header = soup.find('tr')
    headers = [th.text.strip() for th in header.find_all('th')]
    teams = soup.find_all('tr', 'team')
    for team in teams:
        row_dict = {}
        for header, col in zip(headers, team.find_all('td')):
            row_dict[header] = col.text.strip()
        yield row_dict
```

Answer:

```python
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.scrapethissite.com/pages/forms/"

def parse_and_extract_rows(soup: BeautifulSoup):
    """
    Extract table rows from the parsed HTML.
    """
    # Get the table header row
    # Finds the first <tr> → table header row.
    # Extracts every <th> text (column names).
    header = soup.find('tr')
    headers = [th.text.strip() for th in header.find_all('th')]

    # Get all table rows representing teams
    # Finds every <tr class="team"> row → team data.
    teams = soup.find_all('tr', class_='team')

    # Build dictionaries for each team row
    # This loops through each <tr class="team"> row and pairs:
    for team in teams:
        row_dict = {}
        for header, col in zip(headers, team.find_all('td')):
            row_dict[header] = col.text.strip()
        yield row_dict


def scrape_all_pages():
    # Start at page 1. Empty list to store all scraped data.
    page_num = 1
    all_rows = []

    while True:
        print(f"Scraping page {page_num}...")

        # request page
        # Loads the page’s HTML and parses it.
        resp = requests.get(f"{BASE_URL}?page={page_num}")
        soup = BeautifulSoup(resp.text, "html.parser")

        # parse the rows on this page
        # Each yielded row is appended into a big list.
        for row in parse_and_extract_rows(soup):
            all_rows.append(row)

        # detect the pagination "»" button
        # Check for the “Next” button (»)
        # If that <a> exists → there’s a next page.
        next_button = soup.select_one("li.next > a")

        # stop if button is missing or disabled
        if not next_button or "disabled" in next_button.parent.get("class", []):
            break

        # otherwise: go to next page
        page_num += 1

    # Return all scraped items
    return all_rows


# Example usage:
rows = scrape_all_pages()
print(f"Scraped {len(rows)} rows total.")


```

## Submission

- Submit the URL of the GitHub Repository that contains your work to NTU black board.
- Should you reference the work of your classmate(s) or online resources, give them credit by adding either the name of your classmate or URL.
- Ref : Generate via ChatGPT
