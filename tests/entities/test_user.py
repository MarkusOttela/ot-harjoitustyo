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

from src.common.enums import PhysicalActivityLevel, DietType, Gender
from src.common.utils import get_today_str
from src.entities.meal import Meal
from src.entities.nutritional_values import NutritionalValues

from src.entities.user             import User
from src.entities.user_credentials import UserCredentials

from tests.utils import cd_unit_test, cleanup


class TestUser(unittest.TestCase):

    def setUp(self) :

        self.unit_test_dir = cd_unit_test()

        self.user_credentials1 = UserCredentials('test_user',
                                                 salt=32 * b'a',
                                                 database_key=32 * b'a')

        self.user_credentials2 = UserCredentials('test_user',
                                                 salt=32 * b'a',
                                                 database_key=32 * b'a')

        self.user_credentials3 = UserCredentials('diff_user',
                                                 salt=32 * b'a',
                                                 database_key=32 * b'a')

        self.user = User(self.user_credentials1,
                         dob='01/01/1990',
                         gender=Gender.MALE,
                         init_weight=79.0,
                         height=180,
                         pal=PhysicalActivityLevel.MODERATELY_ACTIVE,
                         diet_type=DietType.DIET)

        self.same_user = User(self.user_credentials2,
                              dob='01/01/1990',
                              gender=Gender.MALE,
                              init_weight=79.0,
                              height=180,
                              pal=PhysicalActivityLevel.MODERATELY_ACTIVE,
                              diet_type=DietType.DIET)

        self.diff_user = User(self.user_credentials3,
                              dob='01/01/1990',
                              gender=Gender.MALE,
                              init_weight=75.0,
                              height=180,
                              pal=PhysicalActivityLevel.MODERATELY_ACTIVE,
                              diet_type=DietType.DIET)

        self.morning_weight = 79.9

    def tearDown(self) :
        cleanup(self.unit_test_dir)

    def test_equality(self) :
        self.assertEqual(self.user,    self.same_user)
        self.assertNotEqual(self.user, self.diff_user)
        self.assertNotEqual(self.user, NutritionalValues())

    def test_repr(self):
        self.user.set_morning_weight(self.morning_weight)

        expected_string = f"""\
<User-object {id(self.user)}>
  Name:         test_user
  Birthday:     01/01/1990
  Gender:       Male
  Height:       180
  Init Weight:  80.0
  Curr. Weight: 79.9
  PAL:          Moderately Active
"""
        self.assertEqual(repr(self.user), expected_string)

    def test_serialize(self):
        self.user.set_morning_weight(self.morning_weight)

        expected_string = (b'{"name": "test_user", "birthday": "01/01/1990", "gender": "Male", '
                           b'"height_cm": 180, "init_weight_kg": 80.0, "pal": "Moderately Active", '
                           b'"diet_type": "Diet", "weight_log": "{\\"14/05/2023\\": 79.9}", '
                           b'"meal_log": "{}"}')

        self.assertEqual(self.user.serialize(), expected_string)

    def test_from_database(self):
        self.user.store_db()
        new_user = User.from_database(self.user_credentials1)

        self.assertEqual(self.user, new_user)

    def test_morning_weight(self):
        self.user.set_morning_weight(79.5)
        self.assertEqual(self.user.get_todays_weight(), 79.5)

    def test_storing_meals(self):
        meal = Meal('test', get_today_str(), 250.0, NutritionalValues(), {'Water': 250.0} )
        self.user.add_meal(meal)

        stored_meal = self.user.get_todays_meals()[0]
        self.assertEqual(stored_meal, meal)

    def test_delete_meal(self):
        meal = Meal('test',  get_today_str(), 250.0, NutritionalValues(), {'Water': 250.0})

        self.assertIsNone(self.user.delete_meal(meal))

        self.assertEqual(len(self.user.get_todays_meals()), 0)

        self.user.add_meal(meal)
        self.assertEqual(len(self.user.get_todays_meals()), 1)

        self.user.delete_meal(meal)
        self.assertEqual(len(self.user.get_todays_meals()), 0)

    def test_get_weight_log(self):
        self.assertIsInstance(self.user.get_weight_log(), dict)

    def test_has_weight_entry_for_the_day(self):
        self.assertFalse(self.user.has_weight_entry_for_the_day())
        self.user.set_morning_weight(79.5)
        self.assertTrue(self.user.has_weight_entry_for_the_day())
