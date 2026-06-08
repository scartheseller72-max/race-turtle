"""Tests for bet parsing and resolution."""

from __future__ import annotations

import random

import pytest

from race_turtle.bets import Bet, normalize_color, parse_bet, winners
from race_turtle.config import DEFAULT_COLORS
from race_turtle.engine import RaceEngine

ALLOWED = ("red", "green", "blue")


@pytest.mark.parametrize(
    "raw,expected",
    [("Red", "red"), ("  GREEN ", "green"), ("BLUE", "blue"), ("rEd", "red")],
)
def test_normalize_color(raw: str, expected: str) -> None:
    assert normalize_color(raw) == expected


def test_parse_bet_is_case_insensitive() -> None:
    bet = parse_bet("Alice", "  ReD ", ALLOWED)
    assert bet == Bet(player="Alice", color="red")


@pytest.mark.parametrize("bad", ["", "   ", "magenta", "rainbow"])
def test_parse_bet_rejects_invalid(bad: str) -> None:
    with pytest.raises(ValueError):
        parse_bet("Bob", bad, ALLOWED)


def test_winners_matches_case_insensitively() -> None:
    bets = [Bet("son", "red"), Bet("dad", "blue")]
    assert winners("RED", bets) == ("son",)
    assert winners("green", bets) == ()


def test_winners_supports_multiple_correct_players() -> None:
    bets = [Bet("a", "red"), Bet("b", "red"), Bet("c", "blue")]
    assert winners("red", bets) == ("a", "b")


def test_correct_bet_is_credited_end_to_end() -> None:
    """The original bug: a correct guess scored as a loss. Guard against it."""
    engine = RaceEngine(DEFAULT_COLORS, rng=random.Random(5))
    engine.run()
    winning_color = engine.winner
    assert winning_color is not None
    # A player who bet (in mixed case) on the winning colour must be credited.
    bet = parse_bet("son", winning_color.upper(), DEFAULT_COLORS)
    result = engine.result([bet])
    assert result.correct_players == ("son",)
    assert result.anyone_won
