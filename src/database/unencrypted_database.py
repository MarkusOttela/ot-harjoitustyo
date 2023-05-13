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

import ast
import sqlite3

from collections import ChainMap
from typing      import Any

from src.common.exceptions import IngredientNotFound, RecipeNotFound
from src.common.enums      import DatabaseFileName, Directories, DatabaseTableName, DatabaseTypes
from src.common.utils      import ensure_dir

from src.entities.ingredient         import Ingredient, in_metadata
from src.entities.mealprep           import Mealprep, mealprep_metadata
from src.entities.nutritional_values import nv_metadata, NutritionalValues
from src.entities.recipe             import Recipe, recipe_metadata

column_type_dict : dict = {
    str   : DatabaseTypes.TEXT.value,
    float : DatabaseTypes.REAL.value,
    bool  : DatabaseTypes.TEXT.value,
    list  : DatabaseTypes.TEXT.value
}


class UnencryptedDatabase:
    """UnencryptedDatabase is an SQLite3 database for storing non-sensitive data.

    The database is intended to be public and shareable, thus it is not encrypted.
    """

    def __init__(self,
                 table_name  : DatabaseTableName,
                 db_metadata : dict
                 ) -> None:
        """Create new UnencryptedDatabase object."""
        ensure_dir(Directories.USER_DATA.value)
        self.table_name  = table_name.value
        self.db_metadata = db_metadata
        self.connection  = sqlite3.connect(f'{Directories.USER_DATA.value}'
                                           f'/{DatabaseFileName.SHARED_DATABASE.value}.sqlite3')
        self.cursor      = self.connection.cursor()
        self.connection.isolation_level = None
        self.create_table()

    def create_table(self) -> None:
        """Create the database table procedurally."""
        sql_command = f'CREATE TABLE IF NOT EXISTS {self.table_name} ('

        for key, value in self.db_metadata.items():
            column_name  = key
            data_type    = value[1]
            sql_command += f"{column_name} {column_type_dict[data_type]}, "

        sql_command  = sql_command[:-2]  # Remove trailing comma and space
        sql_command += ')'

        self.cursor.execute(sql_command)

    def insert(self, obj: Any) -> None:
        """Insert object into the database."""
        keys   = list(self.db_metadata.keys())
        values = [getattr(obj, key) for key in keys]

        sql_command  = f'INSERT INTO {self.table_name} ('
        sql_command += ', '.join(keys)
        sql_command += ') VALUES ('
        sql_command += ', '.join(len(keys) * ['?'])
        sql_command += ')'

        self.cursor.execute(sql_command, values)
        self.cursor.connection.commit()

    def get_list_of_entries(self) -> list:
        """Get list of entries in the database."""
        sql_command  =  'SELECT '
        sql_command +=  ', '.join(list(self.db_metadata.keys()))
        sql_command += f' FROM {self.table_name}'

        return self.cursor.execute(sql_command).fetchall()


