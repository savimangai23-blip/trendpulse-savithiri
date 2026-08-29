from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEANED_INPUT_PATH = PROJECT_ROOT / "data" / "cleaned" / "trending_cleaned.csv"
ANALYSIS_OUTPUT_PATH = PROJECT_ROOT / "data" / "analysis" / "trending_summary.json"


def read_clean_data() -> pd.DataFrame:
    return pd.read_csv(CLEANED_INPUT_PATH)


def build_summary(df: pd.DataFrame) -> dict:
    top_gainer = df.loc[df["price_change_pct_24h"].idxmax()]
    top_market_cap = df.loc[df["market_cap_usd"].idxmax()]
    top_volume = df.loc[df["volume_usd"].idxmax()]

    summary = {
        "total_coins": int(len(df)),
        "average_price_usd": round(float(df["price_usd"].mean()), 2),
        "average_24h_change_pct": round(float(df["price_change_pct_24h"].mean()), 2),
        "top_gainer": {
            "name": top_gainer["name"],
            "symbol": top_gainer["symbol"],
            "price_change_pct_24h": round(float(top_gainer["price_change_pct_24h"]), 2),
        },
        "largest_market_cap": {
            "name": top_market_cap["name"],
            "symbol": top_market_cap["symbol"],
            "market_cap_usd": round(float(top_market_cap["market_cap_usd"]), 2),
        },
        "highest_volume": {
            "name": top_volume["name"],
            "symbol": top_volume["symbol"],
            "volume_usd": round(float(top_volume["volume_usd"]), 2),
        },
    }
    return summary


def main() -> None:
    if not CLEANED_INPUT_PATH.exists():
        raise FileNotFoundError(f"Clean data not found: {CLEANED_INPUT_PATH}. Run 02_clean_data.py first.")

    print("Analyzing trending data...")
    df = read_clean_data()
    summary = build_summary(df)

    ANALYSIS_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ANALYSIS_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print(f"Saved analysis summary to: {ANALYSIS_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
