Testing
---

## Unit tests


## Integration tests


## System testing
### Installation and configuration
### Functionality


## Linters

The code quality is maintained with several linters:

### mypy

* Static type checking 
  * Must pass with `strict flag`.
  * `Any` is allowed for polymorphic types only,

### pylint

* Code quality inspection

### autopep8

Calorinator is mostly PEP8 compliant.

However: Code is not read just horizontally, but vertically as well.
The custom style aims to improve readability in some cases where vertical alignment
of assignment operators, keywords such as import, etc. make the code easier to read. 

Following PEP8 inspections have been disabled:

* `E201 - Whitespace after '('`
* `E202 - Whitespace before ']'`
* `E203 - Whitespace before ':'`
* `E221 - Multiple spaces before operator`
* `E222 - Multiple spaces after operator`
* `E272 - Space around keywords`


## Known issues
