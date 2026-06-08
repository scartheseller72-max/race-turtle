"""Tests for the headless race engine."""

from __future__ import annotations

import random

import pytest

from race_turtle.config import DEFAULT_COLORS
from race_turtle.engine import RaceEngine
from race_turtle.models import RaceResult


def make_engine(seed: int = 0, **kwargs) -> RaceEngine:
    return RaceEngine(DEFAULT_COLORS, rng=random.Random(seed), **kwargs)


def test_race_finishes_and_reports_a_valid_winner() -> None:
    engine = make_engine(seed=42)
    result = engine.run()
    assert isinstance(result, RaceResult)
    assert engine.finished
    assert result.winner in DEFAULT_COLORS
    assert result.steps > 0


def test_same_seed_is_deterministic() -> None:
    a = make_engine(seed=7).run()
    b = make_engine(seed=7).run()
    assert a.winner == b.winner
    assert a.steps == b.steps
    assert a.standings == b.standings


def test_different_seeds_can_diverge() -> None:
    winners = {make_engine(seed=s).run().winner for s in range(25)}
    # With 6 colours and 25 seeds we expect more than a single outcome.
    assert len(winners) > 1


def test_positions_are_monotonic_non_decreasing() -> None:
    engine = make_engine(seed=3)
    last = {r.color: 0.0 for r in engine.racers}
    while not engine.finished:
        engine.step()
        for racer in engine.racers:
            assert racer.position >= last[racer.color]
            last[racer.color] = racer.position


def test_standings_sorted_leader_first() -> None:
    result = make_engine(seed=11).run()
    positions = [pos for _, pos in result.standings]
    assert positions == sorted(positions, reverse=True)
    assert result.standings[0][0] == result.winner


def test_step_after_finish_is_noop() -> None:
    engine = make_engine(seed=1)
    engine.run()
    steps_before = engine.steps
    assert engine.step() == ()
    assert engine.steps == steps_before


def test_result_before_finish_raises() -> None:
    engine = make_engine(seed=1)
    with pytest.raises(RuntimeError):
        engine.result()


@pytest.mark.parametrize(
    "kwargs",
    [
        {"colors": ("red",)},
        {"colors": ("red", "red")},
        {"track_length": 0},
        {"max_step": 0},
    ],
)
def test_invalid_construction_raises(kwargs) -> None:
    colors = kwargs.pop("colors", DEFAULT_COLORS)
    with pytest.raises(ValueError):
        RaceEngine(colors, **kwargs)


def test_winner_has_crossed_the_line() -> None:
    engine = make_engine(seed=99, track_length=200)
    result = engine.run()
    winning_racer = next(r for r in engine.racers if r.color == result.winner)
    assert winning_racer.position >= engine.track_length
