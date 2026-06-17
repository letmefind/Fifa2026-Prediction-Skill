from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = ROOT / "config" / "default.yaml"


@dataclass(frozen=True)
class EloConfig:
    base_rating: float
    k_factor: float
    home_advantage: float


@dataclass(frozen=True)
class StrengthConfig:
    min_matches: int
    xg_weight: float
    goals_weight: float
    shrinkage_matches: int


@dataclass(frozen=True)
class PoissonConfig:
    base_goals_per_team: float
    max_goals: int
    home_advantage_multiplier: float
    dixon_coles_rho: float


@dataclass(frozen=True)
class ModelConfig:
    elo: EloConfig
    strengths: StrengthConfig
    poisson: PoissonConfig


@dataclass(frozen=True)
class SimulationConfig:
    default_runs: int
    random_seed: int
    knockout_draw_probability: float


@dataclass(frozen=True)
class DataConfig:
    cache_dir: Path
    matches_csv: Path
    ratings_csv: Path
    xg_csv: Path


@dataclass(frozen=True)
class Config:
    model: ModelConfig
    simulation: SimulationConfig
    data: DataConfig


def _path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def _merge_dict(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge_dict(merged[key], value)
        else:
            merged[key] = value
    return merged


@lru_cache(maxsize=8)
def load_config(path: str | Path | None = None) -> Config:
    with DEFAULT_CONFIG_PATH.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}

    if path is not None:
        with Path(path).open("r", encoding="utf-8") as handle:
            raw = _merge_dict(raw, yaml.safe_load(handle) or {})

    model = raw["model"]
    data = raw["data"]
    simulation = raw["simulation"]
    return Config(
        model=ModelConfig(
            elo=EloConfig(**model["elo"]),
            strengths=StrengthConfig(**model["strengths"]),
            poisson=PoissonConfig(**model["poisson"]),
        ),
        simulation=SimulationConfig(**simulation),
        data=DataConfig(
            cache_dir=_path(data["cache_dir"]),
            matches_csv=_path(data["matches_csv"]),
            ratings_csv=_path(data["ratings_csv"]),
            xg_csv=_path(data["xg_csv"]),
        ),
    )
