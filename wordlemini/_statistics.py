from typing import Any, TypedDict

from ._config import Config


class _GuessDistributionTD(TypedDict):
    g1: int
    g2: int
    g3: int
    g4: int
    g5: int
    g6: int


class _StatisticsTD(TypedDict):
    games: int
    wins: int
    losses: int
    guess_distribution: _GuessDistributionTD


class Statistics:
    MAX_SQUARES = 30
    SQUARE = "\U000025a0"

    @staticmethod
    def make_stats_entry(cfg: Any) -> Any:
        cfg["statistics"] = _StatisticsTD(
            games=0,
            wins=0,
            losses=0,
            guess_distribution=_GuessDistributionTD(
                g1=0, g2=0, g3=0, g4=0, g5=0, g6=0
            ),
        )
        return cfg

    @staticmethod
    def add_entry(win: bool, guesses: int = 0) -> None:
        cfg = Config.read()
        if "statistics" not in cfg:
            Statistics.make_stats_entry(cfg)
        cfg["statistics"]["games"] += 1

        if win:
            cfg["statistics"]["wins"] += 1
            cfg["statistics"]["guess_distribution"][f"g{guesses}"] += 1
        else:
            cfg["statistics"]["losses"] += 1

        Config.write(cfg)

    @staticmethod
    def guess_distribution_to_squares(
        distribution: dict[str, int],
    ) -> str:
        max_value = max(distribution.values())

        def calculate_squares(value: int) -> str:
            return Statistics.SQUARE * int(
                (value / max_value) * Statistics.MAX_SQUARES
            )

        return "\n".join(
            [
                f"{i}  {calculate_squares(distribution.get(f'g{i}', 0))} ({distribution.get(f'g{i}', 0)})\n"
                for i in range(1, 7)
            ]
        )
