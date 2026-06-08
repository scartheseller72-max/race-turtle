"""Static configuration and tunable constants for the race.

Everything that used to be a magic number scattered through ``main.py`` lives
here, so gameplay can be tuned in one place and the rest of the code reads
declaratively.
"""

from __future__ import annotations

#: Default field of racers, in lane order (top -> bottom on screen).
#: All names are valid Tk/``turtle`` colour names.
DEFAULT_COLORS: tuple[str, ...] = (
    "red",
    "orange",
    "yellow",
    "green",
    "blue",
    "purple",
)

#: Distance (in turtle steps) a racer must travel to cross the finish line.
TRACK_LENGTH: float = 400.0

#: Maximum distance a racer can advance on a single tick (inclusive, >= 0).
MAX_STEP: int = 10

#: Drawing surface.
SCREEN_WIDTH: int = 560
SCREEN_HEIGHT: int = 480
SCREEN_TITLE: str = "Race Turtle"

#: Vertical gap between adjacent lanes, in pixels.
LANE_SPACING: int = 60

#: Horizontal margin (px) between the screen edge and the start / finish lines.
EDGE_MARGIN: int = 30

#: ``turtle`` shape used for every racer.
TURTLE_SHAPE: str = "turtle"


def start_x(width: int = SCREEN_WIDTH, margin: int = EDGE_MARGIN) -> int:
    """Return the x coordinate of the starting line."""
    return -(width // 2) + margin


def finish_x(width: int = SCREEN_WIDTH, margin: int = EDGE_MARGIN) -> int:
    """Return the x coordinate of the finish line."""
    return (width // 2) - margin


def lane_offsets(count: int, spacing: int = LANE_SPACING) -> tuple[float, ...]:
    """Return vertically-centred y offsets for ``count`` lanes.

    Lanes are distributed symmetrically around ``y = 0`` so the field stays
    centred regardless of how many racers take part.
    """
    if count <= 0:
        raise ValueError("count must be a positive integer")
    top = (count - 1) / 2.0
    return tuple((top - lane) * spacing for lane in range(count))
