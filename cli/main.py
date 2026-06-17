from __future__ import annotations

import json
from typing import Optional

import typer
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from api.service import get_service, refresh_service
from data import update_dataset
from models.betting import calculate_ev
from models.llm import explain_prediction, generate_llm_prompt


app = typer.Typer(help="FIFA World Cup 2026 prediction engine")
console = Console()


def _pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def _top_scores(result: dict[str, object], limit: int = 5) -> list[tuple[str, float]]:
    distribution = result["score_distribution"]
    if not isinstance(distribution, dict):
        return []
    return sorted(
        ((str(score), float(probability)) for score, probability in distribution.items()),
        key=lambda item: item[1],
        reverse=True,
    )[:limit]


def _render_match_summary(result: dict[str, object]) -> None:
    team_a = str(result["team_a"])
    team_b = str(result["team_b"])
    table = Table(title=f"{team_a} vs {team_b}", box=box.ROUNDED)
    table.add_column("Outcome")
    table.add_column("Probability", justify="right")
    table.add_column("Expected Goals", justify="right")
    table.add_row(f"{team_a} win", _pct(float(result["win_prob_a"])), f"{float(result['expected_goals_a']):.2f}")
    table.add_row("Draw", _pct(float(result["draw_prob"])), "-")
    table.add_row(f"{team_b} win", _pct(float(result["win_prob_b"])), f"{float(result['expected_goals_b']):.2f}")
    console.print(table)

    scores = Table(title="Most Likely Scores", box=box.SIMPLE_HEAVY)
    scores.add_column("Score")
    scores.add_column("Probability", justify="right")
    for score, probability in _top_scores(result):
        scores.add_row(score, _pct(probability))
    console.print(scores)
    console.print(Panel(explain_prediction(result), title="Interpretation", border_style="green"))


@app.command("predict-match")
def predict_match(
    team_a: str,
    team_b: str,
    neutral: bool = typer.Option(True, help="Whether the match is at a neutral venue."),
    llm_prompt: bool = typer.Option(False, help="Print an LLM-ready reasoning prompt."),
    json_output: bool = typer.Option(False, "--json-output", help="Print the raw JSON response."),
) -> None:
    service = get_service()
    result = service.predict_match(team_a, team_b, neutral=neutral)
    if json_output:
        console.print_json(json.dumps(result, default=str))
    else:
        _render_match_summary(result)
    if llm_prompt:
        stats = {"team_a": service.team_profile(team_a), "team_b": service.team_profile(team_b)}
        console.print(
            Panel(
                generate_llm_prompt({"team_a": team_a, "team_b": team_b, "prediction": result}, stats),
                title="LLM Prompt",
                border_style="blue",
            )
        )


@app.command("simulate-tournament")
def simulate_tournament(
    runs: int = typer.Option(10000, "--runs", "-r", min=1, help="Monte Carlo runs."),
) -> None:
    result = get_service().simulate_tournament(n=runs)
    table = Table(title=f"Tournament probabilities ({runs:,} runs)")
    table.add_column("Team")
    table.add_column("Win WC", justify="right")
    table.add_column("Final", justify="right")
    table.add_column("Semis", justify="right")
    for row in result["probabilities"][:20]:
        table.add_row(
            str(row["team"]),
            f"{float(row['win_world_cup']):.3f}",
            f"{float(row['reach_final']):.3f}",
            f"{float(row['reach_semis']):.3f}",
        )
    console.print(table)


@app.command("team-probabilities")
def team_probabilities(
    team: str,
    runs: int = typer.Option(10000, "--runs", "-r", min=1),
    json_output: bool = typer.Option(False, "--json-output", help="Print the raw JSON response."),
) -> None:
    probabilities = get_service().simulate_tournament(n=runs)["probabilities"]
    row = next((item for item in probabilities if item["team"].lower() == team.lower()), None)
    if row is None:
        raise typer.BadParameter(f"Unknown team: {team}")
    if json_output:
        console.print_json(json.dumps(row, default=str))
        return
    table = Table(title=f"{row['team']} tournament probabilities ({runs:,} runs)", box=box.ROUNDED)
    table.add_column("Stage")
    table.add_column("Probability", justify="right")
    table.add_row("Reach Round of 32", _pct(float(row["round_of_32"])))
    table.add_row("Reach Semifinals", _pct(float(row["reach_semis"])))
    table.add_row("Reach Final", _pct(float(row["reach_final"])))
    table.add_row("Win World Cup", _pct(float(row["win_world_cup"])))
    console.print(table)


@app.command("team")
def team(name: str) -> None:
    profile = get_service().team_profile(name)
    table = Table(title=f"{name} team profile", box=box.ROUNDED)
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("ELO rating", f"{float(profile['elo_rating']):.1f}")
    table.add_row("Attack strength", f"{float(profile['attack_strength']):.3f}")
    table.add_row("Defense strength", f"{float(profile['defense_strength']):.3f}")
    table.add_row("Matches in model", str(profile["matches_in_model"]))
    console.print(table)


@app.command("betting-edge")
def betting_edge(
    model_prob: float = typer.Argument(..., min=0.0, max=1.0),
    market_odds: float = typer.Argument(..., min=1.01),
) -> None:
    edge = calculate_ev(model_prob, market_odds)
    table = Table(title="Betting Expected Value", box=box.ROUNDED)
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Model probability", _pct(edge.model_prob))
    table.add_row("Market odds", f"{edge.market_odds:.2f}")
    table.add_row("Implied probability", _pct(edge.implied_prob))
    table.add_row("Expected value", f"{edge.expected_value:.3f}")
    table.add_row("Edge", _pct(edge.edge))
    table.add_row("Label", edge.label)
    console.print(table)


@app.command("update-dataset")
def update_data(
    source: str = typer.Option("csv", help="csv, spi, or statsbomb."),
    output_dir: Optional[str] = typer.Option(None, help="Directory for refreshed CSV files."),
) -> None:
    outputs = update_dataset(source=source, output_dir=output_dir)
    console.print_json(json.dumps({key: str(path) for key, path in outputs.items()}))


@app.command("latest-data-status")
def latest_data_status() -> None:
    console.print_json(json.dumps(get_service().latest_status(), default=str))


@app.command("refresh-latest-data")
def refresh_latest_data() -> None:
    console.print_json(json.dumps(refresh_service().latest_status(), default=str))


if __name__ == "__main__":
    app()
