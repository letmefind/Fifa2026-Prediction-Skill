from __future__ import annotations

from dataclasses import asdict

import pandas as pd

from config import Config, load_config
from models.goal_model import DixonColesPoissonModel
from simulation.tournament import Standing


GROUP_COLUMNS = ["group", "date", "team_a", "team_b", "neutral"]


def load_group_fixtures(config: Config | None = None) -> pd.DataFrame:
    cfg = config or load_config()
    frame = pd.read_csv(cfg.data.group_fixtures_csv)
    missing = sorted(set(GROUP_COLUMNS) - set(frame.columns))
    if missing:
        raise ValueError(f"group fixtures missing columns: {missing}")
    frame = frame[GROUP_COLUMNS].copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["neutral"] = frame["neutral"].astype(bool)
    return frame.sort_values(["group", "date", "team_a"]).reset_index(drop=True)


def _top_score(prediction: dict[str, object]) -> tuple[int, int, str, float]:
    distribution = prediction["score_distribution"]
    if not isinstance(distribution, dict):
        return 0, 0, "0-0", 0.0
    score, probability = max(distribution.items(), key=lambda item: float(item[1]))
    left, right = str(score).split("-")
    return int(left), int(right), str(score), float(probability)


def _sort_standings(standings: dict[str, Standing]) -> list[dict[str, object]]:
    rows = sorted(
        standings.values(),
        key=lambda row: (row.points, row.goal_difference, row.goals_for, row.rating, row.team),
        reverse=True,
    )
    output: list[dict[str, object]] = []
    for rank, standing in enumerate(rows, start=1):
        data = asdict(standing)
        data["rank"] = rank
        data["goal_difference"] = standing.goal_difference
        output.append(data)
    return output


def _record(standings: dict[str, Standing], team_a: str, team_b: str, goals_a: int, goals_b: int) -> None:
    standings[team_a].record(goals_a, goals_b)
    standings[team_b].record(goals_b, goals_a)


def _known_result(latest_matches: pd.DataFrame, team_a: str, team_b: str) -> dict[str, object]:
    if latest_matches.empty:
        return {"found": False}
    home = latest_matches["home_team"].astype(str).str.lower().str.strip()
    away = latest_matches["away_team"].astype(str).str.lower().str.strip()
    a = team_a.lower().strip()
    b = team_b.lower().strip()
    matches = latest_matches[((home == a) & (away == b)) | ((home == b) & (away == a))]
    if matches.empty:
        return {"found": False}
    row = matches.sort_values("date").iloc[-1]
    home_team = str(row["home_team"])
    home_score = int(row["home_score"])
    away_score = int(row["away_score"])
    if home_team.lower().strip() == a:
        goals_a, goals_b = home_score, away_score
    else:
        goals_a, goals_b = away_score, home_score
    return {
        "found": True,
        "date": pd.to_datetime(row["date"]).date().isoformat(),
        "home_team": home_team,
        "away_team": str(row["away_team"]),
        "home_score": home_score,
        "away_score": away_score,
        "competition": str(row["competition"]),
        "goals_a": goals_a,
        "goals_b": goals_b,
    }


def _knockout_winner(goal_model: DixonColesPoissonModel, team_a: str, team_b: str) -> dict[str, object]:
    prediction = goal_model.predict_match(team_a, team_b, neutral=True).as_dict()
    goals_a, goals_b, score, score_probability = _top_score(prediction)
    if goals_a == goals_b:
        non_draw_total = max(float(prediction["win_prob_a"]) + float(prediction["win_prob_b"]), 1e-9)
        win_a_no_draw = float(prediction["win_prob_a"]) / non_draw_total
        winner = team_a if win_a_no_draw >= 0.5 else team_b
        method = "penalties"
    else:
        winner = team_a if goals_a > goals_b else team_b
        method = "regulation"
    return {
        "team_a": team_a,
        "team_b": team_b,
        "predicted_score": score,
        "score_probability": score_probability,
        "expected_goals_a": prediction["expected_goals_a"],
        "expected_goals_b": prediction["expected_goals_b"],
        "win_prob_a": prediction["win_prob_a"],
        "draw_prob": prediction["draw_prob"],
        "win_prob_b": prediction["win_prob_b"],
        "winner": winner,
        "method": method,
    }


def _play_round(goal_model: DixonColesPoissonModel, teams: list[str], name: str) -> tuple[list[str], list[dict[str, object]]]:
    winners: list[str] = []
    matches: list[dict[str, object]] = []
    for index in range(0, len(teams), 2):
        result = _knockout_winner(goal_model, teams[index], teams[index + 1])
        result["stage"] = name
        winners.append(str(result["winner"]))
        matches.append(result)
    return winners, matches


