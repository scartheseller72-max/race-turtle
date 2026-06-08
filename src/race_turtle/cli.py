"""Command-line entry point.

Two modes:

* default (GUI) — opens a ``turtle`` window and plays interactively.
* ``--headless`` — runs the pure simulation and prints the result. Requires no
  display, so it is what CI exercises and what powers reproducible demos via
  ``--seed``.
"""

from __future__ import annotations

import argparse
import random
from collections.abc import Sequence

from . import __version__, config
from .bets import Bet, parse_bet
from .engine import RaceEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="race-turtle",
        description="A friendly turtle racing game. Bet on a colour and watch them go!",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="run without a GUI and print the result (no display required)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="seed the RNG for a reproducible race",
    )
    parser.add_argument(
        "--colors",
        nargs="+",
        metavar="COLOR",
        default=list(config.DEFAULT_COLORS),
        help="custom set of racer colours (>= 2, unique)",
    )
    parser.add_argument(
        "--bet",
        action="append",
        metavar="PLAYER=COLOR",
        default=[],
        help="headless bet, e.g. --bet 'My son=red' (repeatable)",
    )
    parser.add_argument(
        "--track-length",
        type=float,
        default=config.TRACK_LENGTH,
        help="distance a racer must cover to win",
    )
    parser.add_argument(
        "--max-step",
        type=int,
        default=config.MAX_STEP,
        help="maximum advance per tick",
    )
    return parser


def _parse_bets(specs: Sequence[str], colors: Sequence[str]) -> list[Bet]:
    bets: list[Bet] = []
    for spec in specs:
        if "=" not in spec:
            raise SystemExit(f"invalid --bet {spec!r}; expected PLAYER=COLOR")
        player, _, raw = spec.partition("=")
        try:
            bets.append(parse_bet(player.strip(), raw, colors))
        except ValueError as exc:
            raise SystemExit(f"invalid --bet {spec!r}: {exc}") from exc
    return bets


def _run_headless(args: argparse.Namespace) -> int:
    try:
        engine = RaceEngine(
            args.colors,
            track_length=args.track_length,
            max_step=args.max_step,
            rng=random.Random(args.seed),
        )
    except ValueError as exc:
        raise SystemExit(f"cannot start race: {exc}") from exc

    bets = _parse_bets(args.bet, args.colors)
    result = engine.run(bets)

    print(f"Finished in {result.steps} ticks.")
    print("Standings:")
    for rank, (color, position) in enumerate(result.standings, start=1):
        print(f"  {rank}. {color:<8} {position:6.1f}")
    print(f"Winner: {result.winner}")
    if bets:
        if result.correct_players:
            print(f"Correct bets: {', '.join(result.correct_players)}")
        else:
            print("Nobody guessed the winner.")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.headless:
        return _run_headless(args)

    # GUI mode: import lazily so headless use never needs Tk.
    from .game import TurtleRace

    TurtleRace(
        colors=args.colors,
        seed=args.seed,
        track_length=args.track_length,
        max_step=args.max_step,
    ).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
