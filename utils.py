import csv

def save_athletes(athletes, filename="scraped_athletes.csv"):
    if not athletes:
        print("❌ No athletes to save.")
        return

    fieldnames = sorted({key for athlete in athletes for key in athlete.keys()})

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(athletes)

    print(f"✅ Saved {len(athletes)} athletes to {filename}")
