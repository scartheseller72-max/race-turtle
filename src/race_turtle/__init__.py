"""race_turtle — a small, friendly turtle racing game.

Six turtles race across the screen while two players bet on who will win.
Originally a beginner project ("a racing game for my son"); refactored into a
clean, testable package with a pure simulation core (:mod:`race_turtle.engine`)
kept strictly separate from the optional ``turtle`` rendering layer
(:mod:`race_turtle.game`).
"""

from __future__ import annotations

from .bets import Bet, parse_bet, winners
from .engine import RaceEngine
from .models import Racer, RaceResult

__all__ = [
    "Bet",
    "RaceEngine",
    "RaceResult",
    "Racer",
    "parse_bet",
    "winners",
]

__version__ = "1.0.0"
