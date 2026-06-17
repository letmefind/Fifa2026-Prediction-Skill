from __future__ import annotations

import os
from io import StringIO
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import pandas as pd
import requests


MATCH_COLUMNS = [
    "date",
    "home_team",
    "away_team",
    "home_score",
    "away_score",
    "home_xg",
    "away_xg",
    "neutral",
    "competition",
]

RATING_COLUMNS = ["team", "rating", "spi", "confederation"]
XG_COLUMNS = ["date", "team", "opponent", "xg_for", "xg_against", "venue"]


class DataAdapter(Protocol):
    def load_matches(self) -> pd.DataFrame:
        ...

    def load_team_ratings(self) -> pd.DataFrame:
        ...

    def load_xg_data(self) -> pd.DataFrame:
        ...


def _read_csv(path: Path, columns: list[str]) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=columns)
    return pd.read_csv(path)


@dataclass(frozen=True)
class CSVAdapter:
    matches_path: Path
    ratings_path: Path
    xg_path: Path

    def load_matches(self) -> pd.DataFrame:
        return _read_csv(self.matches_path, MATCH_COLUMNS)

    def load_team_ratings(self) -> pd.DataFrame:
        return _read_csv(self.ratings_path, RATING_COLUMNS)

    def load_xg_data(self) -> pd.DataFrame:
        return _read_csv(self.xg_path, XG_COLUMNS)


@dataclass(frozen=True)
class FiveThirtyEightSPIAdapter:
    url: str = "https://projects.fivethirtyeight.com/soccer-api/international/spi_global_rankings_intl.csv"
    timeout_seconds: int = 20

    def load_matches(self) -> pd.DataFrame:
        return pd.DataFrame(columns=MATCH_COLUMNS)

    def load_team_ratings(self) -> pd.DataFrame:
        response = requests.get(self.url, timeout=self.timeout_seconds)
        response.raise_for_status()
        frame = pd.read_csv(StringIO(response.text))
        team_col = "name" if "name" in frame.columns else "team"
        spi_col = "spi" if "spi" in frame.columns else "rating"
        ratings = frame[[team_col, spi_col]].rename(columns={team_col: "team", spi_col: "spi"})
        ratings["rating"] = 1200 + ratings["spi"].astype(float) * 8
        ratings["confederation"] = None
        return ratings[RATING_COLUMNS]

    def load_xg_data(self) -> pd.DataFrame:
        return pd.DataFrame(columns=XG_COLUMNS)


@dataclass(frozen=True)
class StatsBombAdapter:
    base_url: str = "https://data.statsbombservices.com/api/v4"
    timeout_seconds: int = 20

    @property
    def api_key(self) -> str | None:
        return os.getenv("STATSBOMB_API_KEY")

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            raise RuntimeError("STATSBOMB_API_KEY is not set")
        return {"Authorization": f"Bearer {self.api_key}"}

    def load_matches(self) -> pd.DataFrame:
        # StatsBomb account scopes vary; this endpoint path works for authenticated exports.
        response = requests.get(
            f"{self.base_url}/matches",
            headers=self._headers(),
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        raw = response.json()
        rows: list[dict[str, object]] = []
        for item in raw:
            rows.append(
                {
                    "date": item.get("match_date"),
                    "home_team": item.get("home_team", {}).get("home_team_name"),
                    "away_team": item.get("away_team", {}).get("away_team_name"),
                    "home_score": item.get("home_score"),
                    "away_score": item.get("away_score"),
                    "home_xg": item.get("home_xg"),
                    "away_xg": item.get("away_xg"),
                    "neutral": True,
                    "competition": item.get("competition", {}).get("competition_name", "StatsBomb"),
                }
            )
        return pd.DataFrame(rows, columns=MATCH_COLUMNS)

    def load_team_ratings(self) -> pd.DataFrame:
        return pd.DataFrame(columns=RATING_COLUMNS)

    def load_xg_data(self) -> pd.DataFrame:
        matches = self.load_matches()
        if matches.empty:
            return pd.DataFrame(columns=XG_COLUMNS)
        home = matches.rename(
            columns={
                "home_team": "team",
                "away_team": "opponent",
                "home_xg": "xg_for",
                "away_xg": "xg_against",
            }
        )[["date", "team", "opponent", "xg_for", "xg_against"]]
        home["venue"] = "home"
        away = matches.rename(
            columns={
                "away_team": "team",
                "home_team": "opponent",
                "away_xg": "xg_for",
                "home_xg": "xg_against",
            }
        )[["date", "team", "opponent", "xg_for", "xg_against"]]
        away["venue"] = "away"
        return pd.concat([home, away], ignore_index=True)[XG_COLUMNS]
