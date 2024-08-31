from typing import Any, TypedDict

from ._config import Config


class _GuessDistribution(TypedDict):
    g1: int
    g2: int
    g3: int
    g4: int
    g5: int
    g6: int


class _Statistics(TypedDict):
    games: int
    wins: int
    losses: int
    guess_distribution: _GuessDistribution


class Statistics:
    @staticmethod
    def make_stats_entry(cfg: Any) -> Any:
        cfg["statistics"] = _Statistics(
            games=0,
            wins=0,
            losses=0,
            guess_distribution=_GuessDistribution(
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
