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

import sqlite3


from src.common.exceptions import IngredientNotFound, RecipeNotFound
from src.common.statics    import DatabaseFileName, Directories, DatabaseTableName
from src.common.utils      import ensure_dir
from src.common.validation import validate_params
from src.common.types      import DatabaseTypes

from src.diet.ingredient import Ingredient, ingredient_metadata
from src.diet.recipe     import Recipe, recipe_metadata


column_type_dict : dict = {
    str   : DatabaseTypes.TEXT.value,
    float : DatabaseTypes.REAL.value,
    list  : DatabaseTypes.TEXT.value
}


class UnencryptedDatabase:
    """UnencryptedDatabase is an SQLite3 database for storing non-sensitive data.

    The database is intended to be public and shareable, thus it is not encrypted.
    """

    def __init__(self, table_name: DatabaseTableName, db_metadata : dict) -> None:
        """Create new UnencryptedDatabase object."""
        ensure_dir(Directories.USERDATA.value)
        self.table_name  = table_name.value
        self.db_metadata = db_metadata
        self.connection  = sqlite3.connect(f'{Directories.USERDATA.value}'
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

    def insert(self, ingredient: Ingredient) -> None:
        """Insert Ingredient into the database."""

        ingredient_keys   = list(ingredient_metadata.keys())
        ingredient_values = [getattr(ingredient, key) for key in ingredient_keys]

        sql_command = f'INSERT INTO {self.table_name} ('
        sql_command += ', '.join(ingredient_keys)
        sql_command += ') VALUES ('
        sql_command += ', '.join(['?' for _ in range(len(ingredient_keys))])
        sql_command += ')'

        self.cursor.execute(sql_command, ingredient_values)
        self.cursor.connection.commit()

    def get_list_of_entries(self) -> list:
        """Get list of entries in the database."""
        sql_command  =  'SELECT '
        sql_command +=  ', '.join(list(self.db_metadata.keys()))
        sql_command += f' FROM {self.table_name}'

        results = self.cursor.execute(sql_command).fetchall()
        return results


class IngredientDatabase(UnencryptedDatabase):

    def __init__(self) -> None:
        super().__init__(table_name=DatabaseTableName.INGREDIENTS, db_metadata=ingredient_metadata)

    def get_list_of_ingredients(self) -> list:
        """Get list of ingredients."""
        return [Ingredient(*data) for data in self.get_list_of_entries()]

    def get_ingredient(self,
                       name         : str,
                       manufacturer : str = ''
                       ) -> Ingredient:
        """Get Ingredient from database by name (and manufacturer)."""
        validate_params(self.get_ingredient, locals())

        sql_command  =  'SELECT '
        sql_command +=  ', '.join(list(self.db_metadata.keys())[1:])
        sql_command += f' FROM {self.table_name}'
        sql_command += f" WHERE {self.db_metadata['name'][0]} == '{name}'"

        if manufacturer:
            manuf_col    = 'manufacturer'
            sql_command += f" AND {manuf_col} == '{manufacturer}'"

        results = self.cursor.execute(sql_command).fetchall()

        if results:
            return Ingredient(name, *results[0])

        manuf_info = f" by '{manufacturer}'" if manufacturer else ''
        raise IngredientNotFound(f"Could not find ingredient '{name}'{manuf_info}.")

    def remove_ingredient(self, ingredient: Ingredient) -> None:
        """Remove ingredient from database."""
        if not self.has_ingredient(ingredient):
            raise IngredientNotFound(f"No ingredient {ingredient.name} in database.")

        sql_command  = f'DELETE FROM {self.table_name}'
        sql_command += f" WHERE {self.db_metadata['name'][0]} == '{ingredient.name}'"
        self.cursor.execute(sql_command)

    def replace_ingredient(self, ingredient: Ingredient) -> None:
        """Replace ingredient in database."""
        self.remove_ingredient(ingredient)
        self.insert(ingredient)

    def has_ingredient(self, ingredient: Ingredient) -> bool:
        """Returns True if ingredient exists in the database."""
        return any(i == ingredient for i in self.get_list_of_ingredients())


class RecipeDatabase(UnencryptedDatabase):
    """Recipe database contains a repository of shared recipes.

    The database is intended to be public and shareable, thus it is not encrypted.
    """

    def __init__(self) -> None:
        super().__init__(table_name=DatabaseTableName.RECIPES, db_metadata=recipe_metadata)

    def get_list_of_recipe_names(self) -> list:
        """Get list of recipe n ames."""
        return [name for name, author, ser_ingredient_names in self.get_list_of_entries()]

    def get_list_of_recipes(self) -> list:
        """Get list of recipe n ames."""
        return [self.get_recipe(name) for name in self.get_list_of_recipe_names()]

    def get_recipe(self,
                   name   : str,
                   author : str = ''
                   ) -> Recipe:
        """Get Recipe from database by name (and author)."""
        validate_params(self.get_recipe, locals())

        sql_command  =  'SELECT '
        sql_command +=  ', '.join(list(self.db_metadata.keys())[1:])
        sql_command += f' FROM {self.table_name}'
        sql_command += f" WHERE {self.db_metadata['name'][0]} == '{name}'"

        if author:
            author_col   = 'author'
            sql_command += f" AND {author_col} == '{author}'"

        results = self.cursor.execute(sql_command).fetchall()

        if results:
            for result in results:
                author, ingredients = result
                if '\x1f' in ingredients:
                    ingredients = ingredients.split('\x1f')
                else:
                    ingredients = [ingredients]
                return Recipe(name, author, ingredients)

        manuf_info = f" by '{author}'" if author else ''
        raise RecipeNotFound(f"Could not find recipe '{name}'{manuf_info}.")

    def insert_recipe(self, recipe: Recipe) -> None:
        """Insert Recipe into the database."""
        keys = list(self.db_metadata.keys())

        values = []
        for key in self.db_metadata:
            value = getattr(recipe, key)
            if self.db_metadata[key][1] == list:
                value = '\x1f'.join([v.name for v in value])
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
        sql_command += f" WHERE {self.db_metadata['name'][0]} == '{recipe.name}'"
        self.cursor.execute(sql_command)

    def replace_recipe(self, recipe: Recipe) -> None:
        """Replace recipe in database."""
        self.remove_recipe(recipe)
        self.insert_recipe(recipe)
