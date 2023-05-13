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


from src.common.enums      import DatabaseTableName
from src.common.exceptions import CriticalError, IngredientNotFound, RecipeNotFound

from src.database.unencrypted_database import (UnencryptedDatabase, IngredientDatabase,
                                               RecipeDatabase, MealprepDatabase)

from src.entities.ingredient         import Ingredient
from src.entities.mealprep           import Mealprep
from src.entities.nutritional_values import NutritionalValues
from src.entities.recipe             import Recipe

from tests.utils import cd_unit_test, cleanup


class TestUnencryptedDatabase(unittest.TestCase):

    def setUp(self) -> None:
        self.unit_test_dir = cd_unit_test()

        class Test:
            def __init__(self):
                self.test_string1 = 'test_data1'
                self.test_string2 = 'test_data2'

        test_obj = Test()

        metadata = {'test_string1': ('TestString1',  str),
                    'test_string2': ('TestString2',  str)}

        self.database = UnencryptedDatabase(DatabaseTableName.RECIPES, db_metadata=metadata)
        self.database.insert(test_obj)

    def tearDown(self) -> None:
        cleanup(self.unit_test_dir)

    def test_inserting_object_to_database_works(self) -> None:
        res = self.database.cursor.execute('SELECT test_string1, test_string2 FROM Recipes').fetchall()[0]
        self.assertEqual(res, ('test_data1', 'test_data2'))

    def test_get_list_of_entries(self) -> None:
        self.assertEqual(self.database.get_list_of_entries(), [('test_data1', 'test_data2')])


class TestIngredientDatabase(unittest.TestCase):

    def setUp(self) -> None:
        self.unit_test_dir = cd_unit_test()
        self.database = IngredientDatabase()

        self.mock_ingredient1   = Ingredient('test_ingredient_1', NutritionalValues())
        self.mock_ingredient1_2 = Ingredient('test_ingredient_1', NutritionalValues(kcal=1))
        self.mock_ingredient3   = Ingredient('test_ingredient_3', NutritionalValues())

    def tearDown(self) -> None:
        cleanup(self.unit_test_dir)

    def test_get_list_of_ingredients_returns_list_of_ingredients(self) -> None:
        self.assertIsInstance(self.database.get_list_of_ingredients(), list)
        self.assertEqual(len(self.database.get_list_of_ingredients()), 0)

        self.database.insert(self.mock_ingredient1)
        self.assertEqual(len(self.database.get_list_of_ingredients()), 1)

    def test_get_ingredient(self):
        self.database.insert(self.mock_ingredient1)
        ingredient = self.database.get_ingredient('test_ingredient_1')
        self.assertIsInstance(ingredient, Ingredient)
        self.assertEqual(ingredient.name, 'test_ingredient_1')

        with self.assertRaises(IngredientNotFound):
            self.database.get_ingredient('does_not_exist')

    def test_remove_ingredient(self) -> None:
        self.database.insert(self.mock_ingredient1)

        # Test invalid parameter raises CriticalError
        with self.assertRaises(CriticalError):
            self.database.remove_ingredient(1)

        with self.assertRaises(IngredientNotFound):
            self.database.remove_ingredient(self.mock_ingredient3)

        self.assertEqual(len(self.database.get_list_of_ingredients()), 1)
        self.database.remove_ingredient(self.mock_ingredient1)
        self.assertEqual(len(self.database.get_list_of_ingredients()), 0)

    def test_replace_ingredient(self):
        self.database.insert(self.mock_ingredient1)

        # Test invalid parameter raises CriticalError
        with self.assertRaises(CriticalError):
            self.database.replace_ingredient(1)

        self.assertEqual(len(self.database.get_list_of_ingredients()), 1)
        self.database.replace_ingredient(self.mock_ingredient1_2)

        self.assertEqual(len(self.database.get_list_of_ingredients()), 1)

        # Test that new ingredient with different NV works
        ingredient = self.database.get_ingredient('test_ingredient_1')
        self.assertEqual(ingredient.nv_per_g.kcal, 1)

    def test_has_ingredient(self):
        self.database.insert(self.mock_ingredient1)

        # Test invalid parameter raises CriticalError
        with self.assertRaises(CriticalError):
            self.database.has_ingredient(1)

        self.assertTrue(self.database.has_ingredient(self.mock_ingredient1))
        self.assertFalse(self.database.has_ingredient(self.mock_ingredient3))

    def test_has_ingredients(self) -> None:
        self.assertFalse(self.database.has_ingredients())
        self.database.insert(self.mock_ingredient1)
        self.assertTrue(self.database.has_ingredients())


