import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.scrapethissite.com/pages/forms/"

def parse_and_extract_rows(soup: BeautifulSoup):
    """
    Extract table rows from the parsed HTML.
    """
    header = soup.find('tr')
    headers = [th.text.strip() for th in header.find_all('th')] if header else []

    teams = soup.find_all('tr', class_='team')

    for team in teams:
        row_dict = {}
        for header, col in zip(headers, team.find_all('td')):
            row_dict[header] = col.text.strip()
        yield row_dict


def scrape_all_pages():
    all_rows = []

    # Fetch the first page to determine pagination range
    print(f"Scraping {BASE_URL}...")
    resp = requests.get(BASE_URL, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for row in parse_and_extract_rows(soup):
        all_rows.append(row)

    # Determine the max page number from the pagination links
    max_page = 1
    pag = soup.find(class_="pagination")
    if pag:
        page_numbers = []
        for a in pag.find_all("a"):
            text = a.get_text(strip=True)
            if text.isdigit():
                try:
                    page_numbers.append(int(text))
                except ValueError:
                    pass
        if page_numbers:
            max_page = max(page_numbers)

    # Iterate remaining pages 2..max_page using the observed query param "page_num"
    for page_num in range(2, max_page + 1):
        page_url = f"{BASE_URL}?page_num={page_num}"
        print(f"Scraping {page_url}...")
        resp = requests.get(page_url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for row in parse_and_extract_rows(soup):
            all_rows.append(row)

    return all_rows


rows = scrape_all_pages()
print(f"Scraped {len(rows)} rows total.")
