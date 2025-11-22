import requests
from bs4 import BeautifulSoup
from typing import Dict, Iterable, List
import json
from pathlib import Path

SIMPLE_URL = "https://www.scrapethissite.com/pages/simple/"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
}


def fetch_soup(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_countries(soup: BeautifulSoup) -> Iterable[Dict[str, object]]:
    country_divs = soup.select(".country")
    for div in country_divs:
        name_el = div.select_one(".country-name")
        capital_el = div.select_one(".country-capital")
        population_el = div.select_one(".country-population")
        area_el = div.select_one(".country-area")

        name = (name_el.get_text(strip=True) if name_el else "")  # type: ignore[assignment]
        capital = (capital_el.get_text(strip=True) if capital_el else "")

        population_text = population_el.get_text(strip=True) if population_el else "0"
        population_text = population_text.replace(",", "")
        try:
            population = int(population_text)
        except ValueError:
            population = 0

        area_text = area_el.get_text(strip=True) if area_el else "0"
        area_text = area_text.replace(",", "")
        try:
            area_km2 = float(area_text)
        except ValueError:
            area_km2 = 0.0

        yield {
            "name": name,
            "capital": capital,
            "population": population,
            "area_km2": area_km2,
        }


def scrape_countries() -> List[Dict[str, object]]:
    soup = fetch_soup(SIMPLE_URL)
    return list(parse_countries(soup))


if __name__ == "__main__":
    countries = scrape_countries()
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "countries.json"
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(countries, f, ensure_ascii=False, indent=2)
    # Print JSON to stdout
    print(json.dumps(countries, ensure_ascii=False, indent=2))


