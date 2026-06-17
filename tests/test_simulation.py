from __future__ import annotations

from api.service import PredictionService


def test_tournament_simulation_returns_48_probability_rows() -> None:
    service = PredictionService()
    result = service.simulate_tournament(n=5)

    assert result["runs"] == 5
    assert len(result["probabilities"]) == 48
    champion_prob_sum = sum(float(row["win_world_cup"]) for row in result["probabilities"])
    assert abs(champion_prob_sum - 1.0) < 1e-9


def test_team_profile_has_model_fields() -> None:
    profile = PredictionService().team_profile("Brazil")
    assert profile["team"] == "Brazil"
    assert profile["elo_rating"] > 1000
    assert profile["attack_strength"] > 0
    assert profile["defense_strength"] > 0
