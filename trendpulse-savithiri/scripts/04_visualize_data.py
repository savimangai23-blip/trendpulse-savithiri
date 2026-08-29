from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEANED_INPUT_PATH = PROJECT_ROOT / "data" / "cleaned" / "trending_cleaned.csv"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "top_movers_chart.png"


def load_data() -> pd.DataFrame:
    return pd.read_csv(CLEANED_INPUT_PATH)


def plot_top_movers(df: pd.DataFrame) -> None:
    top = df.sort_values("price_change_pct_24h", ascending=False).head(10).copy()
    if top.empty:
        raise ValueError("No data available to visualize.")

    top["label"] = top["symbol"].astype(str)
    plt.figure(figsize=(12, 8))
    bars = plt.bar(top["label"], top["price_change_pct_24h"], color=["#2ecc71" if v >= 0 else "#e74c3c" for v in top["price_change_pct_24h"]])
    plt.axhline(0, color="black", linewidth=0.8)
    plt.title("Top 10 Trending Coins by 24h Price Change")
    plt.xlabel("Symbol")
    plt.ylabel("24h Price Change (%)")
    plt.xticks(rotation=45, ha="right")

    for bar, value in zip(bars, top["price_change_pct_24h"]):
        label = f"{value:.2f}%"
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), label, ha="center", va="bottom" if value >= 0 else "top", fontsize=9)

    plt.tight_layout()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_PATH, dpi=200)
    plt.close()


def main() -> None:
    if not CLEANED_INPUT_PATH.exists():
        raise FileNotFoundError(f"Clean data not found: {CLEANED_INPUT_PATH}. Run 02_clean_data.py first.")

    print("Generating visualization...")
    df = load_data()
    plot_top_movers(df)
    print(f"Saved chart to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
