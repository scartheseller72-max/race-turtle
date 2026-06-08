"""Plain data structures shared across the package.

These types carry no rendering or I/O concerns, which keeps them trivially
testable and reusable by both the headless engine and the GUI layer.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Racer:
    """A single competitor.

    ``position`` is measured in abstract track units (0 at the start line,
    :data:`race_turtle.config.TRACK_LENGTH` at the finish), decoupled from any
    pixel coordinate so the simulation can run without a display.
    """

    color: str
    lane: int
    position: float = 0.0

    def advance(self, distance: float) -> None:
        """Move the racer forward by ``distance`` units."""
        if distance < 0:
            raise ValueError("distance must be non-negative")
        self.position += distance


@dataclass(frozen=True)
class RaceResult:
    """Immutable summary of a finished race."""

    winner: str
    steps: int
    standings: tuple[tuple[str, float], ...]
    correct_players: tuple[str, ...] = ()

    @property
    def anyone_won(self) -> bool:
        """True if at least one player bet on the winning colour."""
        return bool(self.correct_players)
