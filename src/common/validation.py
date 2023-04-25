#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

"""
Calorinator - Diet tracker
Copyright (C) 2023 Markus Ottela

This file is part of Calorinator.
Calorinator is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. Calorinator is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License
along with Calorinator. If not, see <https://www.gnu.org/licenses/>.
"""

import inspect

from typing import Any, Callable

from src.common.exceptions import ValidationError

integers = list(map(str, range(0, 10)))
floats   = integers + ['.']
date     = integers + ['/']


def validate_type(key            : str,
                  purported_type : Any,
                  expected_type  : type
                  ) -> None:
    """Validate the type of value."""
    if not isinstance(purported_type, expected_type):
        raise ValidationError(f"Expected {expected_type}, "
                              f"but type of '{key}' was {type(purported_type)}")


def validate_str(key           : str,
                 value         : str,
                 empty_allowed : bool
                 ) -> None:
    """Validate a value is a string."""
    validate_type('key', key, str)
    validate_type(key,   value, str)

    if not empty_allowed and value == '':
        raise ValidationError(f"Expected string '{key}' to contain chars but it was empty.")


def validate_int(key              : str,
                 value            : int,
                 negative_allowed : bool = False
                 ) -> None:
    """Validate a value is an integer."""
    validate_str('key', key, empty_allowed=False)
    validate_type(key, value, int)

    if not negative_allowed and value < 0:
        raise ValidationError(f"Expected a positive value for '{key}', but value was {value}")


def validate_float(key              : str,
                   value            : float,
                   negative_allowed : bool = False
                   ) -> None:
    """Validate a value is a float."""
    validate_str('key', key, empty_allowed=False)
    validate_type(key, value, float)

    if not negative_allowed and value < 0.0:
        raise ValidationError(f"Expected a positive value for '{key}', but value was {value}")


def validate_bool(key   : str,
                  value : bool,
                  ) -> None:
    """Validate a value is a boolean."""
    validate_str('key', key, empty_allowed=False)
    validate_type(key, value, bool)


def validate_params(func   : Callable[[Any], Any],
                    locals_: dict,
                    ) -> None:
    """Validate parameters given to a function."""
    arg_names   = inspect.getfullargspec(func).args
    arg_names  += inspect.getfullargspec(func).kwonlyargs
    annotations = inspect.getfullargspec(func).annotations

    for arg_name in arg_names:

        if arg_name == 'self':  # Ignore self
            continue

        expected_type  = annotations[arg_name]
        arg_value      = locals_[arg_name]

        if expected_type == bool:
            validate_bool(arg_name, arg_value)
