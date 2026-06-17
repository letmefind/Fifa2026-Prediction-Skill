from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BettingEdge:
    model_prob: float
    market_odds: float
    implied_prob: float
    expected_value: float
    edge: float
    label: str

    def as_dict(self) -> dict[str, float | str]:
        return self.__dict__.copy()


def calculate_ev(model_prob: float, market_odds: float) -> BettingEdge:
    if not 0 <= model_prob <= 1:
        raise ValueError("model_prob must be between 0 and 1")
    if market_odds <= 1:
        raise ValueError("market_odds must be decimal odds greater than 1")

    implied_prob = 1.0 / market_odds
    expected_value = model_prob * (market_odds - 1.0) - (1.0 - model_prob)
    edge = model_prob - implied_prob
    if expected_value > 0.02:
        label = "undervalued"
    elif expected_value < -0.02:
        label = "overvalued"
    else:
        label = "fair"
    return BettingEdge(
        model_prob=float(model_prob),
        market_odds=float(market_odds),
        implied_prob=float(implied_prob),
        expected_value=float(expected_value),
        edge=float(edge),
        label=label,
    )
