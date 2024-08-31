"""Handling of user statistics such as guess distribution and games played."""

from typing import Dict, TypedDict

from ._config import Config


class _GuessDistributionTD(TypedDict):
    """Guess distribution format."""

    g1: int
    g2: int
    g3: int
    g4: int
    g5: int
    g6: int


class _StatisticsTD(TypedDict):
    """Format for the statistics section in the program config."""

    games: int
    wins: int
    losses: int
    guess_distribution: _GuessDistributionTD


class Statistics:
    """Handles the modification of statistics."""

    MAX_SQUARES = 37
    SQUARE = "\U000025a0"

    @staticmethod
    def add_entry(win: bool, guesses: int = 0) -> None:
        """Update the `statistics` section of the config."""
        cfg = Config.read()
        cfg["statistics"]["games"] += 1
        if win:
            cfg["statistics"]["wins"] += 1
            cfg["statistics"]["guess_distribution"][f"g{guesses}"] += 1
        else:
            cfg["statistics"]["losses"] += 1

        Config.write(cfg)

    @staticmethod
    def get_square_bars(
        # this is actually `_GuessDistributionTD` but I annotated it as `Dict`
        # to make mypy shut up
        distribution: Dict[str, int],
    ) -> str:
        """Convert the values (guesses) of a guess distribution dictionary to
        a bar-graph like string, similar to how NYT Wordle displays your guess
        distribution.
        """
        max_value = max(distribution.values())

        def calculate_squares(value: int) -> str:
            """Calculate how many squares should represent `value` based on
            `max_value`.
            """
            if not max_value:
                return ""
            return Statistics.SQUARE * int(
                (value / max_value) * Statistics.MAX_SQUARES
            )

        return "\n".join(
            [
                f"{i}  {calculate_squares(distribution.get(f'g{i}', 0))} ({distribution.get(f'g{i}', 0)})\n"  # noqa
                for i in range(1, 7)
            ]
        )
