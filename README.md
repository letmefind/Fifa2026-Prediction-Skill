# FIFA World Cup 2026 Prediction Engine

**A production-ready prediction stack for the 2026 World Cup** — match forecasts, group-stage tables, tournament simulations, betting EV, and a web dashboard. Built for analysts, bettors, and AI workflows.

🌐 **[Live demo (static preview)](https://letmefind.github.io/Fifa2026-Prediction-Skill/)** — UI only; predictions are sample data. [Why it's not live →](docs/GITHUB_PAGES.md)

Use it as a **Python app**, a **REST API + dashboard**, or a **Claude AI Skill** that runs the same engine from natural language.

---

## Claude AI Skill

Install this repository as a **Claude Skill** so Claude can predict matches, simulate the tournament, refresh live scores, and build betting analysis using this engine.

| | |
|---|---|
| **Skill folder** | [`claude-skill/fifa2026-prediction/`](claude-skill/fifa2026-prediction/) |
| **Install guide** | [`claude-skill/README.md`](claude-skill/README.md) |
| **Skill instructions** | [`claude-skill/fifa2026-prediction/SKILL.md`](claude-skill/fifa2026-prediction/SKILL.md) |
| **Full tournament workflow** | [`claude-skill/fifa2026-prediction/FULL_TOURNAMENT_WORKFLOW.md`](claude-skill/fifa2026-prediction/FULL_TOURNAMENT_WORKFLOW.md) |

**Quick install:** upload or point Claude to the nested folder `claude-skill/fifa2026-prediction/`, then clone or open this repo so Claude can run CLI/API commands.

```bash
git clone https://github.com/letmefind/Fifa2026-Prediction-Skill.git
```

The skill teaches Claude to ask for simulation runs (default 5,000), refresh latest scores before predicting, generate reasoning prompts, and follow a full World Cup research workflow.

---

## Languages / زبان‌ها / 语言

Full help in **10 languages** (setup, CLI, dashboard, betting, Claude skill):

<p>
  <a href="docs/README_10_LANGUAGES.md#1-فارسی"><kbd>Persian / فارسی</kbd></a>
  <a href="docs/README_10_LANGUAGES.md#2-العربية"><kbd>Arabic / العربية</kbd></a>
  <a href="docs/README_10_LANGUAGES.md#3-español"><kbd>Spanish / Español</kbd></a>
  <a href="docs/README_10_LANGUAGES.md#4-français"><kbd>French / Français</kbd></a>
  <a href="docs/README_10_LANGUAGES.md#5-deutsch"><kbd>German / Deutsch</kbd></a>
  <a href="docs/README_10_LANGUAGES.md#6-português"><kbd>Portuguese / Português</kbd></a>
  <a href="docs/README_10_LANGUAGES.md#7-italiano"><kbd>Italian / Italiano</kbd></a>
  <a href="docs/README_10_LANGUAGES.md#8-türkçe"><kbd>Turkish / Türkçe</kbd></a>
  <a href="docs/README_10_LANGUAGES.md#9-हिन्दी"><kbd>Hindi / हिन्दी</kbd></a>
  <a href="docs/README_10_LANGUAGES.md#10-中文"><kbd>Chinese / 中文</kbd></a>
</p>

📄 [Open multilingual guide](docs/README_10_LANGUAGES.md)

---

## What this repo does

| Use case | What you get |
|----------|----------------|
| **Single match** | Win / draw / loss probabilities, expected goals, score distribution |
| **By date** | All group games on a day (e.g. `18 jun`) with model odds and decimal odds |
| **By group** | Official FIFA groups, real scores for played games, projected tables |
| **Tournament** | Monte Carlo World Cup winner and knockout odds (48 teams, 12 groups) |
| **Betting** | Expected value vs market odds — [Betting guide](docs/BETTING_GUIDE.md) |
| **Claude / LLM** | Structured prompts and plain-English explanations |

**Model stack:** ELO ratings → attack/defense strengths (goals + xG) → Poisson with Dixon-Coles → Monte Carlo simulation.

**Data:** Official [FIFA 2026 group fixtures](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/scores-fixtures), live score refresh via CSV + API-Football, 48 qualified teams.

---

## Quick start

```bash
git clone https://github.com/letmefind/Fifa2026-Prediction-Skill.git
cd Fifa2026-Prediction-Skill
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Dashboard:**

```bash
uvicorn api.main:app --reload
# Open http://127.0.0.1:8000/
```

**CLI examples:**

```bash
python -m cli.main refresh-latest-data
python -m cli.main predict-match Brazil France
python -m cli.main predict-by-date "18 jun"
python -m cli.main group-predictions --group G
python -m cli.main simulate-tournament --runs 5000
python -m cli.main betting-edge 0.55 2.20
```

**Recommended workflow:** `refresh-latest-data` → `predict-match` or `predict-by-date` or `group-predictions`. Use `simulate-tournament` only when you need World Cup winner / knockout odds.

---

## Dashboard preview

![Dashboard full view](docs/screenshots/dashboard-full.png)

![Match prediction result](docs/screenshots/dashboard-match-result.png)

The dashboard includes match prediction, predictions by date (with full odds), group stage views, tournament simulation, EV calculator, and a **Refresh Latest Data** button that fetches scores and rebuilds the model.

---

## Features

- Official FIFA 2026 group fixtures and 48-team ratings
- Latest score ingestion: `data/latest_results.csv`, Football-Data API, API-Football
- ELO + attack/defense strengths with goals/xG blend and shrinkage
- Poisson score model with Dixon-Coles low-score adjustment
- Group predictions: played scores + future forecasts + projected tables
- Predictions by date with win/draw/loss %, decimal odds, xG, top scorelines
- 48-team Monte Carlo simulation through Round of 32 to final
- FastAPI REST API, Typer CLI, browser dashboard
- Claude Skill package for AI-driven prediction workflows
- Betting EV module and [Polymarket / sportsbook guide](docs/BETTING_GUIDE.md)
- YAML configuration and pytest coverage

---

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web dashboard |
| `GET` | `/teams` | All teams in model |
| `POST` | `/predict_match` | Match probabilities |
| `POST` | `/simulate` | Tournament Monte Carlo |
| `GET` | `/predictions/date?date=18%20jun` | All matches on a date + odds |
| `GET` | `/groups/predictions` | Full group-stage predictions |
| `GET` | `/groups/{group}` | Single group (e.g. `/groups/G`) |
| `POST` | `/data/refresh_latest` | Fetch scores and rebuild model |
| `GET` | `/data/latest_status` | Latest data status |
| `GET` | `/team/{name}` | Team profile |
| `GET` | `/tournament/probabilities?runs=10000` | Title odds table |

---

## Project structure

```text
claude-skill/  Claude AI skill (install this for Claude)
api/           FastAPI app and service layer
cli/           Command-line interface
web/           Browser dashboard
data/          Fixtures, ratings, latest results, ingestion
models/        ELO, strengths, goal model, LLM, betting EV
simulation/    Group and knockout tournament logic
config/        YAML parameters
docs/          Betting guide, multilingual README, screenshots
tests/         Unit and integration tests
```

---

## Live data and API keys

```bash
cp .env.example .env
# Set API_FOOTBALL_KEY and/or FOOTBALL_DATA_API_KEY
python -m cli.main refresh-latest-data
python -m cli.main latest-data-status
```

- **`data/latest_results.csv`** — manual score updates
- **API feeds** — auto-fetch on refresh (free API-Football plans are rate-limited; results are cached in `.cache/fifa2026/`)

When a match is already in latest results, the app shows the **real score** and labels probabilities as a **rematch forecast**.

---

## Configuration

Edit [`config/default.yaml`](config/default.yaml) for ELO K-factor, xG weights, Poisson base goals, Dixon-Coles rho, simulation runs, and data paths.

---

## Testing

```bash
pytest
```

---

## Disclaimer

This software estimates probabilities; it does not guarantee profitable bets. Always verify squads, injuries, lineups, and market liquidity before wagering.
