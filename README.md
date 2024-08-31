<div align="center">

# wordlemini

</div>

<div align="center">

![wordlemini preview image](./wordlemini/assets/images/banner.png)
![licence](https://img.shields.io/badge/licence-MIT-green?style=flat?logo=licence)
[![PyPI version](https://img.shields.io/pypi/v/wordlemini?style=flat-square)](https://pypi.org/project/wordlemini/)
[![Publish to PyPI.org](https://github.com/tomasvana10/wordlemini/actions/workflows/publish.yml/badge.svg)](https://github.com/tomasvana10/wordlemini/actions/workflows/publish.yml)
[![release](https://img.shields.io/github/v/release/tomasvana10/wordlemini?logo=github)](https://github.com/tomasvana10/wordlemini/releases/latest)
[![issues](https://img.shields.io/github/issues-raw/tomasvana10/wordlemini.svg?maxAge=25000)](https://github.com/tomasvana10/wordlemini/issues)
[![CodeQL](https://github.com/tomasvana10/wordlemini/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/tomasvana10/wordlemini/actions/workflows/github-code-scanning/codeql)
[![Tests](https://github.com/tomasvana10/wordlemini/actions/workflows/tox-tests.yml/badge.svg)](https://github.com/tomasvana10/wordlemini/actions/workflows/tox-tests.yml)

</div>

`wordlemini` is a TUI package that allows you to play wordle in the command-line using `Textual`.

- Download the latest source code [here](https://github.com/tomasvana10/wordlemini/releases/latest).
- Available languages: Czech, German, English, Spanish, French, Italian, Dutch, Portugese, Russian

### Installation
Install the package from PyPI (a virtual environment is recommended):
```
pip install wordlemini
```

Run the game:
```
wordlemini
```

### CLI
**arguments**

- config
  - lang `<lang-code>` - Change the language.
  - dark `<on/off>` - Turn dark mode or on off.

Example: 
```
wordlemini config lang ru
```

- stats - View your stats, including your guess distribution and games played.

### Runtime dependencies
`textual` `platformdirs` `pycountry`

### Acknowledgements
[textual](https://textual.textualize.io/) - A Rapid Application Development framework for Python.

[platformdirs](https://pypi.org/project/platformdirs/) - Finding the right place to store user data, independent to the OS.

[pycountry](https://pypi.org/project/pycountry/) - ISO databases for languages

### Gallery
*Stats TUI*

![stats page](./wordlemini/assets/images/stats.png)
