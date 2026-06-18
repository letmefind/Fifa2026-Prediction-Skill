#!/usr/bin/env python3
"""Generate tournament simulation + match-day PNG reports and JSON data."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from api.service import refresh_service  # noqa: E402

RUNS = 50_000
BG = "#07111f"
PANEL = "#0f1a2e"
TEXT = "#f5f7fb"
MUTED = "#9fb0c7"
ACCENT = "#31d0aa"
ACCENT2 = "#63a4ff"
LINE = "#2a3a52"


def _pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def _odds(prob: float) -> str:
    if prob <= 0:
        return "—"
    return f"{1 / prob:.2f}"


def save_figure(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG, edgecolor="none")
    plt.close(fig)


def render_tournament_table(probabilities: list[dict], runs: int, out_path: Path) -> None:
    rows = probabilities
    n = len(rows)
    fig_h = max(14, 0.32 * n + 3)
    fig, ax = plt.subplots(figsize=(14, fig_h), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis("off")

    title = f"FIFA World Cup 2026 — Tournament Simulation ({runs:,} runs)"
    subtitle = f"Data as of {date.today().isoformat()} · ELO + Dixon-Coles Poisson · Official FIFA groups"
    fig.text(0.5, 0.98, title, ha="center", va="top", fontsize=18, fontweight="bold", color=TEXT)
    fig.text(0.5, 0.965, subtitle, ha="center", va="top", fontsize=10, color=MUTED)

    headers = ["Rank", "Team", "Win WC", "Reach Final", "Reach Semis", "Round of 32"]
    col_x = [0.04, 0.10, 0.52, 0.64, 0.76, 0.88]
    y = 0.92
    for header, x in zip(headers, col_x):
        ax.text(x, y, header, fontsize=9, fontweight="bold", color=ACCENT, transform=ax.transAxes)

    for i, row in enumerate(rows):
        y = 0.905 - i * (0.86 / n)
        bg = PANEL if i % 2 == 0 else BG
        rect = mpatches.FancyBboxPatch(
            (0.02, y - 0.012), 0.96, 0.86 / n - 0.004,
            boxstyle="round,pad=0.002", linewidth=0,
            facecolor=bg, transform=ax.transAxes, zorder=0,
        )
        ax.add_patch(rect)
        values = [
            str(i + 1),
            str(row["team"]),
            _pct(float(row["win_world_cup"])),
            _pct(float(row["reach_final"])),
            _pct(float(row["reach_semis"])),
            _pct(float(row["round_of_32"])),
        ]
        weights = ["normal", "bold", "normal", "normal", "normal", "normal"]
        colors = [MUTED, TEXT, TEXT, TEXT, TEXT, MUTED]
        for val, x, w, c in zip(values, col_x, weights, colors):
            ax.text(x, y, val, fontsize=8.5, fontweight=w, color=c, transform=ax.transAxes, va="center")

    legend = "Round of 32 = probability of qualifying for knockout stage (top 2 per group + 8 best 3rd)"
    fig.text(0.5, 0.02, legend, ha="center", fontsize=8, color=MUTED)
    save_figure(fig, out_path)


def render_match_day(matches_data: dict, out_path: Path) -> None:
    matches = matches_data["matches"]
    n = len(matches)
    fig_h = max(8, 2.2 + n * 1.35)
    fig, ax = plt.subplots(figsize=(16, fig_h), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis("off")

    d = matches_data["date"]
    fig.text(0.5, 0.97, f"Match Day Predictions — {d}", ha="center", fontsize=18, fontweight="bold", color=TEXT)
    fig.text(
        0.5, 0.94,
        f"{n} matches · Model win/draw/loss % and decimal odds · {date.today().isoformat()}",
        ha="center", fontsize=10, color=MUTED,
    )

    headers = ["Grp", "Match", "Score", "Win A", "Draw", "Win B", "Odds A", "Odds D", "Odds B", "xG"]
    col_x = [0.03, 0.08, 0.38, 0.52, 0.58, 0.64, 0.70, 0.76, 0.82, 0.90]
    y0 = 0.88
    for header, x in zip(headers, col_x):
        ax.text(x, y0, header, fontsize=8, fontweight="bold", color=ACCENT, transform=ax.transAxes)

    for i, m in enumerate(matches):
        y = y0 - 0.04 - i * (0.82 / max(n, 1))
        bg = PANEL if i % 2 == 0 else BG
        rect = mpatches.FancyBboxPatch(
            (0.02, y - 0.025), 0.96, 0.82 / max(n, 1) - 0.01,
            boxstyle="round,pad=0.002", linewidth=0,
            facecolor=bg, transform=ax.transAxes, zorder=0,
        )
        ax.add_patch(rect)
        status = str(m.get("status", ""))
        score = str(m.get("score", "—"))
        xg = (
            f"{float(m['expected_goals_a']):.2f}-{float(m['expected_goals_b']):.2f}"
            if m.get("expected_goals_a") is not None else "—"
        )
        match_label = f"{m['team_a']} vs {m['team_b']}"
        if status == "played":
            match_label += " ✓"
        vals = [
            str(m["group"]),
            match_label,
            score,
            _pct(float(m["win_prob_a"])),
            _pct(float(m["draw_prob"])),
            _pct(float(m["win_prob_b"])),
            f"{float(m['decimal_odds_a']):.2f}",
            f"{float(m['decimal_odds_draw']):.2f}",
            f"{float(m['decimal_odds_b']):.2f}",
            xg,
        ]
        for val, x in zip(vals, col_x):
            color = ACCENT if x == col_x[2] and status == "played" else TEXT
            ax.text(x, y, val, fontsize=8, color=color, transform=ax.transAxes, va="center")

    save_figure(fig, out_path)


def render_round_of_32(r32_matches: list[dict], champion: str, out_path: Path) -> None:
    n = len(r32_matches)
    fig_h = max(10, 2.5 + n * 0.72)
    fig, ax = plt.subplots(figsize=(15, fig_h), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis("off")

    fig.text(0.5, 0.97, "Projected Round of 32 — Model Predictions & Odds", ha="center", fontsize=18, fontweight="bold", color=TEXT)
    fig.text(
        0.5, 0.94,
        f"16 knockout matches (32 teams) · Based on group-stage projections · Projected champion: {champion}",
        ha="center", fontsize=10, color=ACCENT,
    )

    headers = ["#", "Match", "Pred. Score", "Winner", "Win A", "Draw", "Win B", "Odds A", "Odds D", "Odds B"]
    col_x = [0.03, 0.07, 0.34, 0.50, 0.60, 0.66, 0.72, 0.78, 0.84, 0.90]
    y0 = 0.90
    for header, x in zip(headers, col_x):
        ax.text(x, y0, header, fontsize=8, fontweight="bold", color=ACCENT, transform=ax.transAxes)

    for i, m in enumerate(r32_matches):
        y = y0 - 0.035 - i * (0.85 / max(n, 1))
        bg = PANEL if i % 2 == 0 else BG
        rect = mpatches.FancyBboxPatch(
            (0.02, y - 0.02), 0.96, 0.85 / max(n, 1) - 0.008,
            boxstyle="round,pad=0.002", linewidth=0,
            facecolor=bg, transform=ax.transAxes, zorder=0,
        )
        ax.add_patch(rect)
        wa = float(m["win_prob_a"])
        wd = float(m["draw_prob"])
        wb = float(m["win_prob_b"])
        vals = [
            str(i + 1),
            f"{m['team_a']} vs {m['team_b']}",
            str(m["predicted_score"]),
            str(m["winner"]),
            _pct(wa),
            _pct(wd),
            _pct(wb),
            _odds(wa),
            _odds(wd),
            _odds(wb),
        ]
        for val, x in zip(vals, col_x):
            color = ACCENT if x == col_x[3] else TEXT
            ax.text(x, y, val, fontsize=8, color=color, transform=ax.transAxes, va="center")

    save_figure(fig, out_path)


def main() -> None:
    print("Refreshing latest data and rebuilding model...")
    service = refresh_service()

    today = date.today()
    date_str = today.strftime("%d %b").lower().lstrip("0")
    alt_date = today.strftime("%d %b").replace(" 0", " ").lower()

    print(f"Running {RUNS:,} tournament simulations (this may take a minute)...")
    sim = service.simulate_tournament(n=RUNS)

    print(f"Fetching match-day predictions for {today.isoformat()}...")
    try:
        day = service.predictions_by_date(alt_date)
    except ValueError:
        day = service.predictions_by_date(date_str)

    print("Building group-stage knockout projection...")
    groups = service.group_stage_predictions()
    knockout = groups["knockout_projection"]
    r32 = knockout["round_of_32"]
    champion = str(knockout["champion"])

    stamp = today.isoformat()
    out_dir = ROOT / "docs" / "screenshots" / stamp
    out_dir.mkdir(parents=True, exist_ok=True)

    tournament_png = out_dir / f"tournament-simulation-{RUNS}-runs.png"
    matchday_png = out_dir / f"match-day-{stamp}.png"
    r32_png = out_dir / f"round-of-32-predictions-{stamp}.png"
    json_path = out_dir / f"report-{stamp}.json"

    print("Rendering images...")
    render_tournament_table(sim["probabilities"], RUNS, tournament_png)
    render_match_day(day, matchday_png)
    render_round_of_32(r32, champion, r32_png)

    report = {
        "generated": stamp,
        "simulation_runs": RUNS,
        "latest_status": service.latest_status(),
        "tournament_probabilities": sim["probabilities"],
        "match_day": day,
        "round_of_32": r32,
        "knockout_champion_projection": champion,
        "images": {
            "tournament": str(tournament_png.relative_to(ROOT)),
            "match_day": str(matchday_png.relative_to(ROOT)),
            "round_of_32": str(r32_png.relative_to(ROOT)),
        },
    }
    json_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")

    print(f"\nSaved:\n  {tournament_png}\n  {matchday_png}\n  {r32_png}\n  {json_path}")
    print("\nTop 10 World Cup title odds:")
    for row in sim["probabilities"][:10]:
        print(f"  {row['team']:20s} {_pct(float(row['win_world_cup']))}")


if __name__ == "__main__":
    main()
