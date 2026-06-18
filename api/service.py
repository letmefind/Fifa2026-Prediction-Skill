from __future__ import annotations

import pandas as pd

from config import Config, load_config
from data import latest_data_status, load_latest_matches, load_latest_matches_detailed, load_matches, load_team_ratings, merge_match_frames
from data.team_aliases import fixture_pair_key, normalize_team_name
from models import AttackDefenseStrengthModel, DixonColesPoissonModel, EloModel
from simulation import TournamentSimulator, groups_from_fixtures, load_group_fixtures, predict_group_stage
from simulation.group_predictions import parse_match_date, predict_matches_by_date


_service_instance: PredictionService | None = None


class PredictionService:
    def __init__(self, config: Config | None = None, fetch_latest: bool = False) -> None:
        self.config = config or load_config()
        self.latest_sources: dict[str, object] = {}
        self.base_matches = load_matches(self.config, include_latest=False)
        if fetch_latest:
            self.latest_matches, self.latest_sources = load_latest_matches_detailed(
                self.config,
                include_api=True,
            )
        else:
            self.latest_matches = load_latest_matches(self.config, include_api=True)
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

    @staticmethod
    def _norm_team(team: str) -> str:
        return normalize_team_name(team).lower()

    def known_latest_result(self, team_a: str, team_b: str) -> dict[str, object]:
        if self.latest_matches.empty:
            return {"found": False}

        target = fixture_pair_key(team_a, team_b)
        pair_keys = self.latest_matches.apply(
            lambda row: fixture_pair_key(str(row["home_team"]), str(row["away_team"])),
            axis=1,
        )
        matches = self.latest_matches[pair_keys == target]
        if matches.empty:
            return {"found": False}

        row = matches.sort_values("date").iloc[-1]
        home_team = normalize_team_name(str(row["home_team"]))
        away_team = normalize_team_name(str(row["away_team"]))
        return {
            "found": True,
            "date": pd.to_datetime(row["date"]).date().isoformat(),
            "home_team": home_team,
            "away_team": away_team,
            "home_score": int(row["home_score"]),
            "away_score": int(row["away_score"]),
            "competition": str(row["competition"]),
            "source": "latest_results",
            "message": "This match already appears in latest results. The probabilities below are for a future rematch forecast.",
        }

    def predict_match(self, team_a: str, team_b: str, neutral: bool = True) -> dict[str, object]:
        prediction = self.goal_model.predict_match(team_a, team_b, neutral=neutral).as_dict()
        prediction["team_a"] = team_a
        prediction["team_b"] = team_b
        prediction["data_status"] = self.latest_status()
        prediction["known_result"] = self.known_latest_result(team_a, team_b)
        prediction["prediction_type"] = (
            "rematch_forecast" if prediction["known_result"]["found"] else "future_forecast"
        )
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
        fixtures = load_group_fixtures(self.config)
        official_groups = groups_from_fixtures(fixtures)
        simulator = TournamentSimulator(
            goal_model=self.goal_model,
            teams=sorted({team for group in official_groups.values() for team in group}),
            ratings=self.ratings_map(),
            seed=self.config.simulation.random_seed,
            groups=official_groups,
        )
        return simulator.simulate_tournament(runs)

    def tournament_probabilities(self, n: int | None = None) -> pd.DataFrame:
        result = self.simulate_tournament(n)
        return pd.DataFrame(result["probabilities"])

    def group_stage_predictions(self) -> dict[str, object]:
        fixtures = load_group_fixtures(self.config)
        return predict_group_stage(
            goal_model=self.goal_model,
            latest_matches=self.latest_matches,
            ratings=self.ratings_map(),
            fixtures=fixtures,
            config=self.config,
        )

    def group_prediction(self, group: str) -> dict[str, object]:
        predictions = self.group_stage_predictions()
        group_key = group.upper().replace("GROUP ", "").strip()
        groups = predictions["groups"]
        if group_key not in groups:
            raise ValueError(f"Unknown group: {group}")
        return groups[group_key]

    def predictions_by_date(self, date_value: str) -> dict[str, object]:
        fixtures = load_group_fixtures(self.config)
        return predict_matches_by_date(
            goal_model=self.goal_model,
            latest_matches=self.latest_matches,
            date_value=date_value,
            fixtures=fixtures,
            config=self.config,
        )

    def latest_status(self) -> dict[str, object]:
        status = latest_data_status(self.config, self.latest_matches, self.latest_sources or None)
        status["base_matches_loaded"] = int(len(self.base_matches))
        status["total_matches_in_model"] = int(len(self.matches))
        status["model_rebuilt"] = bool(self.latest_sources)
        return status


def get_service() -> PredictionService:
    global _service_instance
    if _service_instance is None:
        _service_instance = PredictionService()
    return _service_instance


def refresh_service() -> PredictionService:
    global _service_instance
    _service_instance = PredictionService(fetch_latest=True)
    return _service_instance
