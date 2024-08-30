"""Play wordle in the command-line."""

from pathlib import Path

from platformdirs import user_documents_dir

DIR = Path(__file__).resolve().parent
ASSETS = DIR / "assets"
CORPUS = ASSETS / "corpus"
DOCS = Path(user_documents_dir())
LANGUAGES = ["en", "es", "de", "fr", "ru", "pt", "it", "nl", "cs"]
