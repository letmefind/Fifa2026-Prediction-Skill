from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from config import load_config


def _result_points(home_score: int, away_score: int) -> tuple[float, float]:
    if home_score > away_score:
        return 1.0, 0.0
    if home_score < away_score:
        return 0.0, 1.0
    return 0.5, 0.5


@dataclass
class EloModel:
    base_rating: float | None = None
    k_factor: float | None = None
    home_advantage: float | None = None
    ratings: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        cfg = load_config().model.elo
        self.base_rating = float(self.base_rating if self.base_rating is not None else cfg.base_rating)
        self.k_factor = float(self.k_factor if self.k_factor is not None else cfg.k_factor)
        self.home_advantage = float(
            self.home_advantage if self.home_advantage is not None else cfg.home_advantage
        )

    def get_rating(self, team: str) -> float:
        return self.ratings.get(team, float(self.base_rating))

    def set_rating(self, team: str, rating: float) -> None:
        self.ratings[team] = float(rating)

    def expected_score(self, team_a: str, team_b: str, neutral: bool = True) -> float:
        advantage = 0.0 if neutral else float(self.home_advantage)
        rating_a = self.get_rating(team_a) + advantage
        rating_b = self.get_rating(team_b)
        return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))

    def update_match(
        self,
        home_team: str,
        away_team: str,
        home_score: int,
        away_score: int,
        neutral: bool = True,
    ) -> tuple[float, float]:
        expected_home = self.expected_score(home_team, away_team, neutral=neutral)
        expected_away = 1.0 - expected_home
        actual_home, actual_away = _result_points(home_score, away_score)

        margin = abs(home_score - away_score)
        multiplier = 1.0 if margin <= 1 else (1.0 + margin) ** 0.5
        home_delta = float(self.k_factor) * multiplier * (actual_home - expected_home)
        away_delta = float(self.k_factor) * multiplier * (actual_away - expected_away)

        self.ratings[home_team] = self.get_rating(home_team) + home_delta
        self.ratings[away_team] = self.get_rating(away_team) + away_delta
        return self.ratings[home_team], self.ratings[away_team]

    def fit(self, matches: pd.DataFrame, initial_ratings: pd.DataFrame | None = None) -> "EloModel":
        if initial_ratings is not None and not initial_ratings.empty:
            for row in initial_ratings.itertuples(index=False):
                self.set_rating(str(row.team), float(row.rating))

        for row in matches.sort_values("date").itertuples(index=False):
            self.update_match(
                str(row.home_team),
                str(row.away_team),
                int(row.home_score),
                int(row.away_score),
                neutral=bool(row.neutral),
            )
        return self

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame(
            [{"team": team, "rating": rating} for team, rating in self.ratings.items()]
        ).sort_values("rating", ascending=False, ignore_index=True)
