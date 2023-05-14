Testing
---

## Unit tests

Excluding the UI module, the program has a 100% coverage for its unit tests.

## Integration tests

The integration tests for databases are done as part of serialization and deserialization of the objects,
and loading them from the databases

## System testing

The UI system testing is done by hand.

### Installation and configuration

The system was tested to work on 
  * Fresh installation of Ubuntu 22.04LTS
  * TODO: Cubbli 22.04 


## Linters

The code quality is maintained with several linters:

### mypy

* Static type checking 
  * Must pass with `strict flag`.
  * `Any` is allowed for polymorphic types only,

### pylint

* Code quality inspection

### autopep8

* Code styling inspection

Calorinator is mostly PEP8 compliant. However, code is not read just horizontally, 
but vertically as well. The custom style aims to improve readability in some cases 
where vertical alignment of assignment operators, keywords such as import, etc. 
make the code easier to read. 

Following PEP8 inspections have been disabled:

* `E201 - Whitespace after '('`
* `E202 - Whitespace before ']'`
* `E203 - Whitespace before ':'`
* `E221 - Multiple spaces before operator`
* `E222 - Multiple spaces after operator`
* `E241 - Multiple spaces after ','`
* `E272 - Space around keywords`


## Known issues

* Specifying the `Fixed portion(g)` for new ingredients might cause issues with correct nutrient density.
