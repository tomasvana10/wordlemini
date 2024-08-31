<div align="center">

# wordle-mini

</div>

<div align="center">

![wordle preview image](https://github.com/user-attachments/assets/25fba431-aa45-407d-9d40-c171ea655681)
![licence](https://img.shields.io/badge/licence-MIT-green?style=flat?logo=licence)
[![PyPI version](https://img.shields.io/pypi/v/wordlemini?style=flat-square)](https://pypi.org/project/wordlemini/)
[![Publish to PyPI.org](https://github.com/tomasvana10/wordlemini/actions/workflows/publish.yml/badge.svg)](https://github.com/tomasvana10/wordlemini/actions/workflows/publish.yml)
[![release](https://img.shields.io/github/v/release/tomasvana10/wordlemini?logo=github)](https://github.com/tomasvana10/wordlemini/releases/latest)
[![issues](https://img.shields.io/github/issues-raw/tomasvana10/wordlemini.svg?maxAge=25000)](https://github.com/tomasvana10/wordlemini/issues)
[![CodeQL](https://github.com/tomasvana10/wordlemini/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/tomasvana10/wordlemini/actions/workflows/github-code-scanning/codeql)
[![Tests](https://github.com/tomasvana10/wordlemini/actions/workflows/tox-tests.yml/badge.svg)](https://github.com/tomasvana10/wordlemini/actions/workflows/tox-tests.yml)

</div>

wordle in the command-line with `Textual`.

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
**positional arguments**

- config
  - lang `<lang-code>`
  - dark `<on/off>`

Example: 
```
wordlemini config lang ru
```

### Runtime dependencies
`textual` `platformdirs` `pycountry`

### Acknowledgements
[textual](https://textual.textualize.io/) - A Rapid Application Development framework for Python, built by Textualize.io.

[platformdirs](https://pypi.org/project/platformdirs/) - Finding the right place to store user data, independent to the OS.

[pycountry](https://pypi.org/project/pycountry/) - ISO databases for languages
