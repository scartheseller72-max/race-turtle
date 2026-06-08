"""Bet parsing and resolution.

The original game compared raw dialog strings directly, so ``"Red"`` never
matched the racer colour ``"red"`` and a correct guess was scored as a loss.
This module normalises and validates bets, fixing that class of bug.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Bet:
    """A player's wager on a colour. ``color`` is always normalised."""

    player: str
    color: str


def normalize_color(value: str) -> str:
    """Canonicalise a colour string for comparison (trim + lowercase)."""
    return value.strip().lower()


def parse_bet(player: str, raw_color: str, allowed: Iterable[str]) -> Bet:
    """Validate ``raw_color`` against ``allowed`` and build a :class:`Bet`.

    Raises:
        ValueError: if the colour is empty or not among ``allowed``.
    """
    color = normalize_color(raw_color)
    if not color:
        raise ValueError("a colour is required")
    allowed_set = {normalize_color(c) for c in allowed}
    if color not in allowed_set:
        choices = ", ".join(sorted(allowed_set))
        raise ValueError(f"{raw_color!r} is not a racer colour. Choose one of: {choices}")
    return Bet(player=player, color=color)


def winners(winning_color: str, bets: Iterable[Bet]) -> tuple[str, ...]:
    """Return the names of players whose bet matches ``winning_color``."""
    target = normalize_color(winning_color)
    return tuple(bet.player for bet in bets if bet.color == target)
