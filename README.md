# FIFA World Cup 2026 Prediction Engine

Production-ready Python prediction engine for FIFA World Cup 2026 match forecasts, tournament simulation, LLM reasoning prompts, and betting expected value analysis.

## Features

- CSV-first data ingestion with real-ready FiveThirtyEight SPI and StatsBomb adapters.
- ELO ratings with configurable K-factor and home advantage.
- Attack/defense team strengths blended from goals and xG with shrinkage.
- Poisson score model with Dixon-Coles low-score correlation adjustment.
- 48-team tournament Monte Carlo simulation: 12 groups, best third-place ranking, round of 32 through final.
- FastAPI REST interface and Typer CLI.
- LLM integration helpers for Claude/GPT prompts and plain-English explanations.
- Betting expected value and edge labelling.
- YAML configuration and pytest coverage.

## Project Structure

```text
data/          Data adapters, schemas, ingestion, sample CSVs
models/        ELO, strengths, goal model, LLM, betting EV
simulation/    Group and knockout tournament simulation
api/           FastAPI app and service layer
cli/           Command-line interface
claude-skill/  Claude skill package for AI prediction workflows
config/        YAML parameters and typed settings
tests/         Unit and sanity tests
notebooks/     Optional analysis workspace
```

## Setup

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## CLI Usage

```bash
python -m cli.main predict-match Brazil France
python -m cli.main predict-match Brazil France --llm-prompt
python -m cli.main simulate-tournament --runs 50000
python -m cli.main team-probabilities Brazil --runs 10000
python -m cli.main betting-edge 0.55 2.20
```

## API Usage

```bash
uvicorn api.main:app --reload
```

Endpoints:

- `POST /predict_match` with `{"team_a": "Brazil", "team_b": "France", "neutral": true}`
- `POST /simulate` with `{"runs": 10000}`
- `GET /team/{name}`
- `GET /tournament/probabilities?runs=10000`

## Claude Skill

The Claude skill package lives in `claude-skill/fifa2026-prediction/`.

It teaches Claude how to install this engine, run CLI/API predictions, generate match reasoning prompts, simulate tournaments, and evaluate betting EV. Upload or install that nested folder as the skill package.

## Data

The repository ships with sample CSVs so the engine works immediately. Replace these files with current data for serious analysis:

- `data/sample_matches.csv`
- `data/sample_team_ratings.csv`
- `data/sample_xg.csv`

To refresh adapter output:

```bash
python -m cli.main update-dataset --source csv
python -m cli.main update-dataset --source spi
STATSBOMB_API_KEY=... python -m cli.main update-dataset --source statsbomb
```

## Configuration

Edit `config/default.yaml` to tune:

- ELO `k_factor` and `home_advantage`
- attack/xG blending weights
- Poisson base goal rate
- Dixon-Coles `rho`
- Monte Carlo default runs and seed

## Example Output

```json
{
  "team": "Brazil",
  "win_world_cup": 0.18,
  "reach_final": 0.32,
  "reach_semis": 0.48
}
```

## Testing

```bash
pytest
```

## Betting Note

This software estimates probabilities; it does not guarantee profitable bets. Use current squads, injuries, market odds, lineup news, and liquidity checks before making any wager.
