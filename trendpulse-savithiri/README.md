# TrendPulse

TrendPulse fetches live trending cryptocurrency data from CoinGecko, cleans it, analyzes the strongest movers, and creates a visual summary.

## Project structure

- `scripts/01_fetch_trends.py` fetches the data from the live API.
- `scripts/02_clean_data.py` normalizes the raw payload into a clean table.
- `scripts/03_analyze_data.py` computes summary metrics and key insights.
- `scripts/04_visualize_data.py` generates a bar chart of the top movers.

## Setup

```bash
python -m pip install -r requirements.txt
```

## Run the pipeline

```bash
python scripts/01_fetch_trends.py
python scripts/02_clean_data.py
python scripts/03_analyze_data.py
python scripts/04_visualize_data.py
```

Generated outputs will be saved under the `data/` and `outputs/` directories.
