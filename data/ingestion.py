from __future__ import annotations

from pathlib import Path

import pandas as pd

from config import Config, load_config
from data.adapters import (
    CSVAdapter,
    FiveThirtyEightSPIAdapter,
    MATCH_COLUMNS,
    RATING_COLUMNS,
    StatsBombAdapter,
    XG_COLUMNS,
)


def _adapter(config: Config | None = None) -> CSVAdapter:
    cfg = config or load_config()
    return CSVAdapter(cfg.data.matches_csv, cfg.data.ratings_csv, cfg.data.xg_csv)


def _validate_columns(frame: pd.DataFrame, columns: list[str], dataset: str) -> pd.DataFrame:
    missing = sorted(set(columns) - set(frame.columns))
    if missing:
        raise ValueError(f"{dataset} is missing required columns: {missing}")
    return frame[columns].copy()


def load_matches(config: Config | None = None) -> pd.DataFrame:
    frame = _adapter(config).load_matches()
    frame = _validate_columns(frame, MATCH_COLUMNS, "matches")
    if frame.empty:
        return frame
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["home_score"] = frame["home_score"].astype(int)
    frame["away_score"] = frame["away_score"].astype(int)
    frame["neutral"] = frame["neutral"].astype(bool)
    return frame.sort_values("date").reset_index(drop=True)


def load_team_ratings(config: Config | None = None, include_spi: bool = False) -> pd.DataFrame:
    cfg = config or load_config()
    frame = _adapter(cfg).load_team_ratings()
    if include_spi:
        try:
            spi = FiveThirtyEightSPIAdapter().load_team_ratings()
            frame = pd.concat([frame, spi], ignore_index=True)
        except Exception:
            pass
    frame = _validate_columns(frame, RATING_COLUMNS, "team ratings")
    if frame.empty:
        return frame
    frame = frame.dropna(subset=["team"]).copy()
    frame["rating"] = pd.to_numeric(frame["rating"], errors="coerce")
    frame["spi"] = pd.to_numeric(frame["spi"], errors="coerce")
    frame = frame.sort_values("rating", ascending=False).drop_duplicates("team", keep="first")
    return frame.reset_index(drop=True)


def load_xg_data(config: Config | None = None, include_statsbomb: bool = False) -> pd.DataFrame:
    frame = _adapter(config).load_xg_data()
    if include_statsbomb:
        try:
            statsbomb = StatsBombAdapter().load_xg_data()
            frame = pd.concat([frame, statsbomb], ignore_index=True)
        except Exception:
            pass
    frame = _validate_columns(frame, XG_COLUMNS, "xG")
    if frame.empty:
        return frame
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["xg_for"] = pd.to_numeric(frame["xg_for"], errors="coerce")
    frame["xg_against"] = pd.to_numeric(frame["xg_against"], errors="coerce")
    return frame.dropna(subset=["team", "opponent"]).reset_index(drop=True)


def update_dataset(
    source: str = "csv",
    output_dir: str | Path | None = None,
    config: Config | None = None,
) -> dict[str, Path]:
    cfg = config or load_config()
    target = Path(output_dir) if output_dir else cfg.data.cache_dir
    target.mkdir(parents=True, exist_ok=True)

    if source == "csv":
        adapter = _adapter(cfg)
    elif source == "spi":
        adapter = FiveThirtyEightSPIAdapter()
    elif source == "statsbomb":
        adapter = StatsBombAdapter()
    else:
        raise ValueError("source must be one of: csv, spi, statsbomb")

    outputs = {
        "matches": target / "matches.csv",
        "ratings": target / "team_ratings.csv",
        "xg": target / "xg.csv",
    }
    adapter.load_matches().to_csv(outputs["matches"], index=False)
    adapter.load_team_ratings().to_csv(outputs["ratings"], index=False)
    adapter.load_xg_data().to_csv(outputs["xg"], index=False)
    return outputs
