"""Handling of program configuration."""

from json import dump, load
from os import makedirs, path
from typing import Any

from . import DIR, DOCS


class Config:
    """Class for interacting with wordlemini's configuration JSON."""

    BASE_CFG = DIR / "template.data.json"
    DOC_TOPLEVEL = DOCS / "wordlemini"
    DOC_CFG = DOC_TOPLEVEL / "data.json"

    @property
    def fp(self):
        """Return the path to the config file."""
        makedirs(Config.DOC_TOPLEVEL, exist_ok=True)
        if not path.exists(Config.DOC_TOPLEVEL):
            return (
                Config.BASE_CFG
            )  # Return base config (documents not available)
        if not path.exists(Config.DOC_CFG):
            # Make config in system documents
            with open(Config.DOC_CFG, "x", encoding="utf-8") as dest, open(
                Config.BASE_CFG, encoding="utf-8"
            ) as src:
                dump(load(src), dest, indent=4)
        return Config.DOC_CFG

    @staticmethod
    def read() -> Any:
        """Return the data at `Config().fp`."""
        with open(Config().fp, encoding="utf-8") as f:
            return load(f)

    @staticmethod
    def write(data: Any) -> None:
        """Write `data` to `Config().fp`."""
        with open(Config().fp, "w", encoding="utf-8") as f:
            return dump(data, f, indent=4)

    @staticmethod
    def get(sec: str, opt: str) -> Any:
        """Get the value at `sec` and `opt` in the config."""
        return Config.read()[sec][opt]

    @staticmethod
    def set(sec: str, opt: str, val: Any) -> None:
        """Set config at `sec` and `opt` to `val` and write it to the file system."""
        cfg = Config.read()
        cfg[sec][opt] = val
        return Config.write(cfg)
