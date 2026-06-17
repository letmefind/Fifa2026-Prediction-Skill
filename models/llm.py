from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def _pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def generate_llm_prompt(match_data: Mapping[str, Any], team_stats: Mapping[str, Any]) -> str:
    team_a = str(match_data.get("team_a", "Team A"))
    team_b = str(match_data.get("team_b", "Team B"))
    prediction = match_data.get("prediction", match_data)
    score_distribution = prediction.get("score_distribution", {})
    likely_scores = sorted(score_distribution.items(), key=lambda item: item[1], reverse=True)[:5]
    likely_score_text = ", ".join(f"{score} ({_pct(prob)})" for score, prob in likely_scores)

    return (
        "You are evaluating a FIFA match prediction. Use the quantitative model as the primary "
        "evidence, then add concise football context without overriding probabilities unless there "
        "is strong external evidence.\n\n"
        f"Match: {team_a} vs {team_b}\n"
        f"Win probability {team_a}: {_pct(float(prediction['win_prob_a']))}\n"
        f"Draw probability: {_pct(float(prediction['draw_prob']))}\n"
        f"Win probability {team_b}: {_pct(float(prediction['win_prob_b']))}\n"
        f"Expected goals {team_a}: {float(prediction['expected_goals_a']):.2f}\n"
        f"Expected goals {team_b}: {float(prediction['expected_goals_b']):.2f}\n"
        f"Most likely scores: {likely_score_text}\n\n"
        f"Team stats JSON: {dict(team_stats)}\n\n"
        "Return: 1) baseline prediction, 2) key uncertainty drivers, 3) betting-market caution, "
        "4) final concise recommendation."
    )


def explain_prediction(match_result: Mapping[str, Any]) -> str:
    win_a = float(match_result["win_prob_a"])
    draw = float(match_result["draw_prob"])
    win_b = float(match_result["win_prob_b"])
    eg_a = float(match_result["expected_goals_a"])
    eg_b = float(match_result["expected_goals_b"])
    total = win_a + draw + win_b
    if abs(total - 1.0) > 0.01:
        raise ValueError("match probabilities must sum to approximately 1")

    if win_a > win_b and win_a > draw:
        lean = "team A win"
        margin = win_a - max(win_b, draw)
    elif win_b > win_a and win_b > draw:
        lean = "team B win"
        margin = win_b - max(win_a, draw)
    else:
        lean = "draw"
        margin = draw - max(win_a, win_b)

    confidence = "high" if margin >= 0.20 else "moderate" if margin >= 0.10 else "low"
    return (
        f"The model leans {lean} with {confidence} confidence. Expected goals are "
        f"{eg_a:.2f} to {eg_b:.2f}, and the draw probability is {_pct(draw)}, so low-score "
        "variance remains an important part of the forecast."
    )
