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

from src.common.statics          import Gender
from src.diet.coef               import get_pal_multiplier, get_calorie_deficit_multiplier
from src.diet.enums              import CalContent
from src.diet.nutritional_values import NutritionalValues

if typing.TYPE_CHECKING:
    from src.entities.user import User


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

    [1] https://inspire.edu.lb/inspire/educational-article-resources/
        How-to-Calculate-Your-Calorie-Intake-BMR-and-TDEE
    """
    constant = 5 if gender == Gender.MALE else -161

    return ((  10.00 * weight_kg)
            + ( 6.25 * height_cm)
            - ( 5.00 * age)
            + constant)


def calculate_nv_goal(user: 'User') -> NutritionalValues:
    """Calculate the daily macro goals for the user.

    Protein goal: avg. form https://youtu.be/l7jIU_73ZaM?t=403
    """
    bmr = calculate_bmr(user.get_gender(),
                        user.get_todays_weight(),
                        user.get_height(),
                        user.get_age())

    theoretical_maintenance_kcal = get_pal_multiplier(user.get_pal()) * bmr
    calorie_deficit_multiplier   = get_calorie_deficit_multiplier(user.get_diet_stage())

    macro_goals_nv = NutritionalValues()

    kcal_goal         = calorie_deficit_multiplier * theoretical_maintenance_kcal

    protein_goal_g    = 1.9  * user.get_todays_weight()
    protein_goal_kcal = protein_goal_g * CalContent.KCAL_PER_GRAM_PROTEIN.value

    fat_goal_kcal     = 0.25 * kcal_goal
    fat_goal_g        = fat_goal_kcal / CalContent.KCAL_PER_GRAM_FAT.value

    carbs_goal_kcal   = kcal_goal - protein_goal_kcal - fat_goal_kcal
    carbs_goal_g      = carbs_goal_kcal / CalContent.KCAL_PER_GRAM_CARB.value

    macro_goals_nv.kcal            = kcal_goal
    macro_goals_nv.protein_g       = protein_goal_g
    macro_goals_nv.fat_g           = fat_goal_g
    macro_goals_nv.carbohydrates_g = carbs_goal_g

    return macro_goals_nv
