from __future__ import annotations

import json
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from api.service import get_service
from data import update_dataset
from models.betting import calculate_ev
from models.llm import explain_prediction, generate_llm_prompt


app = typer.Typer(help="FIFA World Cup 2026 prediction engine")
console = Console()


@app.command("predict-match")
def predict_match(
    team_a: str,
    team_b: str,
    neutral: bool = typer.Option(True, help="Whether the match is at a neutral venue."),
    llm_prompt: bool = typer.Option(False, help="Print an LLM-ready reasoning prompt."),
) -> None:
    service = get_service()
    result = service.predict_match(team_a, team_b, neutral=neutral)
    console.print_json(json.dumps(result, default=str))
    console.print(explain_prediction(result))
    if llm_prompt:
        stats = {"team_a": service.team_profile(team_a), "team_b": service.team_profile(team_b)}
        console.print(generate_llm_prompt({"team_a": team_a, "team_b": team_b, "prediction": result}, stats))


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
) -> None:
    probabilities = get_service().simulate_tournament(n=runs)["probabilities"]
    row = next((item for item in probabilities if item["team"].lower() == team.lower()), None)
    if row is None:
        raise typer.BadParameter(f"Unknown team: {team}")
    console.print_json(json.dumps(row, default=str))


@app.command("team")
def team(name: str) -> None:
    console.print_json(json.dumps(get_service().team_profile(name), default=str))


@app.command("betting-edge")
def betting_edge(
    model_prob: float = typer.Argument(..., min=0.0, max=1.0),
    market_odds: float = typer.Argument(..., min=1.01),
) -> None:
    console.print_json(json.dumps(calculate_ev(model_prob, market_odds).as_dict()))


@app.command("update-dataset")
def update_data(
    source: str = typer.Option("csv", help="csv, spi, or statsbomb."),
    output_dir: Optional[str] = typer.Option(None, help="Directory for refreshed CSV files."),
) -> None:
    outputs = update_dataset(source=source, output_dir=output_dir)
    console.print_json(json.dumps({key: str(path) for key, path in outputs.items()}))


if __name__ == "__main__":
    app()
