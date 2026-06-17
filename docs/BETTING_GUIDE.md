# Betting and Prediction Market Guide

This guide explains how to use the FIFA 2026 prediction engine for Polymarket, Betfair Exchange, Pinnacle, Bet365, or similar betting/forecast markets.

This is analytical software, not financial advice. Betting and prediction markets involve risk. Only use legal platforms in your jurisdiction, understand platform rules, and never stake money you cannot afford to lose.

## Core Idea

The engine produces a model probability. Markets produce a market-implied probability. A possible betting edge exists when:

```text
model probability > market-implied probability + safety margin
```

Example:

```text
Model says Brazil win probability = 55%
Market implies Brazil win probability = 45.5%
Estimated edge = 9.5 percentage points
```

Run:

```bash
python -m cli.main betting-edge 0.55 2.20
```

Output:

```text
Model probability: 55.0%
Market odds: 2.20
Implied probability: 45.5%
Expected value: 0.210
Edge: 9.5%
Label: undervalued
```

## Polymarket: Convert Price to Probability

Polymarket usually trades event contracts as `Yes`/`No` shares.

If a `Yes` share costs `$0.42`, the market roughly implies:

```text
42% probability
```

If your model probability is `50%`, then:

```text
model probability = 0.50
market probability = 0.42
edge = 0.08
```

Approximate decimal odds from a Polymarket price:

```text
decimal odds = 1 / price
```

Example:

```text
Polymarket Yes price = 0.42
decimal odds = 1 / 0.42 = 2.38
```

Run:

```bash
python -m cli.main betting-edge 0.50 2.38
```

Interpretation:

- If EV is positive, the `Yes` share may be undervalued by the market.
- If EV is negative, the `Yes` share may be overvalued.
- Include fees, spread, slippage, liquidity, and resolution risk before acting.

## Sportsbooks: Convert Odds to Probability

Decimal odds:

```text
implied probability = 1 / decimal odds
```

Examples:

```text
2.00 odds = 50.0%
2.50 odds = 40.0%
1.67 odds = 59.9%
```

American odds conversion:

```text
Positive odds +150: decimal = 1 + (150 / 100) = 2.50
Negative odds -150: decimal = 1 + (100 / 150) = 1.67
```

Fractional odds conversion:

```text
3/2 fractional = 1 + (3 / 2) = 2.50 decimal
```

## Workflow: Match Betting

1. Run a model prediction:

```bash
python -m cli.main predict-match Brazil France
```

2. Read the probabilities:

```text
Brazil win: 35.6%
Draw: 30.4%
France win: 34.0%
```

3. Compare each outcome to market odds.

Example market:

```text
Brazil win odds: 3.20
Draw odds: 3.10
France win odds: 2.70
```

4. Calculate EV for each outcome:

```bash
python -m cli.main betting-edge 0.356 3.20
python -m cli.main betting-edge 0.304 3.10
python -m cli.main betting-edge 0.340 2.70
```

5. Only consider bets where:

- EV is positive after fees and spreads
- edge is large enough to survive model error
- market liquidity is acceptable
- team news does not contradict the model

## Workflow: Futures Markets

For World Cup winner, finalist, semifinal, or group qualification markets:

```bash
python -m cli.main simulate-tournament --runs 50000
python -m cli.main team-probabilities Brazil --runs 50000
```

Compare model probabilities to futures prices:

```text
Model says Brazil win World Cup = 12%
Polymarket Brazil Yes price = 8%
Edge = 4 percentage points
```

Approximate odds:

```text
decimal odds = 1 / 0.08 = 12.50
```

Run:

```bash
python -m cli.main betting-edge 0.12 12.50
```

## What Counts as a Real Edge?

Avoid betting tiny edges. Sports models are noisy.

Suggested minimum edge thresholds:

```text
High-liquidity match market: 3-5 percentage points
Lower-liquidity futures market: 5-10 percentage points
Longshot/dark horse market: 10+ percentage points
```

Raise the threshold when:

- data is old
- injuries are uncertain
- squads are not final
- market liquidity is low
- bid/ask spread is wide
- resolution rules are unclear

## Bankroll and Position Sizing

Use conservative staking. A simple approach:

```text
Small edge: 0.25% to 0.50% of bankroll
Medium edge: 0.50% to 1.00% of bankroll
Large edge: 1.00% to 2.00% of bankroll
```

Avoid staking full Kelly. If using Kelly sizing, consider quarter-Kelly or less because football outcomes are high variance and model error can be large.

## Before Placing a Bet

Check:

- latest injuries and suspensions
- confirmed lineups when available
- rest days and travel
- venue, altitude, heat, humidity
- manager rotation risk
- market liquidity and spread
- platform fees
- event resolution rules
- whether your model data is current

## Common Mistakes

- Treating sample data as current data.
- Betting because the model favorite is likely to win, not because the price has value.
- Ignoring draw probability in football.
- Ignoring bookmaker margin or Polymarket spread.
- Overbetting longshots because EV looks large on stale prices.
- Comparing model probability to public opinion instead of actual market price.

## Best Use

Use this engine as a probability calculator and decision-support tool:

```text
Model probability -> market probability -> EV -> risk checks -> stake decision
```

The goal is not to bet the team most likely to win. The goal is to find prices where the market probability is lower than your best estimate of true probability.
