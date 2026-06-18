from __future__ import annotations

import os

import pandas as pd

from api.service import PredictionService
from config import load_config
from data.latest_scores import latest_data_status, load_latest_matches, load_local_env, merge_match_frames


def test_latest_results_template_loads() -> None:
    latest = load_latest_matches(load_config(), include_api=False)
    assert {"home_team", "away_team", "home_score", "away_score"}.issubset(latest.columns)
    assert isinstance(latest, pd.DataFrame)


def test_merge_latest_matches_dedupes() -> None:
    base = pd.DataFrame(
        [
            {
                "date": "2026-01-01",
                "home_team": "Brazil",
                "away_team": "France",
                "home_score": 1,
                "away_score": 0,
                "home_xg": None,
                "away_xg": None,
                "neutral": True,
                "competition": "Old",
            }
        ]
    )
    latest = base.copy()
    latest["home_score"] = 2
    latest["competition"] = "Latest"
    merged = merge_match_frames(base, latest)

    assert len(merged) == 1
    assert int(merged.iloc[0]["home_score"]) == 2
    assert merged.iloc[0]["competition"] == "Latest"


def test_merge_preserves_utc_latest_results() -> None:
    base = pd.DataFrame(
        [
            {
                "date": "2024-03-21",
                "home_team": "Brazil",
                "away_team": "France",
                "home_score": 1,
                "away_score": 0,
                "home_xg": None,
                "away_xg": None,
                "neutral": True,
                "competition": "Friendly",
            }
        ]
    )
    latest = pd.DataFrame(
        [
            {
                "date": "2026-06-16 01:00:00+00:00",
                "home_team": "Iran",
                "away_team": "New Zealand",
                "home_score": 2,
                "away_score": 2,
                "home_xg": None,
                "away_xg": None,
                "neutral": True,
                "competition": "World Cup 2026",
            }
        ]
    )
    merged = merge_match_frames(base, latest)

    assert len(merged) == 2
    iran = merged[merged["home_team"] == "Iran"]
    assert len(iran) == 1
    assert int(iran.iloc[0]["away_score"]) == 2


def test_latest_data_status_shape() -> None:
    status = latest_data_status(load_config())
    assert "latest_matches_loaded" in status
    assert "football_data_api_configured" in status
    assert "api_football_configured" in status


def test_load_local_env_does_not_require_real_secret(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("API_FOOTBALL_KEY", raising=False)
    env_path = tmp_path / ".env"
    env_path.write_text("API_FOOTBALL_KEY=placeholder\n", encoding="utf-8")

    load_local_env(env_path)

    assert os.environ["API_FOOTBALL_KEY"] == "placeholder"


def test_known_latest_result_detects_already_played_match() -> None:
    service = PredictionService.__new__(PredictionService)
    service.latest_matches = pd.DataFrame(
        [
            {
                "date": "2026-06-16",
                "home_team": "Iran",
                "away_team": "New Zealand",
                "home_score": 2,
                "away_score": 2,
                "home_xg": None,
                "away_xg": None,
                "neutral": True,
                "competition": "World Cup",
            }
        ]
    )

    result = service.known_latest_result("New Zealand", "Iran")

    assert result["found"] is True
    assert result["home_team"] == "Iran"
    assert result["away_team"] == "New Zealand"
    assert result["home_score"] == 2
    assert result["away_score"] == 2