class IngredientDatabase(UnencryptedDatabase):
    """\
    IngredientDatabase contains the data including name
    and nutritional values of each ingredient.
    """

    def __init__(self) -> None:
        """Create new IngredientDatabase."""
        super().__init__(table_name=DatabaseTableName.INGREDIENTS,
                         db_metadata=dict(ChainMap(nv_metadata, in_metadata)))

    def insert(self, obj: Ingredient) -> None:
        """Insert Ingredient into the database."""
        in_keys   = list(in_metadata.keys())
        nv_keys   = list(nv_metadata.keys())
        in_values = [getattr(obj, key)          for key in in_keys]
        nv_values = [getattr(obj.nv_per_g, key) for key in nv_keys]
        no_values = len(in_keys + nv_keys)

        sql_command  = f'INSERT INTO {self.table_name} ('
        sql_command += ', '.join(in_keys + nv_keys)
        sql_command += ') VALUES ('
        sql_command += ', '.join(no_values * ['?'])
        sql_command += ')'

        self.cursor.execute(sql_command, in_values + nv_values)
        self.cursor.connection.commit()

    def get_list_of_ingredient_names(self) -> list:
        """Get list of ingredient names."""
        sql_command = f'SELECT Name FROM {self.table_name}'
        results     = [r[0] for r in self.cursor.execute(sql_command).fetchall()]
        return results

    def get_list_of_ingredients(self) -> list:
        """Get list of ingredients in the database."""
        return [self.get_ingredient(name) for name in self.get_list_of_ingredient_names()]

    def get_ingredient(self, name: str) -> Ingredient:
        """Get Ingredient from database by name."""
        keys = list(self.db_metadata.keys())[1:]

        sql_command  =  'SELECT '
        sql_command +=  ', '.join(keys)
        sql_command += f' FROM {self.table_name}'
        sql_command += f" WHERE {self.db_metadata['name'][0]} == '{name}'"

        result = self.cursor.execute(sql_command).fetchall()[0]

        if not result:
            raise IngredientNotFound(f"Could not find ingredient '{name}'.")

        ingredient = Ingredient(name, NutritionalValues(*result[2:]),
                                grams_per_unit=result[0],
                                fixed_portion_g=result[1])

        return ingredient

    def remove_ingredient(self, ingredient: Ingredient) -> None:
        """Remove ingredient from database."""
        if not self.has_ingredient(ingredient):
            raise IngredientNotFound(f"No ingredient {ingredient.name} in database.")

        sql_command  = f'DELETE FROM {self.table_name}'
        sql_command += f" WHERE name == '{ingredient.name}'"
        self.cursor.execute(sql_command)

    def replace_ingredient(self, ingredient: Ingredient) -> None:
        """Replace ingredient in database."""
        self.remove_ingredient(ingredient)
        self.insert(ingredient)

    def has_ingredient(self, purp_ingredient: Ingredient) -> bool:
        """Returns True if the ingredient exists in the database."""
        for ingredient in self.get_list_of_ingredients():
            if purp_ingredient == ingredient:
                return True
        return False

    def has_ingredients(self) -> bool:
        """Return True if database contains at least one ingredient."""
        return any(self.get_list_of_ingredient_names())


class RecipeDatabase(UnencryptedDatabase):
    """Recipe database contains a repository of shared recipes.

    The database is intended to be public and shareable, thus it is not encrypted.
    """

    def __init__(self) -> None:
        """Create new RecipeDatabase."""
        super().__init__(table_name=DatabaseTableName.RECIPES, db_metadata=recipe_metadata)

    def get_list_of_recipe_names(self) -> list:
        """Get list of recipe names."""
        return [name for name, *_ in self.get_list_of_entries()]

    def get_list_of_recipes(self) -> list:
        """Get list of recipes."""
        return [self.get_recipe(name) for name in self.get_list_of_recipe_names()]

    def get_list_of_mealprep_recipes(self) -> list:
        """Get list of mealprep recipes."""
        recipes = [self.get_recipe(name) for name in self.get_list_of_recipe_names()]
        return [recipe for recipe in recipes if recipe.is_mealprep]

    def get_list_of_single_recipes(self) -> list:
        """Get list of single recipes."""
        recipes = [self.get_recipe(name) for name in self.get_list_of_recipe_names()]
        return [recipe for recipe in recipes if not recipe.is_mealprep]

    def get_recipe(self,
                   name   : str,
                   author : str = ''
                   ) -> Recipe:
        """Get Recipe from database by name (and author)."""
        sql_command  =  'SELECT '
        sql_command +=  ', '.join(list(self.db_metadata.keys())[1:])
        sql_command += f' FROM {self.table_name}'
        sql_command += f" WHERE name == '{name}'"

        if author:
            sql_command += f" AND author == '{author}'"

        results = self.cursor.execute(sql_command).fetchall()

        if results:
            for result in results:
                author, in_names, ac_names, is_mealprep = result

                in_names = ([] if in_names == 'None' else
                            in_names.split('\x1f') if '\x1f' in in_names else [in_names])
                ac_names = ([] if ac_names == 'None' else
                            ac_names.split('\x1f') if '\x1f' in ac_names else [ac_names])

                return Recipe(name, author, in_names, ac_names, ast.literal_eval(is_mealprep))

        author_info = f" by '{author}'" if author else ''
        raise RecipeNotFound(f"Could not find recipe '{name}'{author_info}.")

    def insert_recipe(self, recipe: Recipe) -> None:
        """Insert Recipe into the database."""
        keys = list(self.db_metadata.keys())

        values = []
        for key, metadata in self.db_metadata.items():
            value = getattr(recipe, key)

            if metadata[1] == list:
                if not value:
                    value = 'None'
                elif not isinstance(value[0], str):
                    value = '\x1f'.join([v.name for v in value])

            if metadata[1] == bool:
                value = str(value)

            values.append(value)

        sql_command = f'INSERT INTO {self.table_name} ('
        sql_command += ', '.join(keys)
        sql_command += ') VALUES ('
        sql_command += ', '.join(['?' for _ in range(len(keys))])
        sql_command += ')'

        self.cursor.execute(sql_command, values)
        self.cursor.connection.commit()

    def has_recipe(self, recipe: Recipe) -> bool:
        """Returns True if recipe exists in the database."""
        return any(name == recipe.name for name in self.get_list_of_recipe_names())

    def remove_recipe(self, recipe: Recipe) -> None:
        """Remove recipe from database."""
        if not self.has_recipe(recipe):
            raise RecipeNotFound(f"No recipe {recipe.name} in database.")

        sql_command  = f'DELETE FROM {self.table_name}'
        sql_command += f" WHERE name == '{recipe.name}'"
        self.cursor.execute(sql_command)

    def replace_recipe(self, recipe: Recipe) -> None:
        """Replace recipe in database."""
        self.remove_recipe(recipe)
        self.insert_recipe(recipe)


