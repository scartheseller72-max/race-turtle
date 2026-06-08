"""Headless race simulation.

This is the heart of the game and has **no** dependency on ``turtle`` or any
display, so it can be unit-tested deterministically by injecting a seeded
:class:`random.Random`. The GUI layer drives this engine one ``step`` at a time
and mirrors each racer's ``position`` onto the screen.
"""

from __future__ import annotations

import random
from collections.abc import Sequence

from .bets import Bet, winners
from .config import DEFAULT_COLORS, MAX_STEP, TRACK_LENGTH
from .models import Racer, RaceResult

#: A single tick's movement: (racer, distance advanced this tick).
Move = tuple[Racer, int]


class RaceEngine:
    """A deterministic, lockstep race over a fixed-length track."""

    def __init__(
        self,
        colors: Sequence[str] = DEFAULT_COLORS,
        *,
        track_length: float = TRACK_LENGTH,
        max_step: int = MAX_STEP,
        rng: random.Random | None = None,
    ) -> None:
        if len(colors) < 2:
            raise ValueError("a race needs at least two racers")
        if len(set(colors)) != len(colors):
            raise ValueError("racer colours must be unique")
        if track_length <= 0:
            raise ValueError("track_length must be positive")
        if max_step <= 0:
            raise ValueError("max_step must be positive")

        self.track_length: float = float(track_length)
        self.max_step: int = int(max_step)
        self._rng: random.Random = rng if rng is not None else random.Random()
        self.racers: list[Racer] = [
            Racer(color=color, lane=lane) for lane, color in enumerate(colors)
        ]
        self._steps: int = 0
        self._winner: str | None = None

    @property
    def finished(self) -> bool:
        """True once a racer has crossed the finish line."""
        return self._winner is not None

    @property
    def winner(self) -> str | None:
        """The winning colour, or ``None`` while the race is in progress."""
        return self._winner

    @property
    def steps(self) -> int:
        """Number of ticks elapsed."""
        return self._steps

    def step(self) -> tuple[Move, ...]:
        """Advance every racer by one tick.

        Returns the per-racer movements for this tick (empty once finished).
        If multiple racers cross on the same tick, the one that travelled
        furthest is declared the winner.
        """
        if self.finished:
            return ()
        self._steps += 1
        moves: list[Move] = []
        for racer in self.racers:
            distance = self._rng.randint(0, self.max_step)
            racer.advance(distance)
            moves.append((racer, distance))

        crossed = [r for r in self.racers if r.position >= self.track_length]
        if crossed:
            self._winner = max(crossed, key=lambda r: r.position).color
        return tuple(moves)

    def standings(self) -> tuple[tuple[str, float], ...]:
        """Current leaderboard as ``(color, position)`` sorted leader-first."""
        ordered = sorted(self.racers, key=lambda r: r.position, reverse=True)
        return tuple((r.color, r.position) for r in ordered)

    def run(self, bets: Sequence[Bet] | None = None) -> RaceResult:
        """Run to completion and return the :class:`RaceResult`."""
        while not self.finished:
            self.step()
        return self.result(bets)

    def result(self, bets: Sequence[Bet] | None = None) -> RaceResult:
        """Build the result for a finished race.

        Raises:
            RuntimeError: if called before the race has finished.
        """
        if self._winner is None:
            raise RuntimeError("the race has not finished yet")
        correct = winners(self._winner, bets) if bets else ()
        return RaceResult(
            winner=self._winner,
            steps=self._steps,
            standings=self.standings(),
            correct_players=correct,
        )
