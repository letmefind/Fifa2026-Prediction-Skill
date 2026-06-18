from __future__ import annotations

import os
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from config import Config, load_config
from data.adapters import MATCH_COLUMNS
from data.team_aliases import fixture_pair_key, normalize_team_name


FOOTBALL_DATA_URL = "https://api.football-data.org/v4/matches"
API_FOOTBALL_URL = "https://v3.football.api-sports.io/fixtures"


def load_local_env(path: Path | None = None) -> None:
    env_path = path or Path(__file__).resolve().parents[1] / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _empty_matches() -> pd.DataFrame:
    return pd.DataFrame(columns=MATCH_COLUMNS)


def _standardize(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return _empty_matches()
    missing = sorted(set(MATCH_COLUMNS) - set(frame.columns))
    if missing:
        raise ValueError(f"latest results missing columns: {missing}")
    standardized = frame[MATCH_COLUMNS].copy()
    if pd.api.types.is_datetime64_any_dtype(standardized["date"]):
        standardized["date"] = pd.to_datetime(standardized["date"], errors="coerce", utc=True).dt.tz_convert(None)
    else:
        standardized["date"] = pd.to_datetime(
            standardized["date"],
            errors="coerce",
            format="mixed",
            utc=True,
        ).dt.tz_convert(None)
    standardized["home_team"] = standardized["home_team"].astype(str).map(normalize_team_name)
    standardized["away_team"] = standardized["away_team"].astype(str).map(normalize_team_name)
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


def _known_teams(config: Config) -> set[str]:
    if not config.data.ratings_csv.exists():
        return set()
    frame = pd.read_csv(config.data.ratings_csv)
    if "team" not in frame.columns:
        return set()
    return {normalize_team_name(str(team)).lower() for team in frame["team"].dropna()}


def _filter_known_team_matches(frame: pd.DataFrame, config: Config) -> pd.DataFrame:
    known = _known_teams(config)
    if frame.empty or not known:
        return frame
    filtered = frame[
        frame["home_team"].astype(str).str.lower().str.strip().isin(known)
        & frame["away_team"].astype(str).str.lower().str.strip().isin(known)
    ]
    return filtered.reset_index(drop=True)


def _api_football_cache_path(config: Config) -> Path:
    return config.data.cache_dir / "api_football_latest.csv"


def _read_api_football_cache(config: Config) -> pd.DataFrame:
    cache_path = _api_football_cache_path(config)
    if not cache_path.exists():
        return _empty_matches()
    return _standardize(pd.read_csv(cache_path))


def _write_api_football_cache(config: Config, frame: pd.DataFrame) -> None:
    if frame.empty:
        return
    config.data.cache_dir.mkdir(parents=True, exist_ok=True)
    frame.to_csv(_api_football_cache_path(config), index=False)


def _api_football_matches(config: Config) -> pd.DataFrame:
    token = os.getenv("API_FOOTBALL_KEY")
    if not token:
        return _empty_matches()

    rows: list[dict[str, Any]] = []
    today = date.today()
    days = max(1, min(config.data.api_football_lookback_days, config.data.latest_lookback_days))
    for offset in range(days):
        match_date = today - timedelta(days=offset)
        response = requests.get(
            API_FOOTBALL_URL,
            headers={"x-apisports-key": token},
            params={"date": match_date.isoformat()},
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        errors = payload.get("errors") or {}
        if errors:
            if "rateLimit" in errors and not rows:
                return _read_api_football_cache(config)
            continue
        for item in payload.get("response", []):
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
    frame = _filter_known_team_matches(_standardize(pd.DataFrame(rows, columns=MATCH_COLUMNS)), config)
    _write_api_football_cache(config, frame)
    return frame


def load_latest_matches(
    config: Config | None = None,
    include_api: bool = True,
) -> pd.DataFrame:
    matches, _ = load_latest_matches_detailed(config, include_api=include_api)
    return matches


def load_latest_matches_detailed(
    config: Config | None = None,
    include_api: bool = True,
) -> tuple[pd.DataFrame, dict[str, object]]:
    load_local_env()
    cfg = config or load_config()
    csv_matches = load_latest_results_csv(cfg.data.latest_results_csv)
    frames = [csv_matches]
    sources: dict[str, object] = {
        "csv_matches": int(len(csv_matches)),
        "football_data_matches": 0,
        "api_football_matches": 0,
        "api_fetch_attempted": include_api,
        "api_errors": [],
    }

    if include_api:
        for loader_name, loader in (
            ("football_data", _football_data_matches),
            ("api_football", _api_football_matches),
        ):
            try:
                frame = loader(cfg)
                if not frame.empty:
                    frames.append(frame)
                if loader_name == "football_data":
                    sources["football_data_matches"] = int(len(frame))
                else:
                    sources["api_football_matches"] = int(len(frame))
            except Exception as exc:
                sources["api_errors"].append(f"{loader_name}: {exc}")
                continue

    combined = pd.concat(frames, ignore_index=True) if frames else _empty_matches()
    matches = _dedupe_matches(_standardize(combined))
    sources["latest_matches_loaded"] = int(len(matches))
    if not matches.empty:
        sources["latest_match_date"] = pd.to_datetime(matches["date"]).max().date().isoformat()
    else:
        sources["latest_match_date"] = None
    return matches, sources


def _dedupe_matches(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return frame
    dedupe = frame.copy()
    dedupe["date_key"] = pd.to_datetime(dedupe["date"]).dt.date.astype(str)
    dedupe["home_key"] = dedupe["home_team"].astype(str).map(lambda team: normalize_team_name(team).lower())
    dedupe["away_key"] = dedupe["away_team"].astype(str).map(lambda team: normalize_team_name(team).lower())
    dedupe = dedupe.drop_duplicates(["date_key", "home_key", "away_key"], keep="last")
    return dedupe.drop(columns=["date_key", "home_key", "away_key"]).sort_values("date").reset_index(drop=True)


def merge_match_frames(base_matches: pd.DataFrame, latest_matches: pd.DataFrame) -> pd.DataFrame:
    if latest_matches.empty:
        return base_matches.sort_values("date").reset_index(drop=True)
    merged = pd.concat([base_matches, latest_matches], ignore_index=True)
    return _dedupe_matches(_standardize(merged))


def latest_data_status(
    config: Config | None = None,
    latest_matches: pd.DataFrame | None = None,
    sources: dict[str, object] | None = None,
) -> dict[str, object]:
    load_local_env()
    cfg = config or load_config()
    latest = latest_matches if latest_matches is not None else load_latest_matches(cfg, include_api=False)
    latest_date = None
    if not latest.empty:
        latest_date = pd.to_datetime(latest["date"]).max().date().isoformat()
    status = {
        "latest_results_csv": str(cfg.data.latest_results_csv),
        "latest_results_csv_exists": cfg.data.latest_results_csv.exists(),
        "latest_matches_loaded": int(len(latest)),
        "latest_match_date": latest_date,
        "football_data_api_configured": bool(os.getenv("FOOTBALL_DATA_API_KEY")),
        "api_football_configured": bool(os.getenv("API_FOOTBALL_KEY")),
        "lookback_days": cfg.data.latest_lookback_days,
        "checked_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
    }
    if sources:
        status.update(sources)
    return status
