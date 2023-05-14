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

from src.entities.meal               import Meal
from src.entities.nutritional_values import NutritionalValues


class TestMeal(unittest.TestCase):

    def setUp(self) :

        self.meal = Meal('test',
                         '01/02/23-15:30:45',
                         250.0,
                         NutritionalValues(),
                         {'Water': 100.0}
                         )

        self.same_meal = Meal('test',
                              '01/02/23-15:30:45',
                              250.0,
                              NutritionalValues(),
                              {'Water': 100.0}
                              )

        self.other_meal1 = Meal('test',
                                '01/02/23-15:30:46',
                                250.0,
                                NutritionalValues(),
                                {'Water': 100.0}
                                )

        self.other_meal2 = Meal('test2',
                                '01/02/23-15:30:45',
                                250.0,
                                NutritionalValues(),
                                {'Water': 100.0}
                                )

    def test_repr(self):
        expected_output = f"""\
<Meal-object {id(self.meal)}>
  General Information:
    Name         : test
    Meal tstamp  : 01/02/23-15:30:45
    Total weight : 350.0g
    Energy       : 0.0kcal
  Accompaniments:
    Water: 100.0g"""

        self.assertEqual(repr(self.meal), expected_output)

    def test_equality(self):
        self.assertEqual(self.meal, self.same_meal)
        self.assertNotEqual(self.meal, self.other_meal1)
        self.assertNotEqual(self.meal, self.other_meal2)
        self.assertNotEqual(self.meal, NutritionalValues())

    def test_at_date(self):
        self.assertEqual(self.meal.eat_date, '01/02/23')

    def test_at_time(self):
        self.assertEqual(self.meal.eat_time, '15:30:45')

    def test_total_weight(self):
        self.assertEqual(self.meal.total_weight, 350.0)

    def test_serialize(self):
        expected_output = ("{'name': 'test', 'eat_tstamp': '01/02/23-15:30:45', "
                           "'main_grams': 250.0, "
                           '\'accompaniment_grams\': "{\'Water\': 100.0}", '
                           '\'meal_nv\': "{\'kcal\': 0.0, ' "'carbohydrates_g': 0.0, "
                           "'sugar_g': 0.0, 'protein_g': 0.0, 'fat_g': 0.0, "
                           "'satisfied_fat_g': 0.0, 'fiber_g': 0.0, 'salt_g': 0.0, "
                           "'omega3_dha_mg': 0.0, "
                           "'omega3_epa_mg': 0.0, 'vitamin_a_ug': 0.0, 'vitamin_d_ug': 0.0, "
                           "'vitamin_e_mg': 0.0, "
                           "'vitamin_k_ug': 0.0, 'vitamin_b1_mg': 0.0, "
                           "'vitamin_b2_mg': 0.0, 'vitamin_b3_mg': 0.0, "
                           "'vitamin_b5_mg': 0.0, "
                           "'vitamin_b6_mg': 0.0, 'vitamin_b7_ug': 0.0, 'vitamin_b9_ug': 0.0, "
                           "'vitamin_b12_ug': 0.0, "
                           "'vitamin_c_mg': 0.0, 'calcium_mg': 0.0, "
                           "'chromium_ug': 0.0, 'iodine_ug': 0.0, "
                           "'potassium_mg': 0.0, 'iron_mg': 0.0, "
                           "'magnesium_mg': 0.0, 'zinc_mg': 0.0, 'caffeine_mg': "
                           "0.0, 'creatine_g': " '0.0}"}')

        self.assertEqual(self.meal.serialize(), expected_output)

    def test_from_serialized(self):
        new_meal = Meal.from_serialized_string(self.meal.serialize())

        self.assertEqual(new_meal.name,       self.meal.name)
        self.assertEqual(new_meal.eat_tstamp, self.meal.eat_tstamp)
        self.assertEqual(new_meal.main_grams, self.meal.main_grams)
        self.assertEqual(new_meal.meal_nv,    self.meal.meal_nv)

        self.assertEqual(set(self.meal.accompaniment_grams.keys()),
                         set(new_meal.accompaniment_grams.keys()))

        for k in self.meal.accompaniment_grams.keys():
            self.assertEqual(self.meal.accompaniment_grams[k],
                             new_meal.accompaniment_grams[k])
