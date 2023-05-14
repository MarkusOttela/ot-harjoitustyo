#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

"""
Calorinator - Diet tracker
Copyright (C) 2023 Markus Ottela

This fiber_gle is part of Calorinator.
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

from src.database.default_ingredient_database import default_ingredients
from src.database.unencrypted_database        import IngredientDatabase

from tests.utils import cd_unit_test, create_mock_user, cleanup


class TestDefaultIngredientDatabase(unittest.TestCase):

    def setUp(self) :
        self.unit_test_dir = cd_unit_test()
        self.user          = create_mock_user()

    def tearDown(self) :
        cleanup(self.unit_test_dir)

    def test_default_ingredients_can_be_imported(self):
        ingredient_db = IngredientDatabase()

        if not ingredient_db.get_list_of_ingredients():
            for ingredient in default_ingredients:
                ingredient_db.insert(ingredient)

        self.assertEqual(len(default_ingredients),
                         len(ingredient_db.get_list_of_ingredient_names()))
