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

from src.common.exceptions import ConversionError, ValidationError
from src.common.validation import validate_float, validate_int


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
