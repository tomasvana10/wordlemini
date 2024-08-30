"""General utilities."""

from gettext import translation

import pycountry

from . import DIR


def parse_lang(lang):
    normalised = lang.strip().lower()
    if pycountry.languages.get(alpha_2=normalised):
        return normalised

    try:
        language = pycountry.languages.lookup(normalised.title())
        return language.alpha_2
    except LookupError:
        return None


def translate(locale) -> None:
    translation(
        "messages",
        localedir=DIR / "locales",
        languages=[locale],
    ).install()
