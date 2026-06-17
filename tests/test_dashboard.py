from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_dashboard_loads() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Prediction Engine Dashboard" in response.text
    assert "How To Find Model Probability" in response.text
    assert "35.6% = 0.356" in response.text
    assert "What Are Decimal Odds?" in response.text
    assert "Odds 2.20 implies 45.5%" in response.text


def test_teams_endpoint_returns_teams() -> None:
    response = client.get("/teams")
    assert response.status_code == 200
    teams = response.json()
    assert "Brazil" in teams
    assert "France" in teams


def test_predict_match_api_for_dashboard() -> None:
    response = client.post(
        "/predict_match",
        json={"team_a": "Brazil", "team_b": "France", "neutral": True},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["team_a"] == "Brazil"
    assert body["team_b"] == "France"
    assert abs(body["win_prob_a"] + body["draw_prob"] + body["win_prob_b"] - 1.0) < 1e-9
