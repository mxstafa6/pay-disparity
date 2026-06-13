import json
import os
import sys
import time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv


BASE_URL = "https://www.alphavantage.co/query"
ROOT = Path(__file__).resolve().parents[1]
TICKERS_PATH = ROOT / "data" / "cleaned" / "manual_tickers.csv"
RAW_OUTPUT_DIR = ROOT / "data" / "raw" / "alphavantage"
OUTPUT_PATH = ROOT / "data" / "cleaned" / "operating_profit.csv"
FAILED_TICKERS_PATH = ROOT / "data" / "cleaned" / "failed_tickers.csv"


def ensure_directories():
    RAW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def fetch_income_statement(ticker, api_key):
    response = requests.get(
        BASE_URL,
        params={
            "function": "INCOME_STATEMENT",
            "symbol": ticker,
            "apikey": api_key,
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    if "Note" in payload or "Information" in payload or "Error Message" in payload:
        raise RuntimeError(json.dumps(payload, indent=2))
    if not payload or not payload.get("annualReports"):
        raise RuntimeError(f"Empty or missing annualReports response for {ticker}: {json.dumps(payload, indent=2)}")

    return payload


def main():
    load_dotenv(ROOT / ".env")
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    if not api_key:
        raise RuntimeError("Set ALPHAVANTAGE_API_KEY before running this script.")

    ensure_directories()
    tickers = pd.read_csv(TICKERS_PATH).dropna(subset=["Ticker"])
    single_ticker = sys.argv[1].strip() if len(sys.argv) > 1 else None
    if single_ticker:
        tickers = tickers[tickers["Ticker"].astype(str).str.strip() == single_ticker]

    rows = []
    failed_rows = []
    for row in tickers.itertuples(index=False):
        company = row.Company
        ticker = row.Ticker.strip()
        if not ticker:
            continue

        print(f"Fetching {company} ({ticker})")
        try:
            payload = fetch_income_statement(ticker, api_key)
        except Exception as exc:
            print(f"Failed for {company} ({ticker})")
            failed_rows.append(
                {
                    "Company": company,
                    "Ticker": ticker,
                    "error": str(exc),
                }
            )
            time.sleep(1.2)
            continue

        raw_path = RAW_OUTPUT_DIR / f"{ticker.lower().replace('.', '_')}.json"
        with raw_path.open("w") as handle:
            json.dump(payload, handle, indent=2)

        for report in payload.get("annualReports", []):
            fiscal_date = report.get("fiscalDateEnding")
            operating_income = report.get("operatingIncome")
            if not fiscal_date or operating_income in (None, "", "None"):
                continue

            rows.append(
                {
                    "Company": company,
                    "Ticker": ticker,
                    "Year": int(fiscal_date[:4]),
                    "operating_income": operating_income,
                    "reported_currency": payload.get("reportedCurrency", ""),
                }
            )
        time.sleep(1.2)

    if rows:
        pd.DataFrame(rows).sort_values(["Company", "Year"]).to_csv(OUTPUT_PATH, index=False)
        print(f"Saved operating profit data to {OUTPUT_PATH}")

    if failed_rows:
        pd.DataFrame(failed_rows).to_csv(FAILED_TICKERS_PATH, index=False)
        print(f"Saved failed ticker log to {FAILED_TICKERS_PATH}")


if __name__ == "__main__":
    main()
