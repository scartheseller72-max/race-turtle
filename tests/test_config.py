"""Tests for configuration helpers and invariants."""

from __future__ import annotations

import pytest

from race_turtle import config


def test_default_colors_are_unique() -> None:
    assert len(set(config.DEFAULT_COLORS)) == len(config.DEFAULT_COLORS)


def test_default_colors_has_six_racers() -> None:
    assert len(config.DEFAULT_COLORS) == 6


def test_lane_offsets_count_matches_request() -> None:
    offsets = config.lane_offsets(6)
    assert len(offsets) == 6


def test_lane_offsets_are_centered() -> None:
    offsets = config.lane_offsets(6)
    assert sum(offsets) == pytest.approx(0.0)


def test_lane_offsets_are_evenly_spaced() -> None:
    offsets = config.lane_offsets(4, spacing=50)
    gaps = [a - b for a, b in zip(offsets, offsets[1:])]
    assert all(gap == pytest.approx(50) for gap in gaps)


def test_lane_offsets_rejects_non_positive() -> None:
    with pytest.raises(ValueError):
        config.lane_offsets(0)


def test_start_is_left_of_finish() -> None:
    assert config.start_x() < config.finish_x()
