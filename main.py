
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "✅ Aussie Scraper API is live and working!"}
