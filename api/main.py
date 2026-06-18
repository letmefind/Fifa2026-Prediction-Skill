from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from api.service import get_service, refresh_service


app = FastAPI(title="FIFA World Cup 2026 Prediction Engine", version="1.0.0")
ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web"
app.mount("/static", StaticFiles(directory=WEB_DIR / "static"), name="static")
app.mount("/project-docs", StaticFiles(directory=ROOT / "docs"), name="project-docs")


class MatchRequest(BaseModel):
    team_a: str
    team_b: str
    neutral: bool = True


class SimulateRequest(BaseModel):
    runs: int = Field(default=10000, ge=1, le=250000)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def dashboard() -> str:
    return (WEB_DIR / "index.html").read_text(encoding="utf-8")


@app.get("/teams")
def teams() -> list[str]:
    return get_service().teams


@app.get("/data/latest_status")
def latest_status() -> dict[str, object]:
    return get_service().latest_status()


@app.post("/data/refresh_latest")
def refresh_latest() -> dict[str, object]:
    return refresh_service().latest_status()


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
