# Full Tournament Prediction Workflow

Use this reference when the user asks for a Gemini-style full FIFA World Cup 2026 prediction, all 104 matches, country-by-country reality, current 2025-2026 data, betting value, dark horses, or a complete tournament report.

## Core Rule

Do not present sample-data outputs as final real-world predictions. For highest accuracy, combine:

- current squad and player data
- injuries, suspensions, fitness, and minutes
- manager/tactical context
- recent form and xG
- market odds
- the Python engine's probabilities and simulations

If current web access, odds access, or player databases are unavailable, say exactly what is missing and produce a clearly labeled model-only forecast.

## Phase 1: Build Current Inputs

For each qualified or projected team, collect:

- expected squad and starting XI
- club, position, age, minutes, goals, assists, xG, xA for expected starters
- injuries, fitness, suspension risk, and likely availability
- goalkeeper, defense, midfield, attack, bench depth
- manager quality, tactical flexibility, substitutions, tournament experience
- last 20, last 10, and last 5 match form
- goals for, goals against, clean sheets, average xG, average xGA
- World Cup, continental, knockout, and penalty history

Prefer recent club and international performance data over reputation or FIFA ranking.

## Phase 2: Create Team Ratings

Create a 0-100 score for each category:

- Offensive Strength: goals, xG, shot creation, set pieces, finishing
- Defensive Strength: goals conceded, xGA, pressing, structure, goalkeeping
- Midfield Control: possession, progressive passing, recoveries, press resistance
- Tournament Resilience: experience, depth, injury tolerance, mentality
- Travel/Home Adjustment: USA/Canada/Mexico venues, climate, altitude, travel, time zones

Penalize aging squads, injury-prone key players, weak bench depth, tactical rigidity, poor recent xG, and travel/climate disadvantages.

Reward squad depth, elite chance creation, strong goalkeeping, tactical flexibility, and recent underlying performance.

## Phase 3: Run Model Baselines

Run these commands:

```bash
.venv/bin/python -m cli.main simulate-tournament --runs 100000
.venv/bin/python -m cli.main team-probabilities Brazil --runs 100000
.venv/bin/python -m cli.main predict-match Brazil France --llm-prompt
```

If 100,000 runs are too slow, run 50,000 and disclose the lower run count.

Use model output as the quantitative baseline. Adjust only when the current-data research gives a clear reason, such as major injury news, squad rotation, travel disadvantage, or market movement.

## Phase 4: Group Stage Forecast

For every group:

- predict every group match score
- include win/draw/loss probabilities and expected goals
- give a confidence level: Low, Medium, or High
- produce the final table with `Team`, `Pts`, `W`, `D`, `L`, `GF`, `GA`, `GD`
- identify group winner, runner-up, third place, and eliminated team

When official groups or fixtures are unavailable, state the assumed draw/fixture structure before forecasting.

## Phase 5: Third-Place Ranking

Rank all 12 third-place teams by:

- points
- goal difference
- goals scored
- model team strength

Select the best 8 and explain close calls numerically.

## Phase 6: Knockout Bracket

Predict:

- Round of 32
- Round of 16
- Quarterfinals
- Semifinals
- Third-place match
- Final

For every knockout match include score, winner, xG, tactical reason, and confidence. For draws after regulation, identify extra-time or penalty winner.

## Phase 7: Betting Market Validation

Compare model probabilities against available market odds:

- Polymarket
- Bet365
- Pinnacle
- Betfair Exchange

Use decimal odds when possible. Calculate EV with:

```bash
.venv/bin/python -m cli.main betting-edge MODEL_PROB DECIMAL_ODDS
```

Classify:

- Undervalued: market price longer than model fair price
- Overvalued: market price shorter than model fair price
- Fair: no meaningful edge

Always account for bookmaker margin, exchange liquidity, stale odds, and model uncertainty.

For Polymarket, convert a `Yes` share price directly into approximate probability. A `Yes` price of `$0.42` means roughly `42%`; approximate decimal odds are `1 / 0.42 = 2.38`. Compare that implied probability to the model probability before identifying value.

Use the repository guide at `docs/BETTING_GUIDE.md` for the complete workflow.

## Phase 8: Risk Analysis

Identify:

- Black Swan Teams: low market probability, high upset potential
- Dark Horses: strong chance to outperform public expectation
- Collapse Candidates: strong reputation but elevated downside risk

Quantify uncertainty with probability ranges or confidence scores.

## Phase 9: Final Deliverable

Produce:

- predicted group tables
- full knockout bracket
- predicted scores for all 104 matches
- simulation probabilities for every team:
  - Round of 32
  - Round of 16
  - Quarterfinals
  - Semifinals
  - Final
  - Winner
- Golden Boot top 10
- Golden Ball top 10
- Best Goalkeeper
- Best Young Player
- winner, runner-up, semifinalists
- biggest surprise
- biggest disappointment
- confidence score from 0-100
- betting value shortlist

Keep calculations visible where possible. Do not hide uncertainty.

## Response Standard

Use concise tables for large outputs. For very long reports, start with an executive summary, then provide sections in phases. If the user asks for a machine-readable result, output JSON.
