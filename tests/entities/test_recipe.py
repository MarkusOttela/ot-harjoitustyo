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

from src.entities.recipe import Recipe


class TestRecipe(unittest.TestCase):

    def setUp(self) :

        self.recipe1 = Recipe('test_recipe1',
                              'tester',
                              ingredient_names=['Water', 'Salt'],
                              accompaniment_names=['Pasta'],
                              is_mealprep=True)

        self.recipe1_2 = Recipe('test_recipe1',
                                'tester',
                                ingredient_names=['Water', 'Salt'],
                                accompaniment_names=['Pasta'],
                                is_mealprep=True)

        self.recipe2 = Recipe('test_recipe3',
                              'tester',
                              ingredient_names=['Water', 'Salt'],
                              accompaniment_names=['Pasta'],
                              is_mealprep=True)

    def test_eq(self):
        self.assertTrue(self.recipe1 == self.recipe1_2)
        self.assertTrue(self.recipe1 != self.recipe2)
        self.assertTrue(self.recipe1 != str())

    def test_str(self):
        self.assertEqual(str(self.recipe1), self.recipe1.name)

    def test_repr(self):
        expected_value= f"""\
<Recipe-object {id(self.recipe1)}>
General Information
  Name        : test_recipe1
  Author      : tester
  Is Mealprep : True
Ingredients:
  Water
  Salt"""
        self.assertEqual(repr(self.recipe1), expected_value)
