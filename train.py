import os
from src.data_loader import fetch_multiple_stocks_price_data, fetch_stock_news
import time
import pandas as pd


company_names = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "AMZN": "Amazon",
    "GOOG": "Alphabet",
    "META": "Meta Platforms",
    "NVDA": "Nvidia",
    "TSLA": "Tesla",
    "BRK-B": "Berkshire Hathaway",
    "UNH": "UnitedHealth Group",
    "JNJ": "Johnson & Johnson",
    "V": "Visa",
    "JPM": "JPMorgan Chase",
    "PG": "Procter & Gamble",
    "MA": "Mastercard",
    "HD": "Home Depot",
    "XOM": "ExxonMobil",
    "LLY": "Eli Lilly",
    "ABBV": "AbbVie",
    "MRK": "Merck",
    "PEP": "PepsiCo",
    "AVGO": "Broadcom",
    "COST": "Costco",
    "KO": "Coca-Cola",
    "BAC": "Bank of America",
    "WMT": "Walmart",
    "ADBE": "Adobe",
    "DIS": "Walt Disney",
    "PFE": "Pfizer",
    "CVX": "Chevron",
    "CSCO": "Cisco Systems",
    "TMO": "Thermo Fisher Scientific",
    "NFLX": "Netflix",
    "NKE": "Nike",
    "ABT": "Abbott Laboratories",
    "CRM": "Salesforce",
    "INTC": "Intel",
    "DHR": "Danaher",
    "TXN": "Texas Instruments",
    "AMD": "Advanced Micro Devices",
    "VZ": "Verizon",
    "LIN": "Linde",
    "HON": "Honeywell",
    "MCD": "McDonald's",
    "QCOM": "Qualcomm",
    "NEE": "NextEra Energy",
    "ACN": "Accenture",
    "PM": "Philip Morris International",
    "UPS": "United Parcel Service",
    "AMGN": "Amgen",
    "LOW": "Lowe's"
}


#Download the OHLCV data
t0=time.time()
stock_data = fetch_multiple_stocks_price_data(start_date="2025-01-01")
print("All stock data fetched! Time taken: {:.4f}s".format(time.time()-t0))

#Download the News Data
news_data = {}
t0=time.time()
for ticker in company_names:
    name = company_names.get(ticker, ticker)  # Fallback to ticker
    try:
        df = fetch_stock_news(ticker, name)
        news_data[ticker] = df
    except Exception as e:
        print(f"[Error] {ticker}: {e}")
    time.sleep(1.5)  # Avoid rate limiting

print("All News data fetched! Time taken: {:.4f}s".format(time.time()-t0))
news_data_df = pd.DataFrame(news_data)


#Merge the data

