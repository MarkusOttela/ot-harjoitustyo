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

from string import ascii_lowercase, ascii_uppercase, digits, punctuation

from typing import Any, Optional

from src.common.exceptions import ValidationError

integers = list(map(str, range(0, 10)))
floats   = integers + ['.']
date     = integers + ['/']
strings  = list(ascii_lowercase + ascii_uppercase + digits + punctuation + ' ')


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
    validate_type(key, value, str)

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


def validate_positive_float(string      : str,
                            var_name    : str = '',
                            upper_limit : Optional[float] = None
                            ) -> float:
    """Validate a string evaluates into a floating point value."""
    try:
        if string is None or string == '':
            raise ValueError

        decimal_value = float(string)

        if decimal_value <= 0.0:
            raise ValueError

        if upper_limit is not None and decimal_value > upper_limit:
            raise ValueError

        return decimal_value

    except ValueError as exc:
        ceil_text = '' if upper_limit is None else f' smaller than {upper_limit}'
        var_text  = '' if var_name == '' else f' for {var_name}'

        raise ValueError(f"Please enter a positive number{ceil_text}{var_text}") from exc


def validate_bool(key   : str,
                  value : bool,
                  ) -> None:
    """Validate a value is a boolean."""
    validate_str('key', key, empty_allowed=False)
    validate_type(key, value, bool)
