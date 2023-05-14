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

from src.entities.mealprep import Mealprep
from src.entities.nutritional_values import NutritionalValues


class TestMealprep(unittest.TestCase):

    def setUp(self) -> None:
        self.mealprep1 = Mealprep('test',
                                  3500.0,
                                  '01/05/2023',
                                  ingredient_grams={'Water': 250,
                                                    'Salt': 5.0},
                                  mealprep_nv=NutritionalValues())

        self.mealprep2 = Mealprep('test',
                                  3500.0,
                                  '01/05/2023',
                                  ingredient_grams={'Water': 250,
                                                    'Salt': 5.0},
                                  mealprep_nv=NutritionalValues())

        self.mealprep3 = Mealprep('different_name',
                                  3500.0,
                                  '01/05/2023',
                                  ingredient_grams={'Water': 250,
                                                    'Salt': 5.0},
                                  mealprep_nv=NutritionalValues())

    def test_equality(self):
        self.assertEqual(self.mealprep1, self.mealprep2)
        self.assertNotEqual(self.mealprep1, self.mealprep3)
        self.assertNotEqual(self.mealprep1, NutritionalValues())

    def test_repr(self):
        expected_value = f"""\
<Mealprep-object {id(self.mealprep1)}>
  Cook_date: 01/05/2023
  Grams:     3500.0
   Ingredients:
     Water: 250g
     Salt: 5.0g
"""
        self.assertEqual(repr(self.mealprep1), expected_value)

    def test_str(self):
        self.assertEqual(str(self.mealprep1), 'test (01/05/2023)')

    def test_get_nv(self):
        # Setup
        start_value = 5.0
        gram_multiplier = 10
        expected_value = start_value * gram_multiplier

        for k in self.mealprep1.mealprep_nv.__dict__.keys():
            self.mealprep1.mealprep_nv.__dict__[k] = start_value

        # Test
        nv = self.mealprep1.get_nv(for_grams=gram_multiplier)
        for v in nv.__dict__.values():
            self.assertEqual(v, expected_value)
