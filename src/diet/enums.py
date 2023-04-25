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

import typing

from enum import Enum

if typing.TYPE_CHECKING:
    pass


class PhysicalActivityLevel(Enum):
    """Activity lifestyle types."""
    SEDENTARY         = 'Sedentary'
    LIGHTLY_ACTIVE    = 'Lightly Active'
    MODERATELY_ACTIVE = 'Moderately Active'
    HIGHLY_ACTIVE     = 'Highly Active'


class DietStage(Enum):
    """Diet stage types."""
    DIET                   = 'Diet'
    MUSCLE_MASS_GROWTH     = 'Muscle mass growth'
    BODY_BUILDING          = 'Body building'
    SHREDDED_BODY_BUILDING = 'Shredded body building'


class CalContent(Enum):
    """Calorie content of macros."""
    KCAL_PER_GRAM_CARB    = 4
    KCAL_PER_GRAM_PROTEIN = 4
    KCAL_PER_GRAM_FAT     = 9
