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

import unittest

from src.common.enums    import DietType, Gender, PhysicalActivityLevel
from src.common.formulae import (calculate_bmr, calculate_nv_goal,
                                 get_pal_multiplier, get_calorie_diet_multiplier)

from src.entities.nutritional_values import NutritionalValues

from tests.utils import cd_unit_test, cleanup, create_mock_user


class TestCalculateBMR(unittest.TestCase):

    def test_calculate_bmr_for_male(self, ) -> None:
        """
        From https://www.omnicalculator.com/health/bmr

        10 × 68.04 + 6.25 × 162.56 – 5 × 60 + 5 = 680.4 + 1016 – 300 + 5 = 1401.4 (kcal / day)
        """
        bmr = calculate_bmr(Gender.MALE, weight_kg=68.04, height_cm=162.56, age=60)
        self.assertEqual(bmr, 1401.4)

    def test_calculate_bmr_for_female(self, ) -> None:
        """
        From https://www.omnicalculator.com/health/bmr

        10 × 59.87 + 6.25 × 172.72 – 5 × 25 - 161 = 598.7 + 1079.5 – 125 – 161 = 1392.2 (kcal/day)
        """
        bmr = calculate_bmr(Gender.FEMALE, weight_kg=59.87, height_cm=172.72, age=25)
        self.assertEqual(round(bmr, 1), 1392.2)


class TestCalculateNVGoal(unittest.TestCase):

    def setUp(self) -> None:
        self.unit_test_dir = cd_unit_test()
        self.user = create_mock_user()

    def tearDown(self) -> None:
        cleanup(self.unit_test_dir)

    def test_calculate_nv(self):
        nv = calculate_nv_goal(self.user)

        # Note: The values pinned here are simply to detect if
        #       the algorithm ever changes accidentally during
        #       development. There is no Known Answer Test to
        #       this specific algorithm as far as we know.
        self.assertIsInstance(nv, NutritionalValues)
        self.assertEqual(round(nv.kcal, 1),            2194.7)
        self.assertEqual(round(nv.protein_g, 1),        152.2)
        self.assertEqual(round(nv.fat_g, 1),             61.0)
        self.assertEqual(round(nv.carbohydrates_g, 1),  259.3)


class TestGetPalMultiplier(unittest.TestCase):

    def test_all_values_are_unique(self):
        values = [get_pal_multiplier(enum) for enum in PhysicalActivityLevel]
        self.assertEqual(len(values), len(set(values)))


class TestGetCalorieDietMultiplier(unittest.TestCase):

    def test_all_values_are_unique(self):
        values = [get_calorie_diet_multiplier(enum) for enum in DietType]
        self.assertEqual(len(values), len(set(values)))
