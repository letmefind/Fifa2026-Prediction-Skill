from __future__ import annotations

from data.team_aliases import fixture_pair_key, normalize_team_name, teams_match


def test_normalize_fifa_team_names() -> None:
    assert normalize_team_name("IR Iran") == "Iran"
    assert normalize_team_name("Korea Republic") == "South Korea"
    assert normalize_team_name("United States") == "USA"
    assert normalize_team_name("Türkiye") == "Turkey"
    assert normalize_team_name("Cabo Verde") == "Cape Verde"
    assert normalize_team_name("DR Congo") == "Congo DR"


def test_teams_match_across_aliases() -> None:
    assert teams_match("United States", "USA")
    assert teams_match("IR Iran", "Iran")
    assert fixture_pair_key("Spain", "Saudi Arabia") == fixture_pair_key("Saudi Arabia", "ESP")
