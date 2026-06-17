from __future__ import annotations

from functools import lru_cache

import pandas as pd

from config import Config, load_config
from data import latest_data_status, load_latest_matches, load_matches, load_team_ratings, merge_match_frames
from models import AttackDefenseStrengthModel, DixonColesPoissonModel, EloModel
from simulation import TournamentSimulator


class PredictionService:
    def __init__(self, config: Config | None = None) -> None:
        self.config = config or load_config()
        self.base_matches = load_matches(self.config, include_latest=False)
        self.latest_matches = load_latest_matches(self.config)
        self.matches = merge_match_frames(self.base_matches, self.latest_matches)
        self.initial_ratings = load_team_ratings(self.config)
        self.elo = EloModel().fit(self.matches, self.initial_ratings)
        self.strengths = AttackDefenseStrengthModel().fit(self.matches)
        self.goal_model = DixonColesPoissonModel(self.strengths, self.elo)

    @property
    def teams(self) -> list[str]:
        from_matches = set(self.matches["home_team"]).union(set(self.matches["away_team"]))
        from_ratings = set(self.initial_ratings["team"]) if not self.initial_ratings.empty else set()
        teams = sorted(from_matches.union(from_ratings), key=lambda team: self.rating_for(team), reverse=True)
        return list(teams)

    def rating_for(self, team: str) -> float:
        return self.elo.get_rating(team)

    def ratings_map(self) -> dict[str, float]:
        return {team: self.rating_for(team) for team in self.teams}

    def predict_match(self, team_a: str, team_b: str, neutral: bool = True) -> dict[str, object]:
        prediction = self.goal_model.predict_match(team_a, team_b, neutral=neutral).as_dict()
        prediction["team_a"] = team_a
        prediction["team_b"] = team_b
        prediction["data_status"] = self.latest_status()
        return prediction

    def team_profile(self, name: str) -> dict[str, object]:
        strength = self.strengths.get(name)
        recent = self.matches[
            (self.matches["home_team"] == name) | (self.matches["away_team"] == name)
        ].tail(10)
        return {
            "team": name,
            "elo_rating": self.rating_for(name),
            "attack_strength": strength.attack,
            "defense_strength": strength.defense,
            "matches_in_model": strength.matches,
            "recent_matches": recent.to_dict(orient="records"),
        }

    def simulate_tournament(self, n: int | None = None) -> dict[str, object]:
        runs = int(n or self.config.simulation.default_runs)
        simulator = TournamentSimulator(
            goal_model=self.goal_model,
            teams=self.teams[:48],
            ratings=self.ratings_map(),
            seed=self.config.simulation.random_seed,
        )
        return simulator.simulate_tournament(runs)

    def tournament_probabilities(self, n: int | None = None) -> pd.DataFrame:
        result = self.simulate_tournament(n)
        return pd.DataFrame(result["probabilities"])

    def latest_status(self) -> dict[str, object]:
        status = latest_data_status(self.config, self.latest_matches)
        status["base_matches_loaded"] = int(len(self.base_matches))
        status["total_matches_in_model"] = int(len(self.matches))
        return status


@lru_cache(maxsize=1)
def get_service() -> PredictionService:
    return PredictionService()


def refresh_service() -> PredictionService:
    get_service.cache_clear()
    return get_service()
