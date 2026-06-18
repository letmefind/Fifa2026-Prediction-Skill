from __future__ import annotations

from api.service import PredictionService
from simulation.group_predictions import load_group_fixtures


def test_tournament_simulation_uses_official_groups() -> None:
    from simulation.tournament import groups_from_fixtures

    fixtures = load_group_fixtures()
    official = groups_from_fixtures(fixtures)
    service = PredictionService()
    simulator_groups = service.simulate_tournament(n=1)["group_standings_last_run"]
    assert set(simulator_groups.keys()) == set(official.keys())
    for group_name, teams in official.items():
        assert {row["team"] for row in simulator_groups[group_name]} == set(teams)


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


def test_group_fixtures_have_12_groups_and_72_matches() -> None:
    fixtures = load_group_fixtures()
    assert fixtures["group"].nunique() == 12
    assert len(fixtures) == 72


def test_official_groups_place_iran_and_spain_separately() -> None:
    fixtures = load_group_fixtures()
    group_g = set(fixtures.loc[fixtures["group"] == "G", "team_a"]).union(
        fixtures.loc[fixtures["group"] == "G", "team_b"]
    )
    group_h = set(fixtures.loc[fixtures["group"] == "H", "team_a"]).union(
        fixtures.loc[fixtures["group"] == "H", "team_b"]
    )
    assert "Iran" in group_g
    assert "Spain" in group_h
    assert "Spain" not in group_g
    assert "Iran" not in group_h


def test_group_stage_predictions_use_official_fixtures() -> None:
    result = PredictionService().group_stage_predictions()
    assert result["fixture_status"]["official"] is True
    assert result["fixture_status"]["warning"] is None


def test_predicted_group_scores_follow_most_likely_outcome() -> None:
    from simulation.group_predictions import _top_score

    prediction = {
        "win_prob_a": 0.58,
        "draw_prob": 0.24,
        "win_prob_b": 0.18,
        "score_distribution": {
            "1-1": 0.116,
            "1-0": 0.109,
            "2-0": 0.108,
            "2-1": 0.098,
            "0-0": 0.073,
        },
    }
    goals_a, goals_b, score, _ = _top_score(prediction)
    assert goals_a > goals_b
    assert score != "1-1"


def test_group_predictions_are_not_mostly_displayed_draws() -> None:
    result = PredictionService().group_stage_predictions()
    predicted = [
        match
        for group in result["groups"].values()
        for match in group["matches"]
        if match["status"] == "predicted"
    ]
    draw_count = sum(1 for match in predicted if match["winner"] == "Draw")
    assert draw_count / len(predicted) < 0.5


def test_group_stage_predictions_project_round_of_32() -> None:
    result = PredictionService().group_stage_predictions()
    assert len(result["groups"]) == 12
    assert len(result["qualified_round_of_32"]) == 32
    assert result["knockout_projection"]["champion"]
