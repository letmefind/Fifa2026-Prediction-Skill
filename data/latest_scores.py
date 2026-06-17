from __future__ import annotations

import os
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from config import Config, load_config
from data.adapters import MATCH_COLUMNS


FOOTBALL_DATA_URL = "https://api.football-data.org/v4/matches"
API_FOOTBALL_URL = "https://v3.football.api-sports.io/fixtures"


def _empty_matches() -> pd.DataFrame:
    return pd.DataFrame(columns=MATCH_COLUMNS)


def _standardize(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return _empty_matches()
    missing = sorted(set(MATCH_COLUMNS) - set(frame.columns))
    if missing:
        raise ValueError(f"latest results missing columns: {missing}")
    standardized = frame[MATCH_COLUMNS].copy()
    standardized["date"] = pd.to_datetime(standardized["date"], errors="coerce")
    standardized["home_score"] = pd.to_numeric(standardized["home_score"], errors="coerce")
    standardized["away_score"] = pd.to_numeric(standardized["away_score"], errors="coerce")
    standardized = standardized.dropna(subset=["date", "home_team", "away_team", "home_score", "away_score"])
    if standardized.empty:
        return _empty_matches()
    standardized["home_score"] = standardized["home_score"].astype(int)
    standardized["away_score"] = standardized["away_score"].astype(int)
    standardized["neutral"] = standardized["neutral"].fillna(True).astype(bool)
    return standardized.sort_values("date").reset_index(drop=True)


def load_latest_results_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return _empty_matches()
    return _standardize(pd.read_csv(path))


def _football_data_matches(config: Config) -> pd.DataFrame:
    token = os.getenv("FOOTBALL_DATA_API_KEY")
    if not token:
        return _empty_matches()

    today = date.today()
    start = today - timedelta(days=config.data.latest_lookback_days)
    response = requests.get(
        FOOTBALL_DATA_URL,
        headers={"X-Auth-Token": token},
        params={"dateFrom": start.isoformat(), "dateTo": today.isoformat()},
        timeout=20,
    )
    response.raise_for_status()
    rows: list[dict[str, Any]] = []
    for item in response.json().get("matches", []):
        score = item.get("score", {}).get("fullTime", {})
        if item.get("status") != "FINISHED" or score.get("home") is None or score.get("away") is None:
            continue
        rows.append(
            {
                "date": item.get("utcDate"),
                "home_team": item.get("homeTeam", {}).get("name"),
                "away_team": item.get("awayTeam", {}).get("name"),
                "home_score": score.get("home"),
                "away_score": score.get("away"),
                "home_xg": None,
                "away_xg": None,
                "neutral": True,
                "competition": item.get("competition", {}).get("name", "Football-Data"),
            }
        )
    return _standardize(pd.DataFrame(rows, columns=MATCH_COLUMNS))


def _api_football_matches() -> pd.DataFrame:
    token = os.getenv("API_FOOTBALL_KEY")
    if not token:
        return _empty_matches()

    response = requests.get(
        API_FOOTBALL_URL,
        headers={"x-apisports-key": token},
        params={"last": 100},
        timeout=20,
    )
    response.raise_for_status()
    rows: list[dict[str, Any]] = []
    for item in response.json().get("response", []):
        status = item.get("fixture", {}).get("status", {}).get("short")
        goals = item.get("goals", {})
        if status not in {"FT", "AET", "PEN"} or goals.get("home") is None or goals.get("away") is None:
            continue
        league = item.get("league", {})
        rows.append(
            {
                "date": item.get("fixture", {}).get("date"),
                "home_team": item.get("teams", {}).get("home", {}).get("name"),
                "away_team": item.get("teams", {}).get("away", {}).get("name"),
                "home_score": goals.get("home"),
                "away_score": goals.get("away"),
                "home_xg": None,
                "away_xg": None,
                "neutral": True,
                "competition": league.get("name", "API-Football"),
            }
        )
    return _standardize(pd.DataFrame(rows, columns=MATCH_COLUMNS))


def load_latest_matches(config: Config | None = None, include_api: bool = True) -> pd.DataFrame:
    cfg = config or load_config()
    frames = [load_latest_results_csv(cfg.data.latest_results_csv)]

    if include_api:
        for loader in (_football_data_matches, _api_football_matches):
            try:
                frame = loader(cfg) if loader is _football_data_matches else loader()
                if not frame.empty:
                    frames.append(frame)
            except Exception:
                # Prediction must remain available even when a third-party feed is down.
                continue

    combined = pd.concat(frames, ignore_index=True) if frames else _empty_matches()
    return _dedupe_matches(_standardize(combined))


def _dedupe_matches(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return frame
    dedupe = frame.copy()
    dedupe["date_key"] = pd.to_datetime(dedupe["date"]).dt.date.astype(str)
    dedupe["home_key"] = dedupe["home_team"].astype(str).str.lower().str.strip()
    dedupe["away_key"] = dedupe["away_team"].astype(str).str.lower().str.strip()
    dedupe = dedupe.drop_duplicates(["date_key", "home_key", "away_key"], keep="last")
    return dedupe.drop(columns=["date_key", "home_key", "away_key"]).sort_values("date").reset_index(drop=True)


def merge_match_frames(base_matches: pd.DataFrame, latest_matches: pd.DataFrame) -> pd.DataFrame:
    if latest_matches.empty:
        return base_matches.sort_values("date").reset_index(drop=True)
    merged = pd.concat([base_matches, latest_matches], ignore_index=True)
    return _dedupe_matches(_standardize(merged))


def latest_data_status(config: Config | None = None, latest_matches: pd.DataFrame | None = None) -> dict[str, object]:
    cfg = config or load_config()
    latest = latest_matches if latest_matches is not None else load_latest_matches(cfg, include_api=False)
    latest_date = None
    if not latest.empty:
        latest_date = pd.to_datetime(latest["date"]).max().date().isoformat()
    return {
        "latest_results_csv": str(cfg.data.latest_results_csv),
        "latest_results_csv_exists": cfg.data.latest_results_csv.exists(),
        "latest_matches_loaded": int(len(latest)),
        "latest_match_date": latest_date,
        "football_data_api_configured": bool(os.getenv("FOOTBALL_DATA_API_KEY")),
        "api_football_configured": bool(os.getenv("API_FOOTBALL_KEY")),
        "lookback_days": cfg.data.latest_lookback_days,
        "checked_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
    }
