# dispatch_scraper.py

import pandas as pd
from bs4 import BeautifulSoup
from detectors.detect_platform import detect_platform
from parsers.sidearm_parser import scrape_sidearm_roster
from parsers.stanford_parser import scrape_stanford_roster
from utils import save_athletes

def dispatch_and_scrape(csv_path):
    df = pd.read_csv(csv_path)
    all_athletes = []

    for _, row in df.iterrows():
        for sport in ["tennis", "golf"]:
            url_col = f"{sport}_roster_url"
            platform_col = f"{sport}_roster_platform"

            if pd.isna(row[url_col]):
                continue

            url = row[url_col]
            college = row["college"]
            platform = row.get(platform_col) or detect_platform(url)

            print(f"🎯 {college} ({sport}) → {platform} → {url}")

            athletes = []

            if platform == "sidearm":
                print(f"📥 Fetching Sidearm roster: {url}")
                athletes = scrape_sidearm_roster(url)

            elif platform == "stanford":
                print(f"📥 Fetching Stanford roster: {url}")
                athletes = scrape_stanford_roster(url)

            if athletes:
                for athlete in athletes:
                    athlete["college"] = college
                    athlete["sport"] = sport
                    athlete["roster_url"] = url
                print(f"✅ Found {len(athletes)} athletes.")
                all_athletes.extend(athletes)
            else:
                print("❌ No athletes found.")

    save_athletes(all_athletes)
    print(f"✅ Saved {len(all_athletes)} athletes to scraped_athletes.csv")

# 👇 Add this to make the script callable by main.py
def run_scraper():
    csv_path = "college_rosters.csv"  # make sure this CSV exists in your repo
    dispatch_and_scrape(csv_path)





