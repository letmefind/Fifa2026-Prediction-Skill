---
name: fifa2026-prediction
description: Predict FIFA World Cup 2026 matches, simulate full tournaments, research squad/team reality, explain football model outputs, and evaluate betting expected value using the Fifa2026-Prediction-Skill Python engine. Use when the user asks for World Cup predictions, match probabilities, score distributions, tournament odds, team probabilities, betting edges, full 104-match forecasts, qualified-team research, or Claude/GPT-ready football reasoning.
---

# FIFA 2026 Prediction

Use this skill to run the FIFA World Cup 2026 prediction engine from:

```text
https://github.com/letmefind/Fifa2026-Prediction-Skill.git
```

## First Check

If the repository is not present locally, clone it:

```bash
git clone https://github.com/letmefind/Fifa2026-Prediction-Skill.git
cd Fifa2026-Prediction-Skill
```

If dependencies are not installed, create a virtual environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Use `.venv/bin/python` for all commands below.

## Before Every Prediction

1. Ask the user how many tournament simulation runs to use when the task includes tournament odds, champion probabilities, group outcomes, or full World Cup simulation.
2. If the user does not specify a run count, use `5000` runs by default.
3. Check the latest score/results at calculation time when web, sports data, or user-provided live data is available.
4. If a relevant latest completed match is missing from the local dataset, state that and incorporate it as current context before explaining the prediction.
5. If the match is already live, ask for or check the current score and match minute. Treat the normal model output as the pre-match baseline, then adjust reasoning for current score, red cards, injuries, remaining time, and momentum. Clearly label it as an in-play adjustment.
6. If latest-score access is unavailable, say so and ask the user to provide the latest score or confirm that a model-only prediction is acceptable.

## Match Prediction

For a user asking who will win, likely score, expected goals, or probabilities:

```bash
.venv/bin/python -m cli.main predict-match Brazil France
```

Use neutral venue by default for World Cup matches. If the user specifies home advantage, run:

```bash
.venv/bin/python -m cli.main predict-match USA Mexico --neutral false
```

Report:

- win probability for each team
- draw probability
- expected goals for each team
- most likely 3-5 scorelines
- short explanation of uncertainty

## LLM Reasoning Prompt

When the user wants Claude/GPT reasoning input or a prompt:

```bash
.venv/bin/python -m cli.main predict-match Brazil France --llm-prompt
```

Use the generated prompt as the structured quantitative base. Do not invent probabilities that differ from the model output.

## Tournament Simulation

For champion odds, reaching final, semifinal, or round-of-32 chances:

```bash
.venv/bin/python -m cli.main simulate-tournament --runs 5000
```

For a single team:

```bash
.venv/bin/python -m cli.main team-probabilities Brazil --runs 5000
```

Ask the user for the run count first. If no run count is provided, use `5000`. Use `50000` or more only when the user asks for more stable probabilities and runtime is acceptable.

If the user asks for an elite analyst, Gemini-style, "entire World Cup", "all 104 matches", squad research, current 2025-2026 data, market validation, awards, or country-by-country reality-based prediction, follow [FULL_TOURNAMENT_WORKFLOW.md](FULL_TOURNAMENT_WORKFLOW.md).

## Team Profile

For ELO, attack strength, defense strength, and recent matches:

```bash
.venv/bin/python -m cli.main team Brazil
```

## Betting Edge

For decimal odds:

```bash
.venv/bin/python -m cli.main betting-edge 0.55 2.20
```

Interpretation:

- `expected_value > 0` means positive model EV before bookmaker margin, limits, and uncertainty.
- `undervalued` means the market odds are higher than the model's fair odds.
- `overvalued` means the market odds are lower than the model's fair odds.

Always state that outputs are model estimates, not guaranteed betting profit.

For Polymarket, Betfair Exchange, sportsbook odds conversion, edge thresholds, and bankroll/risk workflow, follow [BETTING_GUIDE.md](../../docs/BETTING_GUIDE.md). If the guide is not available in the skill package, use the same method: convert market price to implied probability, compare against model probability, calculate EV, then check fees, liquidity, spread, lineups, injuries, and resolution rules.

## API Mode

If a persistent service is better than CLI calls:

```bash
.venv/bin/uvicorn api.main:app --reload
```

Endpoints:

- `POST /predict_match`
- `POST /simulate`
- `GET /team/{name}`
- `GET /tournament/probabilities`

## Response Template

For match predictions, answer in this format:

```text
[Team A] vs [Team B]

Model probabilities:
- [Team A] win: [x%]
- Draw: [x%]
- [Team B] win: [x%]

Expected goals: [Team A] [x.xx], [Team B] [x.xx]
Most likely scores: [score] ([x%]), [score] ([x%]), [score] ([x%])

Interpretation:
[2-4 concise sentences about model lean, uncertainty, and what drives the forecast.]
```

For tournament probabilities, answer with JSON when the user asks for machine-readable output:

```json
{
  "team": "Brazil",
  "win_world_cup": 0.18,
  "reach_final": 0.32,
  "reach_semis": 0.48
}
```

## Data Caution

The bundled CSVs are sample data for immediate use. For serious betting analysis, refresh inputs with current ratings, injuries, squads, lineups, market odds, and verified match data before making recommendations. If current web/data tools are unavailable, clearly label the answer as model-only and ask for updated data files or odds.
