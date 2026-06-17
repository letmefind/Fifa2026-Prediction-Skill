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
2. Ask the user how many simulation runs to use. If no number is provided, use `5000`.
3. Verify current data access and check latest scores/results at calculation time. If unavailable, disclose the limitation and ask for current data files, latest scores, or permission to proceed with a model-only forecast.
4. Run `.venv/bin/python -m cli.main simulate-tournament --runs 5000`, replacing `5000` with the user-selected run count.
5. Run match-level predictions for the assumed or official fixture list.
6. Compare model probabilities to available market odds.
7. Produce the full report with numerical uncertainty and clear assumptions.
