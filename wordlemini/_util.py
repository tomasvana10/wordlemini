"""General utilities."""

from gettext import translation
from typing import Union

import pycountry

from . import DIR


def parse_lang(lang: str) -> Union[None, str]:
    """Attempt to convert `lang` to its alpha_2 version, if not already in that
    format.
    """
    normalised = lang.strip().lower()
    if pycountry.languages.get(alpha_2=normalised):
        return normalised

    try:
        language = pycountry.languages.lookup(normalised.title())
        return language.alpha_2
    except LookupError:
        return None


def translate(locale: str) -> None:
    """Install gettext translations for `locale`."""
    translation(
        "messages",
        localedir=DIR / "locales",
        languages=[locale],
    ).install()
