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

from typing import Any

from src.common.exceptions import ConversionError, ValidationError
from src.common.validation import validate_float, validate_int

from src.gui.screens.callback_classes import StringInput


def str_to_float(key              : str,
                 string           : str,
                 negative_allowed : bool = False
                 ) -> float:
    """Convert string to float."""
    try:
        conversion = float(string)
        validate_float(key, conversion, negative_allowed)
        return conversion

    except (TypeError, ValueError, ValidationError):
        specifier = '' if negative_allowed else 'positive'
        raise ConversionError(f"'{string}' is not a valid {specifier} decimal number.")


def str_to_int(key              : str,
               string           : str,
               negative_allowed : bool = False
               ) -> float:
    """Convert string to int."""
    try:
        conversion = int(string)
        validate_int(key, conversion, negative_allowed)
        return conversion

    except (TypeError, ValueError, ValidationError):
        specifier = '' if negative_allowed else 'positive'
        raise ConversionError(f"'{string}' is not a valid {specifier} integer.")


def convert_input_fields(string_inputs : dict[str, StringInput],
                         keys          : list[str],
                         fields        : list[str],
                         field_types   : list[type]
                         ) -> tuple[bool, dict[str, Any]]:
    """Convert input fields of `Add Ingredient` menu to correct data types."""
    converted_values   : dict[str, Any ] = {}
    failed_conversions : dict[str, None] = {}
    converted_value    : Any

    for key, name, field_type in zip(keys, fields, field_types):
        try:
            string_value = string_inputs[key].value

            if field_type == int:
                converted_value = str_to_int(name, string_value)

            elif field_type == float:
                converted_value = str_to_float(name, string_value)

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
