import requests
from bs4 import BeautifulSoup


def parse_sidearm_fields(raw_fields):
    # Example: "6-2 / Freshman / Sydney, Australia / St. Kevin's College"
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


def scrape_sidearm_roster(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    cards = soup.select(".sidearm-roster-player")
    print(f"📥 Fetching Sidearm roster: {url}")
    print(f"🔍 Found {len(cards)} cards on page.")

    athletes = []
    for card in cards:
        name_tag = card.select_one(".sidearm-roster-player-name")
        raw_fields_tag = card.select_one(".sidearm-roster-player-details")

        name = name_tag.text.strip() if name_tag else None
        raw_fields = raw_fields_tag.text.strip() if raw_fields_tag else ""

        parsed_fields = parse_sidearm_fields(raw_fields)

        athlete = {
            "name": name,
            "height": parsed_fields["height"],
            "year": parsed_fields["year"],
            "hometown": parsed_fields["hometown"],
            "high_school": parsed_fields["high_school"],
            "photo": None,
        }

        # Try to grab the athlete photo
        img_tag = card.select_one("img")
        if img_tag and img_tag.get("src"):
            athlete["photo"] = img_tag["src"].strip()

        athletes.append(athlete)

    print(f"✅ Found {len(athletes)} athletes.")
    return athletes
