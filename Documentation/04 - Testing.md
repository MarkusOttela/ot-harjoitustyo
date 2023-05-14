Testing
---

## Unit tests

Excluding the UI module, the program has a 100% coverage for its unit tests.

![](https://raw.githubusercontent.com/MarkusOttela/ot-harjoitustyo/master/Documentation/Attachments/test_coverage.png)

The `excluded` lines in the modules `src.common.formulae` and `src.database.encrypted_database` are due to the use 
of the `mypy` type linter. More specifically, the seemingly best practice of not importing modules for the simple sake 
of offline type checking by the linter. One big reason is this significantly increases the risk of running into circular 
imports. 


![](https://raw.githubusercontent.com/MarkusOttela/ot-harjoitustyo/master/Documentation/Attachments/skipped_lines.png)

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
  * ~~Must pass with `strict flag`.~~ 
    * UPDATE: Abandoned `--strict` due to disparity in backwards compatibility
      Python3.8 does not support type parameters for generic types, e.g. `list_of_numbers: list[int] = []`
  * `Any` is allowed for polymorphic types only,

### pylint

* Code quality inspection

* 0 warnings from tests module
* All disabled inspections are expalined in the source code
* 0 warnings from src module outside UI, where only warnings about cyclomatic complexity, namely
  * `too-many-statements`
  * `too-many-branches`
  * `too-many-nested-blocks`
  * `too-many-statements`
  * `too-many-locals`
  * `duplicate-code`

are present. Fixing these problems will require major refactoring of the UI-side code in the future. 

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