class TestRecipeDatabase(unittest.TestCase):

    def setUp(self) -> None:
        self.unit_test_dir   = cd_unit_test()
        self.recipe_database = RecipeDatabase()

        water = Ingredient('Water', NutritionalValues())
        salt  = Ingredient('Salt', NutritionalValues())

        self.mock_recipe1   = Recipe('test_recipe_1', 'tester', [water, salt], [],     False)
        self.mock_recipe1_2 = Recipe('test_recipe_1', 'tester', [water],       [],     False)
        self.mock_recipe3   = Recipe('test_recipe_3', 'tester', [water, salt], [],     False)
        self.mock_mp_recipe = Recipe('test_recipe_mp', 'tester', [water],       [salt], True)

    def tearDown(self) -> None:
        cleanup(self.unit_test_dir)

    def test_get_list_of_recipe_names(self):
        self.assertEqual(self.recipe_database.get_list_of_recipe_names(), [])
        self.recipe_database.insert_recipe(self.mock_recipe1)
        self.recipe_database.insert_recipe(self.mock_recipe3)
        self.assertEqual(self.recipe_database.get_list_of_recipe_names(), ['test_recipe_1', 'test_recipe_3'])

    def test_get_list_of_recipes(self):
        self.assertEqual(self.recipe_database.get_list_of_recipes(), [])
        self.recipe_database.insert_recipe(self.mock_recipe1)
        self.recipe_database.insert_recipe(self.mock_recipe3)
        self.assertEqual(self.recipe_database.get_list_of_recipes(), [self.mock_recipe1, self.mock_recipe3])

    def test_get_list_of_single_recipes(self):
        self.assertEqual(self.recipe_database.get_list_of_single_recipes(), [])

        self.recipe_database.insert_recipe(self.mock_mp_recipe)
        self.assertEqual(self.recipe_database.get_list_of_single_recipes(), [])

        self.recipe_database.insert_recipe(self.mock_recipe1)
        self.recipe_database.insert_recipe(self.mock_recipe3)

        self.assertEqual(self.recipe_database.get_list_of_single_recipes(), [self.mock_recipe1, self.mock_recipe3])

    def test_get_list_of_melprep_recipes(self):
        self.assertEqual(self.recipe_database.get_list_of_mealprep_recipes(), [])

        self.recipe_database.insert_recipe(self.mock_recipe1)
        self.assertEqual(self.recipe_database.get_list_of_mealprep_recipes(), [])

        self.recipe_database.insert_recipe(self.mock_mp_recipe)
        self.assertEqual(self.recipe_database.get_list_of_mealprep_recipes(), [self.mock_mp_recipe])

    def test_get_recipe(self):
        self.recipe_database.insert_recipe(self.mock_recipe1)
        r1 = self.recipe_database.get_recipe('test_recipe_1')
        r2 = self.recipe_database.get_recipe('test_recipe_1', 'tester')
        self.assertEqual(r1.name,   r2.name)
        self.assertEqual(r1.author, r2.author)

        with self.assertRaises(RecipeNotFound):
            self.recipe_database.get_recipe('test_recipe_1', author='does_not_exist')

    def test_insert_recipe(self):

        # Test invalid parameter raises CriticalError
        with self.assertRaises(CriticalError):
            self.recipe_database.insert_recipe(1)

        self.recipe_database.insert_recipe(self.mock_recipe1)

        res = self.recipe_database.cursor.execute('SELECT * FROM Recipes').fetchall()[0]

        self.assertEqual(res, ('test_recipe_1', 'tester', 'Water\x1fSalt', 'None', 'False'))

    def test_has_recipe(self):
        self.recipe_database.insert_recipe(self.mock_recipe1)

        # Test invalid parameter raises CriticalError
        with self.assertRaises(CriticalError):
            self.recipe_database.has_recipe(1)

        self.assertTrue(self.recipe_database.has_recipe(self.mock_recipe1))
        self.assertFalse(self.recipe_database.has_recipe(self.mock_recipe3))

    def test_remove_recipe(self) -> None:
        self.recipe_database.insert_recipe(self.mock_recipe1)

        # Test invalid parameter raises CriticalError
        with self.assertRaises(CriticalError):
            self.recipe_database.remove_recipe(1)

        with self.assertRaises(RecipeNotFound):
            self.recipe_database.remove_recipe(self.mock_recipe3)

        self.assertEqual(len(self.recipe_database.get_list_of_recipes()), 1)
        self.recipe_database.remove_recipe(self.mock_recipe1)
        self.assertEqual(len(self.recipe_database.get_list_of_recipes()), 0)

    def test_replace_recipe(self):
        self.recipe_database.insert_recipe(self.mock_recipe1)

        # Test invalid parameter raises CriticalError
        with self.assertRaises(CriticalError):
            self.recipe_database.replace_recipe(1)

        self.assertEqual(len(self.recipe_database.get_list_of_recipes()), 1)
        self.recipe_database.replace_recipe(self.mock_recipe1_2)

        self.assertEqual(len(self.recipe_database.get_list_of_recipes()), 1)

        recipe = self.recipe_database.get_recipe('test_recipe_1')
        self.assertEqual(recipe.ingredient_names, ['Water'])


