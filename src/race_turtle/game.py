"""Interactive ``turtle`` rendering layer.

This module is the only part of the package that imports :mod:`turtle`, and it
is imported lazily by the CLI so headless environments (CI, tests) never need a
display. It owns the screen, prompts the two players for their bets, and
animates the :class:`~race_turtle.engine.RaceEngine` tick by tick.
"""

from __future__ import annotations

import random
from collections.abc import Sequence

from . import config
from .bets import Bet, parse_bet
from .engine import RaceEngine


class TurtleRace:
    """Drives a :class:`RaceEngine` and draws it with ``turtle`` graphics."""

    def __init__(
        self,
        colors: Sequence[str] = config.DEFAULT_COLORS,
        *,
        players: Sequence[str] = ("My son", "Me"),
        seed: int | None = None,
        track_length: float = config.TRACK_LENGTH,
        max_step: int = config.MAX_STEP,
    ) -> None:
        self.colors = tuple(colors)
        self.players = tuple(players)
        self.engine = RaceEngine(
            self.colors,
            track_length=track_length,
            max_step=max_step,
            rng=random.Random(seed),
        )
        # Imported here so module import never requires Tk.
        from turtle import Screen, Turtle

        self._Turtle = Turtle
        self.screen: Screen = Screen()
        self._lanes = config.lane_offsets(len(self.colors))
        self._start_x = config.start_x()
        self._finish_x = config.finish_x()
        self._span = self._finish_x - self._start_x
        self._turtles: dict[str, Turtle] = {}

    # -- setup ---------------------------------------------------------------
    def setup_screen(self) -> None:
        self.screen.setup(width=config.SCREEN_WIDTH, height=config.SCREEN_HEIGHT)
        self.screen.title(config.SCREEN_TITLE)
        self._draw_finish_line()
        self._build_turtles()

    def _draw_finish_line(self) -> None:
        marker = self._Turtle(visible=False)
        marker.speed("fastest")
        marker.penup()
        marker.color("gray")
        marker.goto(self._finish_x, config.SCREEN_HEIGHT // 2)
        marker.setheading(270)
        marker.pendown()
        marker.forward(config.SCREEN_HEIGHT)
        marker.penup()

    def _build_turtles(self) -> None:
        for racer, lane_y in zip(self.engine.racers, self._lanes):
            t = self._Turtle(shape=config.TURTLE_SHAPE)
            t.color(racer.color)
            t.penup()
            t.goto(self._start_x, lane_y)
            self._turtles[racer.color] = t

    # -- input ---------------------------------------------------------------
    def prompt_bets(self) -> list[Bet]:
        """Ask each player to pick a colour, re-prompting on invalid input.

        Returns an empty list if any player cancels the dialog.
        """
        bets: list[Bet] = []
        for player in self.players:
            while True:
                raw = self.screen.textinput(
                    title=f"{player}'s bet",
                    prompt=f"Which colour will win?\nChoices: {', '.join(self.colors)}",
                )
                if raw is None:  # dialog cancelled
                    return []
                try:
                    bets.append(parse_bet(player, raw, self.colors))
                    break
                except ValueError:
                    continue
        return bets

    # -- animation -----------------------------------------------------------
    def _screen_x(self, position: float) -> float:
        fraction = min(position / self.engine.track_length, 1.0)
        return self._start_x + fraction * self._span

    def _render(self) -> None:
        for racer in self.engine.racers:
            self._turtles[racer.color].goto(
                self._screen_x(racer.position),
                self._turtles[racer.color].ycor(),
            )

    def run(self) -> str | None:
        """Set up, take bets, animate the race and announce the result.

        Returns the winning colour, or ``None`` if the race never started.
        """
        self.setup_screen()
        bets = self.prompt_bets()
        if not bets:
            self.screen.bye()
            return None

        while not self.engine.finished:
            self.engine.step()
            self._render()

        result = self.engine.result(bets)
        self._announce(result)
        self.screen.exitonclick()
        return result.winner

    def _announce(self, result) -> None:
        banner = self._Turtle(visible=False)
        banner.penup()
        banner.color("black")
        banner.goto(0, config.SCREEN_HEIGHT // 2 - 40)
        if result.correct_players:
            who = " & ".join(result.correct_players)
            message = f"{who} won! The {result.winner} turtle is the winner."
        else:
            message = f"Nobody guessed it — the {result.winner} turtle won!"
        banner.write(message, align="center", font=("Arial", 16, "bold"))
