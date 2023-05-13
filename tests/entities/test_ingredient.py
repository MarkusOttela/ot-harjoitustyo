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

from src.entities.ingredient import Ingredient
from src.entities.nutritional_values import NutritionalValues


class TestIngredient(unittest.TestCase):

    def setUp(self) -> None:
        self.ingredient1 = Ingredient('test_ingredient1', NutritionalValues())
        self.ingredient2 = Ingredient('test_ingredient2', NutritionalValues())

    def test_equality(self):
        self.assertEqual(self.ingredient1, self.ingredient1)
        self.assertNotEqual(self.ingredient1, self.ingredient2)

    def test_str(self):
        self.assertEqual(str(self.ingredient1), 'test_ingredient1')

    def test_repr(self):
        expected = f"""\
<Ingredient-object {id(self.ingredient1)}>
General Info
  Name: test_ingredient1
Nutrients: <NutritionalValues-object {id(self.ingredient1.nv_per_g)}>
    Energy (per 1g of ingredient)
      kcal            : 0.0
    Macronutrients (per 1g of ingredient)
      carbohydrates_g : 0.0
      sugar_g         : 0.0
      protein_g       : 0.0
      fat_g           : 0.0
      satisfied_fat_g : 0.0
      fiber_g         : 0.0
    Micronutrients (per 1g of ingredient)
      salt_g          : 0.0
      omega3_dha_mg   : 0.0
      omega3_epa_mg   : 0.0
      vitamin_a_ug    : 0.0
      vitamin_d_ug    : 0.0
      vitamin_e_mg    : 0.0
      vitamin_k_ug    : 0.0
      vitamin_b1_mg   : 0.0
      vitamin_b2_mg   : 0.0
      vitamin_b3_mg   : 0.0
      vitamin_b5_mg   : 0.0
      vitamin_b6_mg   : 0.0
      vitamin_b7_ug   : 0.0
      vitamin_b9_ug   : 0.0
      vitamin_b12_ug  : 0.0
      vitamin_c_mg    : 0.0
      calcium_mg      : 0.0
      chromium_ug     : 0.0
      iodine_ug       : 0.0
      potassium_mg    : 0.0
      iron_mg         : 0.0
      magnesium_mg    : 0.0
      zinc_mg         : 0.0
      caffeine_mg     : 0.0
      creatine_g      : 0.0"""

        self.assertEqual(repr(self.ingredient1), expected)