def project_knockout_bracket(
    goal_model: DixonColesPoissonModel,
    qualifiers: list[str],
    ratings: dict[str, float],
) -> dict[str, object]:
    seeded = sorted(qualifiers[:32], key=lambda team: ratings.get(team, 1500.0), reverse=True)
    bracket: list[str] = []
    for index in range(16):
        bracket.extend([seeded[index], seeded[-(index + 1)]])

    round_of_16, r32_matches = _play_round(goal_model, bracket, "Round of 32")
    quarterfinalists, r16_matches = _play_round(goal_model, round_of_16, "Round of 16")
    semifinalists, qf_matches = _play_round(goal_model, quarterfinalists, "Quarterfinals")
    finalists, sf_matches = _play_round(goal_model, semifinalists, "Semifinals")
    champion_result = _knockout_winner(goal_model, finalists[0], finalists[1])
    champion_result["stage"] = "Final"

    return {
        "round_of_32": r32_matches,
        "round_of_16": r16_matches,
        "quarterfinals": qf_matches,
        "semifinals": sf_matches,
        "final": champion_result,
        "champion": champion_result["winner"],
    }


def predict_group_stage(
    goal_model: DixonColesPoissonModel,
    latest_matches: pd.DataFrame,
    ratings: dict[str, float],
    fixtures: pd.DataFrame | None = None,
    config: Config | None = None,
) -> dict[str, object]:
    cfg = config or load_config()
    frame = fixtures if fixtures is not None else load_group_fixtures(cfg)
    groups: dict[str, dict[str, object]] = {}
    third_place: list[dict[str, object]] = []
    qualifiers: list[str] = []

    for group_name, group_frame in frame.groupby("group", sort=True):
        teams = sorted(set(group_frame["team_a"]).union(set(group_frame["team_b"])))
        standings = {
            team: Standing(team=team, rating=ratings.get(team, 1500.0))
            for team in teams
        }
        matches: list[dict[str, object]] = []

        for row in group_frame.itertuples(index=False):
            team_a = str(row.team_a)
            team_b = str(row.team_b)
            known = _known_result(latest_matches, team_a, team_b)
            if known["found"]:
                goals_a = int(known["goals_a"])
                goals_b = int(known["goals_b"])
                match = {
                    "group": group_name,
                    "date": pd.to_datetime(row.date).date().isoformat(),
                    "team_a": team_a,
                    "team_b": team_b,
                    "status": "played",
                    "score": f"{goals_a}-{goals_b}",
                    "winner": team_a if goals_a > goals_b else team_b if goals_b > goals_a else "Draw",
                    "known_result": known,
                }
            else:
                prediction = goal_model.predict_match(team_a, team_b, neutral=bool(row.neutral)).as_dict()
                goals_a, goals_b, score, score_probability = _top_score(prediction)
                match = {
                    "group": group_name,
                    "date": pd.to_datetime(row.date).date().isoformat(),
                    "team_a": team_a,
                    "team_b": team_b,
                    "status": "predicted",
                    "score": score,
                    "score_probability": score_probability,
                    "winner": team_a if goals_a > goals_b else team_b if goals_b > goals_a else "Draw",
                    "win_prob_a": prediction["win_prob_a"],
                    "draw_prob": prediction["draw_prob"],
                    "win_prob_b": prediction["win_prob_b"],
                    "expected_goals_a": prediction["expected_goals_a"],
                    "expected_goals_b": prediction["expected_goals_b"],
                }
            _record(standings, team_a, team_b, int(match["score"].split("-")[0]), int(match["score"].split("-")[1]))
            matches.append(match)

        table = _sort_standings(standings)
        for row in table:
            row["group"] = group_name
        third_place.append(table[2])
        qualifiers.extend([str(table[0]["team"]), str(table[1]["team"])])
        groups[str(group_name)] = {
            "group": str(group_name),
            "matches": matches,
            "table": table,
            "winner": table[0]["team"],
            "runner_up": table[1]["team"],
            "third_place": table[2]["team"],
            "eliminated": table[3]["team"],
        }

    best_thirds = sorted(
        third_place,
        key=lambda row: (row["points"], row["goal_difference"], row["goals_for"], row["rating"], row["team"]),
        reverse=True,
    )
    qualifiers.extend([str(row["team"]) for row in best_thirds[:8]])
    bracket = project_knockout_bracket(goal_model, qualifiers, ratings)

    return {
        "groups": groups,
        "third_place_ranking": best_thirds,
        "qualified_round_of_32": qualifiers,
        "knockout_projection": bracket,
    }
