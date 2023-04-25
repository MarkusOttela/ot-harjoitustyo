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

from src.diet.enums import PhysicalActivityLevel, DietStage


def get_pal_multiplier(activity_level: PhysicalActivityLevel) -> float:
    """Get the physical activity level (PAL) multiplier.

    Source:
        https://en.wikipedia.org/wiki/Physical_activity_level
        http://www.fao.org/3/y5686e/y5686e07.htm

    Multiplier  LIFESTYLE           EXAMPLE
    --------------------------------------------------------------------------------------
    1.40-1.54   Sedentary           Office worker getting little or no exercise
    1.55-1.69   Lightly Active      Office worker who takes their pet for a walk most days
    1.70-1.99   Moderately Active   Construction worker / Walking job
    2.00-2.40   Vigorously active   Non-mechanized agricultural worker
    """
    multiplier_d = {PhysicalActivityLevel.SEDENTARY         : 1.2,
                    PhysicalActivityLevel.LIGHTLY_ACTIVE    : 1.375,
                    PhysicalActivityLevel.MODERATELY_ACTIVE : 1.555,
                    PhysicalActivityLevel.HIGHLY_ACTIVE     : 1.725}

    return multiplier_d[activity_level]


def get_calorie_deficit_multiplier(diet_stage: 'DietStage') -> float:
    """Determine the calorie deficit multiplier."""
    multiplier_d = {
        DietStage.DIET:                   0.8,
        DietStage.MUSCLE_MASS_GROWTH:     0.9,
        DietStage.BODY_BUILDING:          1.1,
        DietStage.SHREDDED_BODY_BUILDING: 1.0,
    }

    return multiplier_d[diet_stage]
