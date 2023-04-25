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

from contextlib import contextmanager
from typing     import Any, Iterator


class CalorinatorException(Exception):
    """Base-class for internal program exceptions."""


class SecurityException(CalorinatorException):
    """Base-class for critical security exceptions that should close the program."""


class DatabaseException(CalorinatorException):
    """Base-class for database exceptions."""


class IngredientNotFound(DatabaseException):
    """Exception raised when the Ingredient is not found in the Ingredient database."""


class ValidationError(CalorinatorException):
    """Exception raised when a value fails validation"""


class ConversionError(CalorinatorException):
    """Exception raised when a value fails to convert."""


class IncompleteConversion(CalorinatorException):
    """Exception raised when conversion of all values fails."""


class IncorrectPassword(CalorinatorException):
    """Exception raised when the user enters an incorrect password."""


class AbortMenuOperation(CalorinatorException):
    """Exception raised when the user returns to main menu."""


@contextmanager
def ignored(*exceptions: Any) -> Iterator:
    """Ignore an exception."""
    try:
        yield
    except exceptions:
        pass
