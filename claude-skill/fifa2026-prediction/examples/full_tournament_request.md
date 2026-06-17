# Full Tournament Request Example

User request:

```text
Produce a full FIFA World Cup 2026 prediction using current 2025-2026 data.
Act as a football analytics department, sports bettor, xG statistician, scout,
predictive modeler, and tournament simulation specialist.

Include all qualified teams, squad quality, expected starters, injuries,
manager analysis, last 20/10/5 form, advanced team scores, match probabilities,
expected goals, all group tables, third-place ranking, full knockout bracket,
all 104 predicted scores, betting market validation, dark horses, collapse
candidates, Golden Boot, Golden Ball, best goalkeeper, best young player,
tournament winner, runner-up, semifinalists, and confidence score.
```

Skill behavior:

1. Read `FULL_TOURNAMENT_WORKFLOW.md`.
2. Verify current data access. If unavailable, disclose the limitation and ask for current data files or proceed with a model-only forecast.
3. Run `.venv/bin/python -m cli.main simulate-tournament --runs 100000`.
4. Run match-level predictions for the assumed or official fixture list.
5. Compare model probabilities to available market odds.
6. Produce the full report with numerical uncertainty and clear assumptions.
