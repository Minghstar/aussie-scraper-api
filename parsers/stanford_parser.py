import requests
from bs4 import BeautifulSoup

def parse_stanford_fields(raw_fields):
    parts = [part.strip() for part in raw_fields.split('/')]

    height = year = hometown = high_school = None
    if len(parts) == 4:
        height, year, hometown, high_school = parts
    elif len(parts) == 3:
        height, year, hometown = parts
    elif len(parts) == 2:
        height, year = parts
    elif len(parts) == 1:
        height = parts[0]

    return {
        "height": height,
        "year": year,
        "hometown": hometown,
        "high_school": high_school,
    }

def scrape_stanford_roster(url):
    athletes = []

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    cards = soup.find_all("div", class_="roster-card-item")

    print(f"🔍 Found {len(cards)} cards on Stanford roster page.")

    for card in cards:
        # Extract name from the h2/h3 tag inside the card
        name_tag = card.find(["h2", "h3"])
        name = name_tag.get_text(strip=True) if name_tag else "N/A"

        # Extract profile fields (e.g., height/year/hometown/etc.)
        fields_div = card.find("div", class_="roster-player-card-profile-fields")
        raw_fields = fields_div.get_text(" / ", strip=True) if fields_div else ""

        parsed = parse_stanford_fields(raw_fields)

        athlete = {
            "name": name,
            "height": parsed["height"],
            "year": parsed["year"],
            "hometown": parsed["hometown"],
            "high_school": parsed["high_school"],
        }

        athletes.append(athlete)

    return athletes

