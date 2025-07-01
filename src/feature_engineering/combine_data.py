import pandas as pd
from pathlib import Path
from tqdm import tqdm
import os

PRICE_DIR = Path("data/cache/prices")
NEWS_DIR = Path("data/cache/news")
SENTIMENT_COLS = ["negative", "neutral", "positive", "predicted_sentiment"]

def load_prices(ticker):
    filename = [x for x in os.listdir(PRICE_DIR) if ticker in x][0]
    df = pd.read_csv(PRICE_DIR / filename, parse_dates=["date"])
    df["ticker"] = ticker
    return df

def load_news_with_sentiment(ticker):
    filename = [x for x in os.listdir(NEWS_DIR) if ticker in x][0]
    path = NEWS_DIR / filename
    if not path.exists():
        return pd.DataFrame(columns=["publishedAt", "predicted_sentiment"])
    
    df = pd.read_csv(path, parse_dates=["publishedAt"])
    df["date"] = df["publishedAt"].dt.floor("D")
    
    # Convert sentiment to score: pos=1, neutral=0, neg=-1
    sentiment_map = {"positive": 1, "neutral": 0, "negative": -1}
    df["sentiment_score"] = df["predicted_sentiment"].map(sentiment_map)

    df_grouped = df.groupby("date").agg({
        "sentiment_score": "mean",
        "predicted_sentiment": "count"
    }).rename(columns={"predicted_sentiment": "headline_count"}).reset_index()
    
    return df_grouped

def create_features(prices: pd.DataFrame, sentiment: pd.DataFrame) -> pd.DataFrame:
    df = prices.copy()

    # Lag features
    df["lag_1"] = df["adj_close"].shift(1)
    df["lag_3"] = df["adj_close"].shift(3)
    df["rolling_mean_3"] = df["adj_close"].rolling(3).mean()
    df["rolling_std_5"] = df["adj_close"].rolling(5).std()
    df["target_return"] = df["adj_close"].pct_change(1).shift(-1)

    # Merge sentiment
    df = df.merge(sentiment, on="date", how="left")

    # Fill missing sentiment with 0
    df["sentiment_score"] = df["sentiment_score"].fillna(0)
    df["headline_count"] = df["headline_count"].fillna(0)

    return df.dropna(subset=["lag_1", "target_return"])

def build_full_panel(tickers: list[str]) -> pd.DataFrame:
    all_dfs = []
    for ticker in tqdm(tickers, desc="Combining data"):
        try:
            prices = load_prices(ticker)
            sentiment = load_news_with_sentiment(ticker)
            features = create_features(prices, sentiment)
            all_dfs.append(features)
        except Exception as e:
            print(f"[Error] {ticker}: {e}")
    return pd.concat(all_dfs, ignore_index=True)

if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "META", "TSLA"]
    full_panel = build_full_panel(tickers)
    full_panel.to_csv("data/cache/full_panel.csv", index=False)