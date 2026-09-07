import json
from pathlib import Path

import pandas as pd

BACKEND_DIR = Path(__file__).resolve().parent
CSV_PATH = BACKEND_DIR.parent / "tmdb_5000_movies.csv"


def parse_genres(raw: object) -> list[str]:
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return []
    try:
        items = json.loads(str(raw))
    except json.JSONDecodeError:
        return []
    if not isinstance(items, list):
        return []
    return [item["name"] for item in items if isinstance(item, dict) and "name" in item]


def parse_year(raw: object) -> int:
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return 0
    text = str(raw).strip()
    if len(text) < 4 or not text[:4].isdigit():
        return 0
    return int(text[:4])
