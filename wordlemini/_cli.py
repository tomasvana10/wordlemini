from argparse import ArgumentParser
from logging import INFO, Formatter, StreamHandler, getLogger

from . import LANGUAGES
from .__main__ import initialise
from ._config import Config
from ._util import parse_lang

USAGE_INFO = """
Type `wordlemini -h` to view an information page.

Simply type `wordlemini` to initialise the text interface.

Supported languages (configurable with `wordlemini config lang <lang-or-code>`)
- Czech, German, English, Spanish, French, Italian, Dutch, Portugese, Russian
"""

logger = getLogger()
logger.setLevel(INFO)
console = StreamHandler()
formatter = Formatter("%(levelname)s: %(message)s")
console.setFormatter(formatter)
logger.addHandler(console)


def parse():
    parser = ArgumentParser(
        description="wordlemini CLI tool", prog="wordlemini", epilog=USAGE_INFO
    )

    subparsers = parser.add_subparsers(dest="command")

    config_parser = subparsers.add_parser(
        "config",
        help="Configure settings. Type wordlemini config -h to learn more.",
    )
    config_subparsers = config_parser.add_subparsers(dest="config_command")
    lang_parser = config_subparsers.add_parser(
        "lang", help="Set the language. e.x. `wordlemini config lang es`."
    )
    lang_parser.add_argument(
        "language", type=str, help="Language code or name"
    )
    dark_parser = config_subparsers.add_parser(
        "dark",
        help="Enable/disable dark mode. e.x. `wordlemini config dark off`.",
    )
    dark_parser.add_argument(
        "dark", type=str, help="Dark mode state - on or off"
    )
    args = parser.parse_args()
    handle_args(args)


def handle_args(args):
    if args.command is None:
        return initialise()
    if args.command == "config":
        if args.config_command == "lang":
            lang = parse_lang(args.language)
            if lang is None or lang not in LANGUAGES:
                return logger.error(
                    "Language is either invalid or not supported by wordlemini."
                )
            Config.set("settings", "lang", lang)
            return logger.info("Set language to %s.", lang)
        if args.config_command == "dark":
            dark = args.dark.strip().casefold()
            if dark == "on":
                val = True
            elif dark == "off":
                val = False
            else:
                return logger.error("Value must either be on or off")
            Config.set("settings", "dark", val)
            return logger.info("Turned dark mode %s.", dark)

    return None


if __name__ == "__main__":
    parse()
