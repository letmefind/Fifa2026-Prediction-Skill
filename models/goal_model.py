from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.stats import poisson

from config import load_config
from models.elo import EloModel
from models.strength import AttackDefenseStrengthModel


@dataclass(frozen=True)
class MatchPrediction:
    win_prob_a: float
    draw_prob: float
    win_prob_b: float
    expected_goals_a: float
    expected_goals_b: float
    score_distribution: dict[str, float]

    def as_dict(self) -> dict[str, object]:
        return {
            "win_prob_a": self.win_prob_a,
            "draw_prob": self.draw_prob,
            "win_prob_b": self.win_prob_b,
            "expected_goals_a": self.expected_goals_a,
            "expected_goals_b": self.expected_goals_b,
            "score_distribution": self.score_distribution,
        }


class DixonColesPoissonModel:
    def __init__(
        self,
        strengths: AttackDefenseStrengthModel,
        elo: EloModel | None = None,
        base_goals: float | None = None,
        max_goals: int | None = None,
        rho: float | None = None,
        home_advantage_multiplier: float | None = None,
    ) -> None:
        cfg = load_config().model.poisson
        self.strengths = strengths
        self.elo = elo
        self.base_goals = float(base_goals if base_goals is not None else cfg.base_goals_per_team)
        self.max_goals = int(max_goals if max_goals is not None else cfg.max_goals)
        self.rho = float(rho if rho is not None else cfg.dixon_coles_rho)
        self.home_advantage_multiplier = float(
            home_advantage_multiplier
            if home_advantage_multiplier is not None
            else cfg.home_advantage_multiplier
        )

    @staticmethod
    def _elo_multiplier(elo: EloModel | None, team_a: str, team_b: str, neutral: bool) -> tuple[float, float]:
        if elo is None:
            return 1.0, 1.0
        expected = elo.expected_score(team_a, team_b, neutral=neutral)
        # Keep the ELO adjustment conservative; team strengths carry most of the signal.
        a = np.exp((expected - 0.5) * 0.55)
        b = np.exp(((1.0 - expected) - 0.5) * 0.55)
        return float(a), float(b)

    def expected_goals(self, team_a: str, team_b: str, neutral: bool = True) -> tuple[float, float]:
        a = self.strengths.get(team_a)
        b = self.strengths.get(team_b)
        elo_a, elo_b = self._elo_multiplier(self.elo, team_a, team_b, neutral=neutral)
        home_mult = 1.0 if neutral else self.home_advantage_multiplier
        lambda_a = self.base_goals * a.attack * b.defense * elo_a * home_mult
        lambda_b = self.base_goals * b.attack * a.defense * elo_b
        return float(np.clip(lambda_a, 0.15, 5.5)), float(np.clip(lambda_b, 0.15, 5.5))

    def _dc_tau(self, home_goals: np.ndarray, away_goals: np.ndarray, lambda_a: float, lambda_b: float) -> np.ndarray:
        tau = np.ones_like(home_goals, dtype=float)
        tau[(home_goals == 0) & (away_goals == 0)] = 1.0 - lambda_a * lambda_b * self.rho
        tau[(home_goals == 0) & (away_goals == 1)] = 1.0 + lambda_a * self.rho
        tau[(home_goals == 1) & (away_goals == 0)] = 1.0 + lambda_b * self.rho
        tau[(home_goals == 1) & (away_goals == 1)] = 1.0 - self.rho
        return np.clip(tau, 0.01, 2.0)

    def predict_match(self, team_a: str, team_b: str, neutral: bool = True) -> MatchPrediction:
        lambda_a, lambda_b = self.expected_goals(team_a, team_b, neutral=neutral)
        goals = np.arange(self.max_goals + 1)
        probs_a = poisson.pmf(goals, lambda_a)
        probs_b = poisson.pmf(goals, lambda_b)
        matrix = np.outer(probs_a, probs_b)
        home_grid, away_grid = np.meshgrid(goals, goals, indexing="ij")
        matrix *= self._dc_tau(home_grid, away_grid, lambda_a, lambda_b)
        matrix /= matrix.sum()

        win_a = float(np.tril(matrix, k=-1).sum())
        draw = float(np.trace(matrix))
        win_b = float(np.triu(matrix, k=1).sum())
        distribution = {
            f"{i}-{j}": float(matrix[i, j])
            for i in range(self.max_goals + 1)
            for j in range(self.max_goals + 1)
        }
        return MatchPrediction(
            win_prob_a=win_a,
            draw_prob=draw,
            win_prob_b=win_b,
            expected_goals_a=lambda_a,
            expected_goals_b=lambda_b,
            score_distribution=distribution,
        )
