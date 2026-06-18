from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Iterable

import numpy as np
import pandas as pd

from config import load_config
from models.goal_model import DixonColesPoissonModel, MatchPrediction


@dataclass
class Standing:
    team: str
    points: int = 0
    played: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    goals_for: int = 0
    goals_against: int = 0
    rating: float = 1500.0

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against

    def record(self, goals_for: int, goals_against: int) -> None:
        self.played += 1
        self.goals_for += goals_for
        self.goals_against += goals_against
        if goals_for > goals_against:
            self.points += 3
            self.wins += 1
        elif goals_for < goals_against:
            self.losses += 1
        else:
            self.points += 1
            self.draws += 1


@dataclass
class TournamentRun:
    champion: str
    runner_up: str
    semifinalists: list[str]
    finalists: list[str]
    round_of_32: list[str]
    group_standings: dict[str, list[Standing]] = field(default_factory=dict)


def groups_from_fixtures(fixtures: pd.DataFrame) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for group_name, group_frame in fixtures.groupby("group", sort=True):
        teams = sorted(set(group_frame["team_a"]).union(set(group_frame["team_b"])))
        groups[str(group_name)] = teams
    return groups


class TournamentSimulator:
    def __init__(
        self,
        goal_model: DixonColesPoissonModel,
        teams: Iterable[str],
        ratings: dict[str, float] | None = None,
        seed: int | None = None,
        groups: dict[str, list[str]] | None = None,
    ) -> None:
        self.goal_model = goal_model
        self.teams = list(dict.fromkeys(teams))
        if len(self.teams) < 48:
            raise ValueError("Tournament simulation requires at least 48 unique teams")
        self.teams = self.teams[:48]
        self.ratings = ratings or {}
        self.groups = groups
        cfg = load_config().simulation
        self.rng = np.random.default_rng(seed if seed is not None else cfg.random_seed)

    def make_groups(self) -> dict[str, list[str]]:
        if self.groups:
            return self.groups
        sorted_teams = sorted(self.teams, key=lambda team: self.ratings.get(team, 1500), reverse=True)
        groups = {chr(ord("A") + idx): [] for idx in range(12)}
        for idx, team in enumerate(sorted_teams):
            group_idx = idx % 12 if (idx // 12) % 2 == 0 else 11 - (idx % 12)
            groups[chr(ord("A") + group_idx)].append(team)
        return groups

    def _sample_score(self, prediction: MatchPrediction) -> tuple[int, int]:
        scores = list(prediction.score_distribution.keys())
        probabilities = np.array(list(prediction.score_distribution.values()), dtype=float)
        probabilities /= probabilities.sum()
        selected = str(self.rng.choice(scores, p=probabilities))
        a, b = selected.split("-")
        return int(a), int(b)

    def _simulate_match(self, team_a: str, team_b: str, neutral: bool = True) -> tuple[int, int]:
        prediction = self.goal_model.predict_match(team_a, team_b, neutral=neutral)
        return self._sample_score(prediction)

    @staticmethod
    def _sort_standings(standings: dict[str, Standing]) -> list[Standing]:
        return sorted(
            standings.values(),
            key=lambda row: (
                row.points,
                row.goal_difference,
                row.goals_for,
                row.rating,
                row.team,
            ),
            reverse=True,
        )

    def _simulate_group(self, group: list[str]) -> list[Standing]:
        standings = {
            team: Standing(team=team, rating=self.ratings.get(team, 1500.0))
            for team in group
        }
        for idx, team_a in enumerate(group):
            for team_b in group[idx + 1 :]:
                goals_a, goals_b = self._simulate_match(team_a, team_b, neutral=True)
                standings[team_a].record(goals_a, goals_b)
                standings[team_b].record(goals_b, goals_a)
        return self._sort_standings(standings)

    @staticmethod
    def _best_third_place(third_place: list[Standing]) -> list[Standing]:
        return sorted(
            third_place,
            key=lambda row: (row.points, row.goal_difference, row.goals_for, row.rating, row.team),
            reverse=True,
        )[:8]

    def _knockout_winner(self, team_a: str, team_b: str) -> str:
        goals_a, goals_b = self._simulate_match(team_a, team_b, neutral=True)
        if goals_a > goals_b:
            return team_a
        if goals_b > goals_a:
            return team_b

        prediction = self.goal_model.predict_match(team_a, team_b, neutral=True)
        win_prob = prediction.win_prob_a / max(prediction.win_prob_a + prediction.win_prob_b, 1e-9)
        return team_a if self.rng.random() < win_prob else team_b

    def _play_round(self, teams: list[str]) -> list[str]:
        winners: list[str] = []
        for idx in range(0, len(teams), 2):
            winners.append(self._knockout_winner(teams[idx], teams[idx + 1]))
        return winners

    def simulate_once(self) -> TournamentRun:
        groups = self.make_groups()
        standings = {name: self._simulate_group(group) for name, group in groups.items()}

        winners = [rows[0].team for rows in standings.values()]
        runners_up = [rows[1].team for rows in standings.values()]
        thirds = self._best_third_place([rows[2] for rows in standings.values()])
        round_of_32 = winners + runners_up + [row.team for row in thirds]

        seeded = sorted(round_of_32, key=lambda team: self.ratings.get(team, 1500), reverse=True)
        bracket: list[str] = []
        for idx in range(16):
            bracket.extend([seeded[idx], seeded[-(idx + 1)]])

        round_of_16 = self._play_round(bracket)
        quarterfinalists = self._play_round(round_of_16)
        semifinalists = self._play_round(quarterfinalists)
        finalists = self._play_round(semifinalists)
        champion = self._knockout_winner(finalists[0], finalists[1])
        runner_up = finalists[1] if champion == finalists[0] else finalists[0]
        return TournamentRun(
            champion=champion,
            runner_up=runner_up,
            semifinalists=semifinalists,
            finalists=finalists,
            round_of_32=round_of_32,
            group_standings=standings,
        )

    def simulate_tournament(self, n: int = 10000) -> dict[str, object]:
        counters: dict[str, Counter[str]] = {
            "round_of_32": Counter(),
            "reach_semis": Counter(),
            "reach_final": Counter(),
            "win_world_cup": Counter(),
        }
        latest_group_standings: dict[str, list[dict[str, object]]] = {}

        for _ in range(n):
            run = self.simulate_once()
            counters["round_of_32"].update(run.round_of_32)
            counters["reach_semis"].update(run.semifinalists)
            counters["reach_final"].update(run.finalists)
            counters["win_world_cup"].update([run.champion])
            latest_group_standings = {
                group: [standing.__dict__ | {"goal_difference": standing.goal_difference} for standing in rows]
                for group, rows in run.group_standings.items()
            }

        probabilities: dict[str, dict[str, float | str]] = defaultdict(dict)
        for team in self.teams:
            probabilities[team]["team"] = team
            for key, counter in counters.items():
                probabilities[team][key] = counter[team] / n

        table = sorted(
            probabilities.values(),
            key=lambda row: float(row["win_world_cup"]),
            reverse=True,
        )
        return {
            "runs": n,
            "probabilities": table,
            "group_standings_last_run": latest_group_standings,
        }

    def probabilities_frame(self, n: int = 10000) -> pd.DataFrame:
        result = self.simulate_tournament(n=n)
        return pd.DataFrame(result["probabilities"])
