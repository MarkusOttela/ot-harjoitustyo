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

from src.entities.ingredient         import Ingredient, in_metadata
from src.entities.nutritional_values import NutritionalValues, nv_metadata


class TestIngredient(unittest.TestCase):

    def setUp(self) :
        self.ingredient1 = Ingredient('test_ingredient1', NutritionalValues())
        self.ingredient2 = Ingredient('test_ingredient2', NutritionalValues())
        self.ingredient1.nv_per_g.vitamin_b7_ug = '0.1'

    def test_equality(self):
        self.assertEqual(self.ingredient1, self.ingredient1)
        self.assertNotEqual(self.ingredient1, self.ingredient2)
        self.assertNotEqual(self.ingredient1, NutritionalValues())

    def test_str(self):
        self.assertEqual(str(self.ingredient1), 'test_ingredient1')

    # pylint: disable=duplicate-code
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
      vitamin_b7_ug   : 0.1
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

    def test_from_dict_missing_nv_key_raises_key_error(self):

        # Create test dict
        ingredient_d = {}
        for key, tup in nv_metadata.items():
            value = 1 if tup[1] == float else 'Test'
            ingredient_d[key] = value

        for key, tup in in_metadata.items():
            value = 1.0
            ingredient_d[key] = value

        ingredient_d['nv_per_g'] = NutritionalValues()

        # Remove one key
        del ingredient_d['kcal']

        # Test
        with self.assertRaises(KeyError):
            Ingredient.from_dict(ingredient_d)

    def test_from_dict_for_ingredients_with_grams_per_unit(self):

        # Create test dict
        units_in_gram = 5
        label_grams   = 100
        total_units   = units_in_gram * label_grams

        test_gram_amount = 1
        expected_value   = units_in_gram * test_gram_amount

        ingredient_d = {}
        for key, tup in nv_metadata.items():
            value = total_units if tup[1] == float else 'Test'
            ingredient_d[key] = value

        for key, tup in in_metadata.items():
            value = 1.0
            ingredient_d[key] = value

        ingredient_d['grams_per_unit']  = 100.0
        ingredient_d['fixed_portion_g'] = 0.0
        ingredient_d['nv_per_g'] = NutritionalValues()

        # Test
        ingredient = Ingredient.from_dict(ingredient_d)

        self.assertIsInstance(ingredient, Ingredient)

        nutritional_values = ingredient.get_nv(for_grams=test_gram_amount)
        for value in nutritional_values.__dict__.values():
            self.assertEqual(value, expected_value)

    def test_from_dict_for_ingredients_with_fixed_portion_size(self):

        # Create test dict (with example of five 2g capsules that contain each 0.1g of everything)
        grams_per_capsule = 2
        total_units_per_c = 0.1
        total_no_capsules = 5
        test_gram_amount  = grams_per_capsule * total_no_capsules
        expected_value    = total_no_capsules * total_units_per_c

        ingredient_d = {}
        for key, tup in nv_metadata.items():
            value = total_units_per_c if tup[1] == float else 'Test'
            ingredient_d[key] = value

        for key, tup in in_metadata.items():
            value = 1.0
            ingredient_d[key] = value

        ingredient_d['fixed_portion_g'] = grams_per_capsule
        ingredient_d['grams_per_unit']  = 100.0  # Must be overridden by fixed_portion_g
        ingredient_d['nv_per_g']        = NutritionalValues()

        # Test
        ingredient = Ingredient.from_dict(ingredient_d)

        self.assertIsInstance(ingredient, Ingredient)

        new_nv = ingredient.get_nv(for_grams=test_gram_amount)
        for value in new_nv.__dict__.values():
            self.assertEqual(value, expected_value)

    def test_get_nv(self) :
        # Setup
        start_value     = 5.0
        gram_multiplier = 10
        expected_value  = start_value * gram_multiplier

        for key in self.ingredient1.nv_per_g.__dict__.keys():
            self.ingredient1.nv_per_g.__dict__[key] = start_value

        # Test
        nutritional_values = self.ingredient1.get_nv(for_grams=gram_multiplier)
        for value in nutritional_values.__dict__.values():
            self.assertEqual(value, expected_value)
