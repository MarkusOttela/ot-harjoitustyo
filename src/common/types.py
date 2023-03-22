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
from typing import Annotated

from annotated_types import Gt, MinLen


class DatabaseTypes(Enum):
    """SQL Database types."""
    TEXT = 'TEXT'
    REAL = 'REAL'

# Ints
NonNegativeInt = Annotated[int, Gt(0)]

# Floats
NonNegativeFloat = Annotated[float, Gt(0)]

# Strings
NonEmptyStr = Annotated[str, MinLen(1)]
