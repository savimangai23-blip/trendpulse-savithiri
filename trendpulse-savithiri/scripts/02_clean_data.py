from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_INPUT_PATH = PROJECT_ROOT / "data" / "raw" / "trending_raw.json"
CLEANED_OUTPUT_PATH = PROJECT_ROOT / "data" / "cleaned" / "trending_cleaned.csv"


def parse_numeric(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)

    cleaned = str(value).strip()
    cleaned = cleaned.replace("$", "").replace(",", "").replace("%", "")
    cleaned = re.sub(r"[^0-9.\-]", "", cleaned)

    if cleaned in {"", "-", "."}:
        return None

    try:
        return float(cleaned)
    except ValueError:
        return None


def extract_coin(item: dict) -> dict:
    data = item.get("data", {})
    price_change = data.get("price_change_percentage_24h", {})
    if isinstance(price_change, dict):
        pct_change = price_change.get("usd")
    else:
        pct_change = None

    return {
        "rank": item.get("market_cap_rank") or item.get("score"),
        "name": item.get("name"),
        "symbol": item.get("symbol"),
        "price_usd": parse_numeric(data.get("price")),
        "market_cap_usd": parse_numeric(data.get("market_cap")),
        "volume_usd": parse_numeric(data.get("total_volume")),
        "price_change_pct_24h": parse_numeric(pct_change),
        "score": item.get("score"),
    }


def load_raw_data():
    with RAW_INPUT_PATH.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    coins = payload.get("coins", [])
    rows = [extract_coin(coin.get("item", {})) for coin in coins]
    return pd.DataFrame(rows)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.dropna(subset=["name", "symbol"]).copy()
    cleaned["rank"] = pd.to_numeric(cleaned["rank"], errors="coerce").fillna(-1).astype(int)
    cleaned["price_usd"] = pd.to_numeric(cleaned["price_usd"], errors="coerce")
    cleaned["market_cap_usd"] = pd.to_numeric(cleaned["market_cap_usd"], errors="coerce")
    cleaned["volume_usd"] = pd.to_numeric(cleaned["volume_usd"], errors="coerce")
    cleaned["price_change_pct_24h"] = pd.to_numeric(cleaned["price_change_pct_24h"], errors="coerce")
    cleaned["score"] = pd.to_numeric(cleaned["score"], errors="coerce")
    return cleaned.sort_values("rank").reset_index(drop=True)


def main() -> None:
    if not RAW_INPUT_PATH.exists():
        raise FileNotFoundError(f"Raw data not found: {RAW_INPUT_PATH}. Run 01_fetch_trends.py first.")

    print("Cleaning trending data...")
    df = load_raw_data()
    cleaned = clean_dataframe(df)

    CLEANED_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(CLEANED_OUTPUT_PATH, index=False)
    print(f"Saved cleaned data to: {CLEANED_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
