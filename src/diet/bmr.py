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

from src.common.statics import Gender


def calculate_bmr(gender    : Gender,
                  weight_kg : float,
                  height_cm : float,
                  age       : float,
                  ) -> float:
    """Calculate the basal metabolic rate with the St. Jeor formula (1990)[1].

    Accuracy:
        ~87% with normal weight individuals
        ~75% with overweight
        On average, ~5% more accurate than Harris-Benedict

    [1] https://inspire.edu.lb/inspire/educational-article-resources/How-to-Calculate-Your-Calorie-Intake-BMR-and-TDEE
    """
    constant = 5 if gender == Gender.MALE else -161

    return ((  10.00 * weight_kg)
            + ( 6.25 * height_cm)
            - ( 5.00 * age)
            + constant)
