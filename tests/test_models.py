from __future__ import annotations

import pandas as pd

from data import load_matches, load_team_ratings
from models import AttackDefenseStrengthModel, DixonColesPoissonModel, EloModel
from models.betting import calculate_ev
from models.llm import explain_prediction, generate_llm_prompt


def test_elo_updates_winner_upward() -> None:
    elo = EloModel(k_factor=20, home_advantage=0)
    before = elo.get_rating("Brazil")
    elo.update_match("Brazil", "France", 2, 0)
    assert elo.get_rating("Brazil") > before
    assert elo.get_rating("France") < before


def test_prediction_probabilities_sum_to_one() -> None:
    matches = load_matches()
    ratings = load_team_ratings()
    elo = EloModel().fit(matches, ratings)
    strengths = AttackDefenseStrengthModel().fit(matches)
    model = DixonColesPoissonModel(strengths, elo)

    prediction = model.predict_match("Brazil", "France")
    total = prediction.win_prob_a + prediction.draw_prob + prediction.win_prob_b

    assert abs(total - 1.0) < 1e-9
    assert prediction.expected_goals_a > 0
    assert prediction.expected_goals_b > 0
    assert abs(sum(prediction.score_distribution.values()) - 1.0) < 1e-9


def test_strength_model_shrinks_unknown_to_average() -> None:
    model = AttackDefenseStrengthModel().fit(load_matches())
    unknown = model.get("Atlantis")
    assert unknown.attack == 1.0
    assert unknown.defense == 1.0
    assert unknown.matches == 0


def test_betting_ev_labels_value() -> None:
    edge = calculate_ev(model_prob=0.55, market_odds=2.2)
    assert edge.expected_value > 0
    assert edge.label == "undervalued"


def test_llm_prompt_and_explanation() -> None:
    result = {
        "win_prob_a": 0.46,
        "draw_prob": 0.27,
        "win_prob_b": 0.27,
        "expected_goals_a": 1.5,
        "expected_goals_b": 1.1,
        "score_distribution": {"1-0": 0.13, "1-1": 0.12, "2-1": 0.09},
    }
    prompt = generate_llm_prompt({"team_a": "Brazil", "team_b": "France", "prediction": result}, {})
    explanation = explain_prediction(result)
    assert "Brazil vs France" in prompt
    assert "team A win" in explanation


def test_loaders_return_expected_columns() -> None:
    matches = load_matches()
    ratings = load_team_ratings()
    assert {"home_team", "away_team", "home_score", "away_score"}.issubset(matches.columns)
    assert {"team", "rating"}.issubset(ratings.columns)
    assert isinstance(matches, pd.DataFrame)
