import os
from dotenv import load_dotenv

#.env folder has "NEWSAPI_KEY" env var set and is located at top level (same as readme.md)
load_dotenv("../../.env")

import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from time import sleep

CACHE_DIR = Path("data/cache/news")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")  # Store your key in environment variables
if NEWSAPI_KEY is None:
    raise ValueError("Set your NewsAPI key in the NEWSAPI_KEY environment variable.")

def fetch_stock_news(
    ticker: str,
    company_name: str,
    days_back: int = 3,
    max_articles: int = 50,
    force_refresh: bool = False
) -> pd.DataFrame:
    """
    Fetch recent news headlines for a given stock using NewsAPI.

    Args:
        ticker (str): e.g., 'AAPL'
        company_name (str): e.g., 'Apple'
        days_back (int): How many days of news to retrieve
        max_articles (int): Limit on number of articles
        force_refresh (bool): Re-download even if cached

    Returns:
        pd.DataFrame: ['publishedAt', 'title', 'description', 'url', 'source']
    """
    assert NEWSAPI_KEY, "Set your NewsAPI key in the NEWSAPI_KEY environment variable."

    to_date = datetime.today()
    from_date = to_date - timedelta(days=days_back)

    cache_file = CACHE_DIR / f"{ticker}_{from_date.date()}_{to_date.date()}.csv"
    if cache_file.exists() and not force_refresh:
        return pd.read_csv(cache_file, parse_dates=["publishedAt"])

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": f"{ticker} OR {company_name}",
        "language": "en",
        "sortBy": "publishedAt",
        "from": from_date.date().isoformat(),
        "to": to_date.date().isoformat(),
        "pageSize": 100,  # Max per page
        "apiKey": NEWSAPI_KEY,
    }

    print(f"Fetching news for {ticker} ({company_name})...")
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"[Error] {ticker}: {response.status_code} - {response.text}")
        return pd.DataFrame()

    articles = response.json().get("articles", [])[:max_articles]
    df = pd.DataFrame([
        {
            "publishedAt": art["publishedAt"],
            "title": art["title"],
            "description": art["description"],
            "url": art["url"],
            "source": art["source"]["name"]
        } for art in articles
    ])
    if not df.empty:
        df["publishedAt"] = pd.to_datetime(df["publishedAt"])
        df.to_csv(cache_file, index=False)

    return df

