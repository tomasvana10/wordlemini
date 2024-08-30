"""Handling of program configuration."""

from json import dump, load
from os import makedirs, path

from . import DIR, DOCS


class Config:
    BASE_CFG = DIR / "template.data.json"
    DOC_TOPLEVEL = DOCS / "wordlemini"
    DOC_CFG = DOC_TOPLEVEL / "data.json"

    @property
    def fp(self):
        makedirs(Config.DOC_TOPLEVEL, exist_ok=True)
        if not path.exists(Config.DOC_TOPLEVEL):
            return Config.BASE_CFG
        if not path.exists(Config.DOC_CFG):
            with open(Config.DOC_CFG, "x", encoding="utf-8") as dest, open(
                Config.BASE_CFG, encoding="utf-8"
            ) as src:
                dump(load(src), dest, indent=4)
        return Config.DOC_CFG

    @staticmethod
    def _read():
        with open(Config().fp, encoding="utf-8") as f:
            return load(f)

    @staticmethod
    def _write(data):
        with open(Config().fp, "w", encoding="utf-8") as f:
            return dump(data, f, indent=4)

    @staticmethod
    def get(sec, opt):
        return Config._read()[sec][opt]

    @staticmethod
    def set(sec, opt, val):
        cfg = Config._read()
        cfg[sec][opt] = val
        return Config._write(cfg)
