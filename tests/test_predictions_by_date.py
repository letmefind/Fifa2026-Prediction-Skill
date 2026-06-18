from __future__ import annotations

import pytest

from api.service import PredictionService
from simulation.group_predictions import load_group_fixtures, parse_match_date, predict_matches_by_date


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("18 jun", "2026-06-18"),
        ("June 18", "2026-06-18"),
        ("2026-06-18", "2026-06-18"),
        ("18 Jun 2026", "2026-06-18"),
    ],
)
def test_parse_match_date_accepts_flexible_input(value: str, expected: str) -> None:
    assert parse_match_date(value) == expected


def test_predictions_by_date_returns_june_18_fixtures() -> None:
    service = PredictionService()
    result = service.predictions_by_date("18 jun")
    assert result["date"] == "2026-06-18"
    assert result["match_count"] == 4
    pairs = {(match["team_a"], match["team_b"]) for match in result["matches"]}
    assert ("Czechia", "South Africa") in pairs
    assert ("Canada", "Qatar") in pairs


def test_predictions_by_date_shape() -> None:
    fixtures = load_group_fixtures()
    service = PredictionService()
    result = predict_matches_by_date(
        service.goal_model,
        service.latest_matches,
        "2026-06-18",
        fixtures=fixtures,
    )
    assert len(result["matches"]) == len(fixtures[fixtures["date"].dt.date.astype(str) == "2026-06-18"])
