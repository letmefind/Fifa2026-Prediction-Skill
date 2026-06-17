from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field


class MatchRecord(BaseModel):
    date: date
    home_team: str
    away_team: str
    home_score: int = Field(ge=0)
    away_score: int = Field(ge=0)
    home_xg: float | None = Field(default=None, ge=0)
    away_xg: float | None = Field(default=None, ge=0)
    neutral: bool = True
    competition: str = "International"


class TeamRating(BaseModel):
    team: str
    rating: float
    spi: float | None = None
    confederation: str | None = None


class XGRecord(BaseModel):
    date: date
    team: str
    opponent: str
    xg_for: float = Field(ge=0)
    xg_against: float = Field(ge=0)
    venue: str = "neutral"
