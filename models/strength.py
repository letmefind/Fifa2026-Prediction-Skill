from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from config import load_config


@dataclass(frozen=True)
class TeamStrength:
    team: str
    attack: float
    defense: float
    matches: int
    goals_for_per_match: float
    goals_against_per_match: float


class AttackDefenseStrengthModel:
    def __init__(
        self,
        goals_weight: float | None = None,
        xg_weight: float | None = None,
        shrinkage_matches: int | None = None,
    ) -> None:
        cfg = load_config().model.strengths
        self.goals_weight = float(goals_weight if goals_weight is not None else cfg.goals_weight)
        self.xg_weight = float(xg_weight if xg_weight is not None else cfg.xg_weight)
        total = self.goals_weight + self.xg_weight
        self.goals_weight /= total
        self.xg_weight /= total
        self.shrinkage_matches = int(
            shrinkage_matches if shrinkage_matches is not None else cfg.shrinkage_matches
        )
        self.strengths: dict[str, TeamStrength] = {}
        self.global_goals_for = 1.35
        self.global_goals_against = 1.35

    @staticmethod
    def _team_rows(matches: pd.DataFrame) -> pd.DataFrame:
        home = pd.DataFrame(
            {
                "team": matches["home_team"],
                "opponent": matches["away_team"],
                "goals_for": matches["home_score"],
                "goals_against": matches["away_score"],
                "xg_for": matches["home_xg"],
                "xg_against": matches["away_xg"],
            }
        )
        away = pd.DataFrame(
            {
                "team": matches["away_team"],
                "opponent": matches["home_team"],
                "goals_for": matches["away_score"],
                "goals_against": matches["home_score"],
                "xg_for": matches["away_xg"],
                "xg_against": matches["home_xg"],
            }
        )
        return pd.concat([home, away], ignore_index=True)

    def fit(self, matches: pd.DataFrame) -> "AttackDefenseStrengthModel":
        if matches.empty:
            return self

        rows = self._team_rows(matches)
        rows["xg_for"] = pd.to_numeric(rows["xg_for"], errors="coerce").fillna(rows["goals_for"])
        rows["xg_against"] = pd.to_numeric(rows["xg_against"], errors="coerce").fillna(
            rows["goals_against"]
        )
        rows["attack_signal"] = self.goals_weight * rows["goals_for"] + self.xg_weight * rows["xg_for"]
        rows["defense_signal"] = (
            self.goals_weight * rows["goals_against"] + self.xg_weight * rows["xg_against"]
        )

        self.global_goals_for = float(rows["attack_signal"].mean())
        self.global_goals_against = float(rows["defense_signal"].mean())

        grouped = rows.groupby("team", as_index=False).agg(
            matches=("team", "size"),
            attack_signal=("attack_signal", "mean"),
            defense_signal=("defense_signal", "mean"),
            goals_for_per_match=("goals_for", "mean"),
            goals_against_per_match=("goals_against", "mean"),
        )

        strengths: dict[str, TeamStrength] = {}
        for row in grouped.itertuples(index=False):
            weight = float(row.matches) / float(row.matches + self.shrinkage_matches)
            attack_rate = weight * float(row.attack_signal) + (1 - weight) * self.global_goals_for
            defense_rate = weight * float(row.defense_signal) + (1 - weight) * self.global_goals_against
            attack = attack_rate / max(self.global_goals_for, 1e-9)
            defense = defense_rate / max(self.global_goals_against, 1e-9)
            strengths[str(row.team)] = TeamStrength(
                team=str(row.team),
                attack=float(np.clip(attack, 0.35, 2.75)),
                defense=float(np.clip(defense, 0.35, 2.75)),
                matches=int(row.matches),
                goals_for_per_match=float(row.goals_for_per_match),
                goals_against_per_match=float(row.goals_against_per_match),
            )
        self.strengths = strengths
        return self

    def get(self, team: str) -> TeamStrength:
        return self.strengths.get(
            team,
            TeamStrength(
                team=team,
                attack=1.0,
                defense=1.0,
                matches=0,
                goals_for_per_match=self.global_goals_for,
                goals_against_per_match=self.global_goals_against,
            ),
        )

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame([strength.__dict__ for strength in self.strengths.values()]).sort_values(
            "attack", ascending=False, ignore_index=True
        )
