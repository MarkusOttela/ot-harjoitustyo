<img align="right" src="https://raw.githubusercontent.com/MarkusOttela/ot-harjoitustyo/master/logo.png" style="position: relative; top: 0; left: 0;">

# Calorinator 

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-informational)](https://python.org)

[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Unit Tests](https://github.com/MarkusOttela/ot-harjoitustyo/actions/workflows/unit_tests.yml/badge.svg?branch=master)](https://github.com/MarkusOttela/ot-harjoitustyo/actions/workflows/unit_tests.yml)
[![codecov](https://codecov.io/gh/MarkusOttela/ot-harjoitustyo/branch/master/graph/badge.svg?token=W1LR4KBFNX)](https://codecov.io/gh/MarkusOttela/ot-harjoitustyo)

[![CodeFactor](https://www.codefactor.io/repository/github/markusottela/ot-harjoitustyo/badge)](https://www.codefactor.io/repository/github/markusottela/ot-harjoitustyo)

Calorinator supports the user in maintaining their diet by
  1. Tracking their meals, and by counting the nutritional values of each meal
  2. Informing them about the daily consumption in relation to their goal values
  3. Creating statistics about food and nutrient consumption, and progress of the diet

**Privacy preserving design**

* Locally hosted, all persistent sensitive data encrypted
* State-of-the-art primitives, all based on the [ChaCha](https://cr.yp.to/chacha/chacha-20080128.pdf) stream cipher
  * BLAKE2b cryptographic hash function
    * Argon2id password hashing function
  * ChaCha20 stream cipher
    * XChaCha20-Poly1305 AEAD (IETF variant)
    * Linux kernel primary DRNG


## Progress

* [x] Ingredient database
* [x] User registration
* [x] Password login
* [x] Initial survey
* [x] Mealprep recipe creation
* [x] Mealprep instance creation
* [x] Daily tracking
* [x] Statistics


### Releases

* [Week 5 Release](https://github.com/MarkusOttela/ot-harjoitustyo/releases/tag/viikko5)
* [Week 6 Release](https://github.com/MarkusOttela/ot-harjoitustyo/releases/tag/viikko6)


## Platform Support

* Linux / Python 3.8+


## Documentation

* [User Manual](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/Documentation/01%20-%20User%20Manual.md)
* [Functional Specification](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/Documentation/02%20-%20Functional%20Specification.md)
* [Program Architecture](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/Documentation/03%20-%20Architectural%20Design.md)
* [Testing](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/Documentation/04%20-%20Testing.md)
* [Hour Tracker](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/Documentation/05%20-%20Hour%20Tracker.md)
* [Changelog](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/Documentation/06%20-%20Changelog.md)
* [Architecture](https://github.com/MarkusOttela/ot-harjoitustyo/blob/master/Documentation/08%20-%20Architecture.md)


---

## Installation

##### 1. Install dependencies

```
$ sudo apt update
$ sudo apt install -y curl git
$ curl -sSL https://install.python-poetry.org | POETRY_HOME=$HOME/poetry python3 -
$ echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> $HOME/.bashrc && bash
$ echo "export PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring" >> $HOME/.bashrc && bash
```

##### 2. Install Calorinator
```
$ git clone https://github.com/MarkusOttela/ot-harjoitustyo.git $HOME/calorinator
$ cd $HOME/calorinator/
$ poetry install
```


### Launching

```
$ poetry run invoke start
```

Or if you prefer an alias

```
$ echo 'alias calorinator="poetry run python3 $HOME/calorinator/calorinator.py"' >> $HOME/.bashrc && bash
$ calorinator 
```

## Development


### Available Tasks


**Unit tests**

```
$ poetry run invoke test
```

**Unit test coverage report**

```
$ poetry run invoke coverage-report
$ xdg-open $HOME/calorinator/htmlcov/index.html
```


### Linters

**pylint style checks**

```
$ poetry run invoke lint
```

**mypy type checker**

```
$ poetry run invoke mypy
```

**AutoPEP8 linter**

```
$ poetry run invoke pep8
```
