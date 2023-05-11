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

from enum   import Enum
from typing import Any

from src.common.exceptions import ConversionError, ValidationError
from src.common.validation import validate_float, validate_int


class Conversion(Enum):
    """Conversion values."""
    DAYS_PER_YEAR = 365.25


def str_to_float(key              : str,
                 string           : str,
                 negative_allowed : bool = False
                 ) -> float:
    """Convert string to float."""
    try:
        conversion = float(string)
        validate_float(key, conversion, negative_allowed)
        return conversion

    except (TypeError, ValueError, ValidationError) as conv_error:
        specifier = '' if negative_allowed else 'positive'
        raise ConversionError(f"'{string}' is not a valid "
                              f"{specifier} decimal number.") from conv_error


def str_to_int(key              : str,
               string           : str,
               negative_allowed : bool = False
               ) -> float:
    """Convert string to int."""
    try:
        conversion = int(string)
        validate_int(key, conversion, negative_allowed)
        return conversion

    except (TypeError, ValueError, ValidationError) as conv_error:
        specifier = '' if negative_allowed else 'positive'
        raise ConversionError(f"'{string}' is not a valid {specifier} integer.") from conv_error


def convert_input_fields(string_inputs : dict,
                         metadata      : dict
                         ) -> tuple:
    """Convert StringInput dictionary values to correct data types."""
    converted_values   : dict = {}
    failed_conversions : dict = {}
    converted_value    : Any

    for key in string_inputs.keys():
        try:
            string_value = string_inputs[key].value
            field_name   = metadata[key][0]
            field_type   = metadata[key][1]

            if field_type == int:
                converted_value = str_to_int(field_name, string_value)

            elif field_type == float:
                converted_value = str_to_float(field_name, string_value)

            elif field_type == str:
                converted_value = string_value

            else:
                raise ValueError(f"Unknown field type {field_type}.")

            converted_values[key] = converted_value

        except (ConversionError, ValidationError):
            failed_conversions[key] = None

    if failed_conversions:
        return False, failed_conversions
    return True, converted_values
