"""Handling of program configuration."""

from json import dump, load
from os import makedirs, path
from pathlib import Path
from typing import Any, Optional

from . import DIR, DOCS


class Config:
    """Class for interacting with wordlemini's configuration JSON."""

    TEMPLATE_CFG = DIR / "template.config.json"
    DOC_TOPLEVEL = DOCS / "wordlemini"
    DOC_CFG = DOC_TOPLEVEL / "config.json"
    CFG_SRC = TEMPLATE_CFG

    @property
    def fp(self):
        """Return the path to the config file."""
        makedirs(Config.DOC_TOPLEVEL, exist_ok=True)
        if not path.exists(Config.DOC_TOPLEVEL):
            Config.CFG_SRC = Config.TEMPLATE_CFG
            return Config.CFG_SRC  # Return base config (docs not available)
        if not path.exists(Config.DOC_CFG):
            # Make config in system documents
            Config.make_doc_cfg()
        Config.CFG_SRC = Config.DOC_CFG
        return Config.CFG_SRC

    @staticmethod
    def make_doc_cfg() -> None:
        """Create `config.json` in the system documents directory based on
        `template.config.json`.
        """
        with open(Config.DOC_CFG, "w", encoding="utf-8") as dest, open(
            Config.TEMPLATE_CFG, encoding="utf-8"
        ) as src:
            dump(load(src), dest, indent=4)

    @staticmethod
    def update() -> None:
        """If `Config.CFG_SRC` points to the documents directory, ensure it is
        up to date with the config at `Config.TEMPLATE_CFG`.
        """
        if not Config.CFG_SRC == Config.DOC_CFG:
            return
        template_cfg = Config.read(Config.TEMPLATE_CFG, no_update=True)
        doc_cfg = Config.read(Config.DOC_CFG, no_update=True)
        must_update = False
        for section in template_cfg:
            if section not in doc_cfg or any(
                opt not in doc_cfg[section] for opt in template_cfg[section]
            ):
                must_update = True
                break

        if must_update:
            Config.make_doc_cfg()

    @staticmethod
    def read(fp: Optional[Path] = None, no_update: bool = False) -> Any:
        """Return the data at `Config().fp`."""
        with open(fp or Config().fp, encoding="utf-8") as f:
            # Prevent recursion as `Config.update` calls this method
            if not no_update:
                Config.update()
            return load(f)

    @staticmethod
    def write(data: Any, fp: Optional[Path] = None) -> None:
        """Write `data` to `Config().fp`."""
        with open(fp or Config().fp, "w", encoding="utf-8") as f:
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
