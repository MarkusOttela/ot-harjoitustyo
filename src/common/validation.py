#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

"""
Calorienator - Diet tracker
Copyright (C) Markus Ottela

This file is part of Calorienator.
Calorienator is free software: you can redistribute it and/or modify it under the 
terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version. Calorienator is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
details. You should have received a copy of the GNU General Public License
along with Calorienator. If not, see <https://www.gnu.org/licenses/>.
"""

import inspect

from src.common.Exceptions import ValidationError
from src.common.types      import NonEmptyStr, NonNegativeFloat, NonNegativeInt


def validate_str(key           : str,
                 value         : str,
                 empty_allowed : bool
                 ) -> None:
    """Validate a value is a string."""
    if not isinstance(key, str):
        raise ValidationError(f"Expected key of type {str}, was of type {type(value)}")

    if not isinstance(value, str):
        raise ValidationError(f"Expected value of type {str}, was of type {type(value)}")

    if not empty_allowed and value == '':
        raise ValidationError(f"Expected string '{key}' to contain chars but it was empty.")


def validate_int(key              : str,
                 value            : int,
                 negative_allowed : bool = False
                 ) -> None:
    """Validate a value is an integer."""
    validate_str('key', key, empty_allowed=False)

    if not isinstance(value, int):
        raise ValidationError(f"Expected {int}, was {type(value)}")

    if not negative_allowed and value < 0:
        raise ValidationError(f"Expected a positive value but value was {value}")


def validate_float(key              : str,
                   value            : float,
                   negative_allowed : bool = False
                   ) -> None:
    """Validate a value is a float."""
    validate_str('key', key, empty_allowed=False)

    if not isinstance(value, float):
        raise ValidationError(f"Expected {float}, type of '{key}' was {type(value)}")

    if not negative_allowed and value < 0.0:
        raise ValidationError(f"Expected a positive value but value was {value}")


def validate_params(func   : callable,
                    locals_: dict
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

        if expected_type in [str, NonEmptyStr]:
            validate_str(arg_name, arg_value, empty_allowed=expected_type != NonEmptyStr)

        if expected_type in [int, NonNegativeInt]:
            validate_int(arg_name, arg_value, negative_allowed=expected_type != NonNegativeInt)

        if expected_type in [float, NonNegativeFloat]:
            validate_float(arg_name, arg_value, negative_allowed=expected_type != NonNegativeFloat)
