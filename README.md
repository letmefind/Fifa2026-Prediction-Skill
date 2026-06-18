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

---

## Predictions — 2026-06-18

Generated with **50,000 Monte Carlo tournament simulations** using latest scores through 2026-06-17 (88 matches in model).

### Images

| Report | File |
|--------|------|
| Full tournament odds (all 48 teams) | [tournament-simulation-50000-runs.png](docs/screenshots/2026-06-18/tournament-simulation-50000-runs.png) |
| All group-stage matches (72) + predicted scores | [all-matches-predictions-2026-06-18.png](docs/screenshots/2026-06-18/all-matches-predictions-2026-06-18.png) |
| Round of 32 projections (16 matches) | [round-of-32-predictions-2026-06-18.png](docs/screenshots/2026-06-18/round-of-32-predictions-2026-06-18.png) |

### All group-stage matches (72)

22 played (actual score) · 50 predicted · odds for upcoming games

| Date | Grp | Match | Pred. Score | Status | Win A | Draw | Win B | Odds A | Odds D | Odds B |
|------|-----|-------|-------------|--------|-------|------|-------|--------|--------|--------|
| 2026-06-11 | A | Mexico vs South Africa | 2-0 | played | — | — | — | — | — | — |
| 2026-06-12 | A | South Korea vs Czechia | 2-1 | played | — | — | — | — | — | — |
| 2026-06-12 | B | Canada vs Bosnia and Herzegovina | 1-1 | played | — | — | — | — | — | — |
| 2026-06-13 | B | Qatar vs Switzerland | 1-1 | played | — | — | — | — | — | — |
| 2026-06-13 | C | Brazil vs Morocco | 1-1 | played | — | — | — | — | — | — |
| 2026-06-13 | D | USA vs Paraguay | 4-1 | played | — | — | — | — | — | — |
| 2026-06-14 | C | Haiti vs Scotland | 0-1 | played | — | — | — | — | — | — |
| 2026-06-14 | D | Australia vs Turkey | 2-0 | played | — | — | — | — | — | — |
| 2026-06-14 | E | Côte d'Ivoire vs Ecuador | 1-0 | played | — | — | — | — | — | — |
| 2026-06-14 | E | Germany vs Curaçao | 7-1 | played | — | — | — | — | — | — |
| 2026-06-14 | F | Netherlands vs Japan | 2-2 | played | — | — | — | — | — | — |
| 2026-06-15 | F | Sweden vs Tunisia | 5-1 | played | — | — | — | — | — | — |
| 2026-06-15 | G | Belgium vs Egypt | 1-1 | played | — | — | — | — | — | — |
| 2026-06-15 | H | Saudi Arabia vs Uruguay | 1-1 | played | — | — | — | — | — | — |
| 2026-06-15 | H | Spain vs Cape Verde | 0-0 | played | — | — | — | — | — | — |
| 2026-06-16 | G | Iran vs New Zealand | 2-2 | played | — | — | — | — | — | — |
| 2026-06-16 | I | France vs Senegal | 3-1 | played | — | — | — | — | — | — |
| 2026-06-16 | I | Iraq vs Norway | 1-4 | played | — | — | — | — | — | — |
| 2026-06-17 | J | Argentina vs Algeria | 3-0 | played | — | — | — | — | — | — |
| 2026-06-17 | J | Austria vs Jordan | 3-1 | played | — | — | — | — | — | — |
| 2026-06-17 | K | Portugal vs Congo DR | 1-1 | played | — | — | — | — | — | — |
| 2026-06-17 | L | England vs Croatia | 4-2 | played | — | — | — | — | — | — |
| 2026-06-17 | L | Ghana vs Panama | 2-1 | predicted | 43.7% | 26.6% | 29.8% | 2.29 | 3.77 | 3.36 |
| 2026-06-18 | A | Czechia vs South Africa | 2-1 | predicted | 41.2% | 27.6% | 31.2% | 2.43 | 3.62 | 3.20 |
| 2026-06-18 | B | Canada vs Qatar | 1-0 | predicted | 35.6% | 29.4% | 35.1% | 2.81 | 3.41 | 2.85 |
| 2026-06-18 | B | Switzerland vs Bosnia and Herzegovina | 1-0 | predicted | 43.1% | 27.5% | 29.4% | 2.32 | 3.64 | 3.40 |
| 2026-06-18 | K | Uzbekistan vs Colombia | 0-1 | predicted | 18.8% | 24.9% | 56.4% | 5.33 | 4.02 | 1.77 |
| 2026-06-19 | A | Mexico vs South Korea | 1-0 | predicted | 37.4% | 28.0% | 34.6% | 2.68 | 3.57 | 2.89 |
| 2026-06-19 | C | Scotland vs Morocco | 1-2 | predicted | 26.7% | 26.8% | 46.5% | 3.75 | 3.73 | 2.15 |
| 2026-06-19 | D | USA vs Australia | 1-0 | predicted | 42.5% | 27.7% | 29.8% | 2.35 | 3.61 | 3.35 |
| 2026-06-20 | C | Brazil vs Haiti | 1-0 | predicted | 55.3% | 26.2% | 18.5% | 1.81 | 3.81 | 5.41 |
| 2026-06-20 | D | Turkey vs Paraguay | 1-2 | predicted | 33.0% | 27.6% | 39.4% | 3.03 | 3.62 | 2.54 |
| 2026-06-20 | E | Germany vs Côte d'Ivoire | 2-1 | predicted | 58.4% | 22.8% | 18.8% | 1.71 | 4.38 | 5.33 |
| 2026-06-20 | F | Netherlands vs Sweden | 1-2 | predicted | 36.3% | 25.6% | 38.1% | 2.76 | 3.91 | 2.62 |
| 2026-06-21 | E | Ecuador vs Curaçao | 2-1 | predicted | 54.2% | 24.4% | 21.4% | 1.84 | 4.10 | 4.67 |
| 2026-06-21 | F | Tunisia vs Japan | 1-2 | predicted | 23.2% | 23.7% | 53.1% | 4.31 | 4.21 | 1.88 |
| 2026-06-21 | G | Belgium vs Iran | 2-1 | predicted | 39.2% | 27.6% | 33.1% | 2.55 | 3.62 | 3.02 |
| 2026-06-21 | H | Spain vs Saudi Arabia | 1-0 | predicted | 58.1% | 24.3% | 17.5% | 1.72 | 4.11 | 5.70 |
| 2026-06-21 | H | Uruguay vs Cape Verde | 1-0 | predicted | 45.2% | 30.5% | 24.3% | 2.21 | 3.28 | 4.11 |
| 2026-06-22 | G | New Zealand vs Egypt | 1-2 | predicted | 31.2% | 27.2% | 41.6% | 3.20 | 3.68 | 2.40 |
| 2026-06-22 | I | France vs Iraq | 2-0 | predicted | 60.8% | 23.4% | 15.8% | 1.64 | 4.28 | 6.33 |
| 2026-06-22 | J | Argentina vs Austria | 1-0 | predicted | 57.6% | 24.3% | 18.0% | 1.74 | 4.11 | 5.55 |
| 2026-06-23 | I | Norway vs Senegal | 2-1 | predicted | 46.5% | 25.4% | 28.1% | 2.15 | 3.94 | 3.56 |
| 2026-06-23 | J | Jordan vs Algeria | 1-2 | predicted | 34.6% | 27.0% | 38.4% | 2.89 | 3.70 | 2.61 |
| 2026-06-23 | K | Portugal vs Uzbekistan | 1-0 | predicted | 50.8% | 26.6% | 22.6% | 1.97 | 3.76 | 4.42 |
| 2026-06-23 | L | England vs Ghana | 2-1 | predicted | 59.0% | 23.1% | 17.9% | 1.70 | 4.33 | 5.58 |
| 2026-06-23 | L | Panama vs Croatia | 1-2 | predicted | 26.5% | 24.1% | 49.4% | 3.77 | 4.15 | 2.03 |
| 2026-06-24 | B | Bosnia and Herzegovina vs Qatar | 0-1 | predicted | 34.0% | 28.4% | 37.6% | 2.94 | 3.53 | 2.66 |
| 2026-06-24 | B | Switzerland vs Canada | 1-0 | predicted | 41.1% | 28.6% | 30.3% | 2.43 | 3.50 | 3.30 |
| 2026-06-24 | C | Morocco vs Haiti | 1-0 | predicted | 50.1% | 27.0% | 22.9% | 2.00 | 3.70 | 4.37 |
| 2026-06-24 | C | Scotland vs Brazil | 0-1 | predicted | 19.9% | 25.7% | 54.4% | 5.03 | 3.89 | 1.84 |
| 2026-06-24 | K | Colombia vs Congo DR | 1-0 | predicted | 55.0% | 25.5% | 19.5% | 1.82 | 3.92 | 5.13 |
| 2026-06-25 | A | Czechia vs Mexico | 0-1 | predicted | 27.3% | 27.2% | 45.5% | 3.66 | 3.68 | 2.20 |
| 2026-06-25 | A | South Africa vs South Korea | 0-1 | predicted | 24.4% | 26.4% | 49.2% | 4.10 | 3.78 | 2.03 |
| 2026-06-25 | E | Curaçao vs Côte d'Ivoire | 1-2 | predicted | 16.9% | 21.8% | 61.3% | 5.93 | 4.58 | 1.63 |
| 2026-06-25 | E | Ecuador vs Germany | 0-2 | predicted | 14.7% | 21.1% | 64.3% | 6.82 | 4.74 | 1.56 |
| 2026-06-25 | F | Japan vs Sweden | 1-2 | predicted | 29.9% | 25.2% | 44.9% | 3.35 | 3.96 | 2.23 |
| 2026-06-25 | F | Tunisia vs Netherlands | 1-2 | predicted | 19.2% | 22.1% | 58.6% | 5.20 | 4.52 | 1.71 |
| 2026-06-26 | D | Paraguay vs Australia | 0-1 | predicted | 24.7% | 26.5% | 48.8% | 4.05 | 3.78 | 2.05 |
| 2026-06-26 | D | Turkey vs USA | 0-2 | predicted | 17.6% | 23.7% | 58.7% | 5.69 | 4.21 | 1.70 |
| 2026-06-26 | I | Norway vs France | 0-1 | predicted | 27.4% | 27.8% | 44.9% | 3.66 | 3.60 | 2.23 |
| 2026-06-26 | I | Senegal vs Iraq | 2-1 | predicted | 48.8% | 25.0% | 26.2% | 2.05 | 4.00 | 3.81 |
| 2026-06-27 | G | Egypt vs Iran | 1-2 | predicted | 34.7% | 27.4% | 37.9% | 2.88 | 3.65 | 2.64 |
| 2026-06-27 | G | New Zealand vs Belgium | 1-2 | predicted | 28.4% | 27.1% | 44.5% | 3.52 | 3.69 | 2.25 |
| 2026-06-27 | H | Cape Verde vs Saudi Arabia | 0-1 | predicted | 33.3% | 29.4% | 37.3% | 3.00 | 3.40 | 2.68 |
| 2026-06-27 | H | Uruguay vs Spain | 0-1 | predicted | 23.0% | 29.0% | 47.9% | 4.34 | 3.44 | 2.09 |
| 2026-06-27 | K | Colombia vs Portugal | 1-0 | predicted | 39.8% | 29.1% | 31.1% | 2.51 | 3.44 | 3.21 |
| 2026-06-27 | K | Congo DR vs Uzbekistan | 1-0 | predicted | 37.7% | 28.0% | 34.2% | 2.65 | 3.57 | 2.92 |
| 2026-06-27 | L | Croatia vs Ghana | 2-1 | predicted | 41.6% | 25.8% | 32.6% | 2.40 | 3.88 | 3.07 |
| 2026-06-27 | L | Panama vs England | 0-2 | predicted | 13.8% | 20.0% | 66.2% | 7.24 | 5.01 | 1.51 |
| 2026-06-28 | J | Algeria vs Austria | 1-2 | predicted | 22.2% | 24.7% | 53.2% | 4.51 | 4.05 | 1.88 |
| 2026-06-28 | J | Jordan vs Argentina | 0-2 | predicted | 11.1% | 19.8% | 69.1% | 9.01 | 5.06 | 1.45 |

### Top title contenders (50k runs)

| Team | Win WC | Reach Final | Reach Semis | Round of 32 |
|------|--------|-------------|-------------|-------------|
| Argentina | 16.5% | 21.8% | 32.9% | 95.5% |
| Germany | 14.9% | 20.2% | 35.6% | 96.2% |
| England | 8.1% | 11.7% | 20.1% | 93.0% |
| Spain | 8.0% | 11.6% | 19.8% | 89.6% |
| Colombia | 6.5% | 12.3% | 24.3% | 86.2% |

Full JSON data: [report-2026-06-18.json](docs/screenshots/2026-06-18/report-2026-06-18.json)

Regenerate: `python scripts/generate_daily_report.py`
