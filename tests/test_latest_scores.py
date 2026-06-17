from __future__ import annotations

import pandas as pd

from config import load_config
from data.latest_scores import latest_data_status, load_latest_matches, merge_match_frames


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


def test_latest_data_status_shape() -> None:
    status = latest_data_status(load_config())
    assert "latest_matches_loaded" in status
    assert "football_data_api_configured" in status
    assert "api_football_configured" in status
