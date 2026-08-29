from __future__ import annotations

import json
from pathlib import Path

import requests

API_URL = "https://api.coingecko.com/api/v3/search/trending"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "trending_raw.json"


def fetch_trending_data() -> dict:
    response = requests.get(API_URL, timeout=20)
    response.raise_for_status()
    payload = response.json()

    if "coins" not in payload:
        raise ValueError("Unexpected API response: 'coins' not found.")

    return payload


def save_raw_data(payload: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    print("Fetching live trending data from CoinGecko...")
    payload = fetch_trending_data()
    save_raw_data(payload, RAW_OUTPUT_PATH)
    print(f"Saved raw trending data to: {RAW_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
