from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_dashboard_loads() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Prediction Engine Dashboard" in response.text
    assert "Predictions By Date" in response.text
    assert "Multilingual Help" not in response.text
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


def test_predictions_by_date_endpoint() -> None:
    response = client.get("/predictions/date?date=18%20jun&refresh=false")
    assert response.status_code == 200
    body = response.json()
    assert body["date"] == "2026-06-18"
    assert body["match_count"] == 4
    assert len(body["matches"]) == 4


def test_refresh_latest_rebuilds_model() -> None:
    response = client.post("/data/refresh_latest")
    assert response.status_code == 200
    body = response.json()
    assert body["model_rebuilt"] is True
    assert body["api_fetch_attempted"] is True
    assert "total_matches_in_model" in body
    response = client.get("/data/latest_status")
    assert response.status_code == 200
    body = response.json()
    assert "latest_matches_loaded" in body
    assert "total_matches_in_model" in body


def test_multilingual_doc_is_served() -> None:
    response = client.get("/project-docs/README_10_LANGUAGES.md")
    assert response.status_code == 200
    assert "## 1. فارسی" in response.text
    assert "## 10. 中文" in response.text


def test_predict_match_api_for_dashboard() -> None:
    response = client.post(
        "/predict_match",
        json={"team_a": "Brazil", "team_b": "France", "neutral": True},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["team_a"] == "Brazil"
    assert body["team_b"] == "France"
    assert "data_status" in body
    assert "known_result" in body
    assert "prediction_type" in body
    assert abs(body["win_prob_a"] + body["draw_prob"] + body["win_prob_b"] - 1.0) < 1e-9


def test_group_predictions_endpoint() -> None:
    response = client.get("/groups/predictions?refresh=false")
    assert response.status_code == 200
    body = response.json()
    assert "groups" in body
    assert "A" in body["groups"]
    assert body["fixture_status"]["official"] is True
    assert body["fixture_status"]["warning"] is None
    assert len(body["groups"]["A"]["matches"]) == 6
    assert "knockout_projection" in body


def test_group_g_includes_played_iran_new_zealand() -> None:
    response = client.get("/groups/G?refresh=false")
    assert response.status_code == 200
    group = response.json()
    played = [
        match
        for match in group["matches"]
        if match["team_a"] == "Iran" and match["team_b"] == "New Zealand"
    ]
    assert played
    assert played[0]["status"] == "played"
    assert played[0]["score"] == "2-2"
