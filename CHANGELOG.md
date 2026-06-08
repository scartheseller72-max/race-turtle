# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-08

The original single-file script became a clean, tested, packaged project while
keeping the same fun gameplay.

### Added
- `src/` layout package `race_turtle` split into focused modules: `config`,
  `models`, `bets`, `engine` (pure/headless), `game` (turtle GUI) and `cli`.
- Deterministic, seedable `RaceEngine` with no display dependency.
- `--headless`, `--seed`, `--colors`, `--bet`, `--track-length` and
  `--max-step` command-line options; `python -m race_turtle` and a
  `race-turtle` console script.
- Pytest suite (31 tests) covering the engine, bet logic and configuration.
- Packaging (`pyproject.toml`), tooling (ruff, mypy, pre-commit) and GitHub
  Actions CI across Python 3.9–3.12.
- README, MIT `LICENSE`, and project logo.

### Fixed
- Colour bets are now matched case-insensitively and whitespace-trimmed, so a
  correct guess like `Red` no longer scores as a loss.
- Winner detection is evaluated once via a single authoritative finish check
  instead of inside the per-turtle movement loop, removing duplicate/incorrect
  result messages.
- Invalid or cancelled bet input is validated and re-prompted.

### Removed
- Committed `venv/` and `.idea/` directories; both are now git-ignored.
