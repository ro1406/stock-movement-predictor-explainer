import os
from pathlib import Path
import yfinance as yf
import pandas as pd
from datetime import datetime

# Folder to cache downloaded data
CACHE_DIR = Path("data/cache/prices")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Default list of popular S&P 500 stocks (modifiable)
TOP_50_TICKERS = [
    "AAPL", "MSFT", "AMZN", "GOOG", "META", "NVDA", "TSLA", "BRK-B", "UNH", "JNJ",
    "V", "JPM", "PG", "MA", "HD", "XOM", "LLY", "ABBV", "MRK", "PEP",
    "AVGO", "COST", "KO", "BAC", "WMT", "ADBE", "DIS", "PFE", "CVX", "CSCO",
    "TMO", "NFLX", "NKE", "ABT", "CRM", "INTC", "DHR", "TXN", "AMD", "VZ",
    "LIN", "HON", "MCD", "QCOM", "NEE", "ACN", "PM", "UPS", "AMGN", "LOW"
]

def fetch_stock_price_data(
    ticker: str,
    start_date: str = "2020-01-01",
    end_date: str = None,
    force_refresh: bool = False
) -> pd.DataFrame:
    """
    Fetch historical OHLCV price data for a single stock ticker.
    """
    if end_date is None:
        end_date = datetime.today().strftime("%Y-%m-%d")

    cache_file = CACHE_DIR / f"{ticker}_{start_date}_{end_date}.csv"

    if cache_file.exists() and not force_refresh:
        return pd.read_csv(cache_file, parse_dates=["date"])

    print(f"Downloading data for {ticker}...")
    df = yf.download(ticker, start=start_date, end=end_date)

    if df.empty:
        print(f"[Warning] No data returned for {ticker}")
        return pd.DataFrame()

    df = df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "adj_close",
        "Volume": "volume"
    }).reset_index()

    df["date"] = pd.to_datetime(df["Date"])
    df.drop(columns=["Date"], inplace=True)

    df.to_csv(cache_file, index=False)
    return df


def fetch_multiple_stocks_price_data(
    tickers: list[str] = None,
    start_date: str = "2020-01-01",
    end_date: str = None,
    force_refresh: bool = False
) -> dict[str, pd.DataFrame]:
    """
    Fetch price data for multiple stock tickers.

    Returns:
        dict: {ticker: DataFrame}
    """
    if tickers is None:
        tickers = TOP_50_TICKERS

    all_data = {}
    for ticker in tickers:
        try:
            df = fetch_stock_price_data(ticker, start_date, end_date, force_refresh)
            if not df.empty:
                all_data[ticker] = df
        except Exception as e:
            print(f"[Error] Failed to fetch {ticker}: {e}")

    return all_data


if __name__ == "__main__":
    stock_data = fetch_multiple_stocks_price_data(start_date="2025-01-01")
    # Access AAPL data:
    aapl_df = stock_data["AAPL"]
    print(aapl_df.head())