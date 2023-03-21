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


class CalorienatorException(Exception):
    """Base-class for internal program exceptions."""
    pass

class DatabaseException(CalorienatorException):
    """Base-class for database exceptions."""
    pass

class IngredientNotFound(DatabaseException):
    """Exception raised when the Ingredient is not found in the Ingredient database."""
    pass

class ValidationError(CalorienatorException):
    """Exception raised when a value fails validation"""
    pass

class ConversionError(CalorienatorException):
    """Exception raised when a value fails to convert."""
    pass

class IncompleteConversion(CalorienatorException):
    """Exception raised when conversion of all values fails."""
    pass
