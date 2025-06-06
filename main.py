
from fastapi import FastAPI, Request
from dispatch_scraper import run_scraper  # you already have this script

app = FastAPI()

@app.post("/scrape")
async def scrape_endpoint(request: Request):
    data = await request.json()
    sport = data.get("sport")
    nationality = data.get("nationality")

    if not sport or not nationality:
        return {"error": "Missing sport or nationality"}

    results = run_scraper(sport=sport, nationality=nationality)
    return {"athletes": results}