class MealprepDatabase(UnencryptedDatabase):
    """MealprepDatabase database contains a repository of shared mealpreps.

    The database is intended to be public and shareable, thus it is not encrypted.

    While a mealprep is somewhat personal wrt its nutritional content, we assume
    cases where the same OS account is shared for the application, means the users
    also share the same fridge content. Thus, one person cooking a meal into the fridge
    benefits everyone in the household.
    """

    def __init__(self) -> None:
        """Create new MealprepDatabase."""
        super().__init__(table_name=DatabaseTableName.MEALPREPS, db_metadata=mealprep_metadata)

    def get_list_of_mealprep_names(self) -> list:
        """Get list of mealprep names."""
        return [name for name, *_ in self.get_list_of_entries()]

    def get_list_of_mealpreps(self) -> list:
        """Get list of mealpreps."""
        return [self.get_mealprep(name) for name in self.get_list_of_mealprep_names()]

    def get_mealprep(self, name: str) -> Mealprep:
        """Get Recipe from database by name."""
        sql_command  =  'SELECT '
        sql_command +=  ', '.join(list(self.db_metadata.keys())[1:])
        sql_command += f' FROM {self.table_name}'
        sql_command += f" WHERE recipe_name == '{name}'"

        result = self.cursor.execute(sql_command).fetchall()[0]

        if result:
            total_grams      = result[0]
            cook_date        = result[1]
            ingredient_grams = ast.literal_eval(result[2])
            mealprep_nv      = NutritionalValues.from_serialized(result[3])
            return Mealprep(name, total_grams, cook_date, ingredient_grams, mealprep_nv)

        raise RecipeNotFound(f"Could not find recipe '{name}'.")

    def insert_mealprep(self, mealprep: Mealprep) -> None:
        """Insert Mealprep into the database."""
        keys = list(self.db_metadata.keys())

        values = []
        for key in self.db_metadata:
            value = getattr(mealprep, key)
            if isinstance(value, dict):
                value = str(value)
            elif isinstance(value, NutritionalValues):
                value = value.serialize()
            values.append(value)

        sql_command = f'INSERT INTO {self.table_name} ('
        sql_command += ', '.join(keys)
        sql_command += ') VALUES ('
        sql_command += ', '.join(['?' for _ in range(len(keys))])
        sql_command += ')'

        self.cursor.execute(sql_command, values)
        self.cursor.connection.commit()

    def has_mealprep(self, mealprep: Mealprep) -> bool:
        """Returns True if the mealprep exists in the database."""
        return any(name == mealprep.recipe_name for name in self.get_list_of_mealprep_names())

    def remove_mealprep(self, mealprep: Mealprep) -> None:
        """Remove mealprep from the database."""
        if not self.has_mealprep(mealprep):
            raise RecipeNotFound(f"No mealprep {mealprep.recipe_name} in database.")

        sql_command  = f'DELETE FROM {self.table_name}'
        sql_command += f" WHERE recipe_name == '{mealprep.recipe_name}'"
        self.cursor.execute(sql_command)

    def replace_mealprep(self, mealprep: Mealprep) -> None:
        """Replace mealprep in the database."""
        self.remove_mealprep(mealprep)
        self.insert_mealprep(mealprep)
