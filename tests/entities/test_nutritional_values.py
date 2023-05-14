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

from src.entities.nutritional_values import NutritionalValues


class TestNutritionalValues(unittest.TestCase):

    def setUp(self) -> None:
        self.nv1 = NutritionalValues()
        self.nv2 = NutritionalValues()
        self.nv3 = NutritionalValues()

        self.nv3.kcal = 1.0

    def test_repr(self):
        expected_value = f"""\
<NutritionalValues-object {id(self.nv1)}>
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

        self.assertEqual(repr(self.nv1), expected_value)

    def test_equality(self):
        self.assertEqual(self.nv1, self.nv2)
        self.assertNotEqual(self.nv1, self.nv3)
        self.assertNotEqual(self.nv1, None)

    def test_add(self):
        v1 = 5.0
        v2 = 5.0

        for k in self.nv1.__dict__.keys():
            self.nv1.__dict__[k] = v1
        for k in self.nv2.__dict__.keys():
            self.nv2.__dict__[k] = v2

        res_nv = self.nv1 + self.nv2

        for k in res_nv.__dict__.keys():
            self.assertEqual(res_nv.__dict__[k], v1 + v2)

    def test_sub(self):
        v1 = 10.0
        v2 = 3.0

        for k in self.nv1.__dict__.keys():
            self.nv1.__dict__[k] = v1
        for k in self.nv2.__dict__.keys():
            self.nv2.__dict__[k] = v2

        res_nv = self.nv1 - self.nv2

        for k in res_nv.__dict__.keys():
            self.assertEqual(res_nv.__dict__[k], v1 - v2)

    def test_mul_with_non_number(self):
        with self.assertRaises(ValueError):
            self.nv1 *= 'test'

    def test_mul(self):
        orig_value = 3.0
        multiplier = 5

        for k in self.nv1.__dict__.keys():
            self.nv1.__dict__[k] = orig_value

        res_nv = self.nv1 * multiplier

        for k in res_nv.__dict__.keys():
            self.assertEqual(res_nv.__dict__[k], orig_value * multiplier)

    def test_truediv_with_non_number(self):
        with self.assertRaises(ValueError):
            self.nv1 /= 'test'

    def test_truediv(self):
        orig_value = 15.0
        divider    = 5

        for k in self.nv1.__dict__.keys():
            self.nv1.__dict__[k] = orig_value

        res_nv = self.nv1 / divider

        for k in res_nv.__dict__.keys():
            self.assertEqual(res_nv.__dict__[k], orig_value / divider)

    def test_truediv_with_two_nv_objects(self):
        orig_value = 15.0
        multiplier = 2.0

        for k in self.nv1.__dict__.keys():
            self.nv1.__dict__[k] = orig_value  * multiplier

        for k in self.nv2.__dict__.keys():
            self.nv2.__dict__[k] = orig_value

        res_nv = self.nv1 / self.nv2

        for k in res_nv.__dict__.keys():
            self.assertEqual(res_nv.__dict__[k], multiplier)

    def test_apply_tef_multipliers(self):
        for k in self.nv1.__dict__.keys():
            self.nv1.__dict__[k] = 100.0

        orig_value = 1500
        self.nv1.kcal = orig_value
        self.nv1.apply_tef_multipliers()
        self.assertTrue(self.nv1.kcal < orig_value)

    def test_serialize(self):
        expected_string = ("{'kcal': 0.0, 'carbohydrates_g': 0.0, 'sugar_g': 0.0, 'protein_g': 0.0, "
                           "'fat_g': 0.0, 'satisfied_fat_g': 0.0, 'fiber_g': 0.0, 'salt_g': 0.0, "
                           "'omega3_dha_mg': 0.0, 'omega3_epa_mg': 0.0, 'vitamin_a_ug': 0.0, "
                           "'vitamin_d_ug': 0.0, 'vitamin_e_mg': 0.0, 'vitamin_k_ug': 0.0, "
                           "'vitamin_b1_mg': 0.0, 'vitamin_b2_mg': 0.0, 'vitamin_b3_mg': 0.0, "
                           "'vitamin_b5_mg': 0.0, 'vitamin_b6_mg': 0.0, 'vitamin_b7_ug': 0.0, "
                           "'vitamin_b9_ug': 0.0, 'vitamin_b12_ug': 0.0, 'vitamin_c_mg': 0.0, "
                           "'calcium_mg': 0.0, 'chromium_ug': 0.0, 'iodine_ug': 0.0, 'potassium_mg': "
                           "0.0, 'iron_mg': 0.0, 'magnesium_mg': 0.0, 'zinc_mg': 0.0, 'caffeine_mg': "
                           "0.0, 'creatine_g': 0.0}")
        self.assertEqual(self.nv1.serialize(), expected_string)

    def test_from_serialized(self):
        new_nv = NutritionalValues.from_serialized(self.nv1.serialize())
        self.assertEqual(new_nv, self.nv1)
