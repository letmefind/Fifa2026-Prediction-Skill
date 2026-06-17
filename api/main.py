from __future__ import annotations

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

from api.service import get_service


app = FastAPI(title="FIFA World Cup 2026 Prediction Engine", version="1.0.0")


class MatchRequest(BaseModel):
    team_a: str
    team_b: str
    neutral: bool = True


class SimulateRequest(BaseModel):
    runs: int = Field(default=10000, ge=1, le=250000)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict_match")
def predict_match(request: MatchRequest) -> dict[str, object]:
    return get_service().predict_match(request.team_a, request.team_b, neutral=request.neutral)


@app.post("/simulate")
def simulate(request: SimulateRequest) -> dict[str, object]:
    return get_service().simulate_tournament(n=request.runs)


@app.get("/team/{name}")
def team(name: str) -> dict[str, object]:
    return get_service().team_profile(name)


@app.get("/tournament/probabilities")
def tournament_probabilities(runs: int = Query(default=10000, ge=1, le=250000)) -> list[dict[str, object]]:
    return get_service().simulate_tournament(n=runs)["probabilities"]