class TestMealprepDatabase(unittest.TestCase):
    
    def setUp(self) -> None:
        self.unit_test_dir   = cd_unit_test()
        self.mealprep_database = MealprepDatabase()

        self.mock_mealprep1   = Mealprep('test_mealprep_1',
                                         total_grams=150.0,
                                         cook_date='14/05/2023',
                                         ingredient_grams={'Water': 50, 'Salt': 20},
                                         mealprep_nv=NutritionalValues())
        self.mock_mealprep1_2 = Mealprep('test_mealprep_1',
                                         total_grams=150.0,
                                         cook_date='14/05/2023',
                                         ingredient_grams={'Water': 50},
                                         mealprep_nv=NutritionalValues())
        self.mock_mealprep3   = Mealprep('test_mealprep_3',
                                         total_grams=150.0,
                                         cook_date='14/05/2023',
                                         ingredient_grams={'Water': 50, 'Salt': 20},
                                         mealprep_nv=NutritionalValues())

    def tearDown(self) -> None:
        cleanup(self.unit_test_dir)

    def test_get_list_of_mealprep_names(self):
        self.assertEqual(self.mealprep_database.get_list_of_mealprep_names(), [])
        self.mealprep_database.insert_mealprep(self.mock_mealprep1)
        self.mealprep_database.insert_mealprep(self.mock_mealprep3)
        self.assertEqual(self.mealprep_database.get_list_of_mealprep_names(), ['test_mealprep_1', 'test_mealprep_3'])

    def test_get_list_of_mealpreps(self):
        self.assertEqual(self.mealprep_database.get_list_of_mealpreps(), [])
        self.mealprep_database.insert_mealprep(self.mock_mealprep1)
        self.mealprep_database.insert_mealprep(self.mock_mealprep3)

        mealprep_list = self.mealprep_database.get_list_of_mealpreps()
        self.assertEqual(mealprep_list, [self.mock_mealprep1, self.mock_mealprep3])

    def test_get_mealprep(self):
        self.mealprep_database.insert_mealprep(self.mock_mealprep1)

        with self.assertRaises(RecipeNotFound):
            self.mealprep_database.get_mealprep('does_not_exist')

        self.assertIsInstance(self.mealprep_database.get_mealprep('test_mealprep_1'), Mealprep)

    def test_insert_mealprep(self):

        # Test invalid parameter raises CriticalError
        with self.assertRaises(CriticalError):
            self.mealprep_database.insert_mealprep(1)

        self.mealprep_database.insert_mealprep(self.mock_mealprep1)

        res = self.mealprep_database.cursor.execute('SELECT * FROM Mealpreps').fetchall()[0]
        self.assertEqual(res, ('test_mealprep_1',
                               150.0,
                               '14/05/2023',
                               "{'Water': 50, 'Salt': 20}",
                               "{'kcal': 0.0, 'carbohydrates_g': 0.0, 'sugar_g': 0.0, "
                               "'protein_g': 0.0, 'fat_g': 0.0, 'satisfied_fat_g': 0.0, "
                               "'fiber_g': 0.0, 'salt_g': 0.0, 'omega3_dha_mg': 0.0, "
                               "'omega3_epa_mg': 0.0, 'vitamin_a_ug': 0.0, 'vitamin_d_ug': 0.0, "
                               "'vitamin_e_mg': 0.0, 'vitamin_k_ug': 0.0, 'vitamin_b1_mg': 0.0, "
                               "'vitamin_b2_mg': 0.0, 'vitamin_b3_mg': 0.0, 'vitamin_b5_mg': 0.0, "
                               "'vitamin_b6_mg': 0.0, 'vitamin_b7_ug': 0.0, 'vitamin_b9_ug': 0.0, "
                               "'vitamin_b12_ug': 0.0, 'vitamin_c_mg': 0.0, 'calcium_mg': 0.0, "
                               "'chromium_ug': 0.0, 'iodine_ug': 0.0, 'potassium_mg': 0.0,"
                               " 'iron_mg': 0.0, 'magnesium_mg': 0.0, 'zinc_mg': 0.0,"
                               " 'caffeine_mg': 0.0, 'creatine_g': 0.0}"))

    def test_has_mealprep(self):
        self.mealprep_database.insert_mealprep(self.mock_mealprep1)

        # Test invalid parameter raises CriticalError
        with self.assertRaises(CriticalError):
            self.mealprep_database.has_mealprep(1)

        self.assertTrue(self.mealprep_database.has_mealprep(self.mock_mealprep1))
        self.assertFalse(self.mealprep_database.has_mealprep(self.mock_mealprep3))

    def test_remove_mealprep(self):
        self.mealprep_database.insert_mealprep(self.mock_mealprep1)

        # Test invalid parameter raises CriticalError
        with self.assertRaises(CriticalError):
            self.mealprep_database.remove_mealprep(1)

        with self.assertRaises(RecipeNotFound):
            self.mealprep_database.remove_mealprep(self.mock_mealprep3)

        self.assertEqual(len(self.mealprep_database.get_list_of_mealpreps()), 1)
        self.mealprep_database.remove_mealprep(self.mock_mealprep1)
        self.assertEqual(len(self.mealprep_database.get_list_of_mealpreps()), 0)

    def test_replace_mealprep(self):
        self.mealprep_database.insert_mealprep(self.mock_mealprep1)

        # Test invalid parameter raises CriticalError
        with self.assertRaises(CriticalError):
            self.mealprep_database.replace_mealprep(1)

        self.assertEqual(len(self.mealprep_database.get_list_of_mealpreps()), 1)
        self.mealprep_database.replace_mealprep(self.mock_mealprep1_2)

        self.assertEqual(len(self.mealprep_database.get_list_of_mealpreps()), 1)

        mealprep = self.mealprep_database.get_mealprep('test_mealprep_1')
        self.assertEqual(list(mealprep.ingredient_grams.keys()), ['Water'])
