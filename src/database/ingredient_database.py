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

from enum import Enum

from src.common.exceptions import IngredientNotFound
from src.common.statics    import DatabaseFileNames, Directories
from src.common.utils      import ensure_dir
from src.common.validation import validate_params
from src.diet.ingredient   import Ingredient, ingredient_metadata
from src.common.types      import DatabaseTypes


column_type_dict : dict = {
    str   : DatabaseTypes.TEXT.value,
    float : DatabaseTypes.REAL.value
}


class IngredientDB(Enum):
    """Ingredient database literals."""
    TABLE_NAME = 'Ingredients'


class IngredientDatabase:
    """IngredientDatabase is an SQLite3 database for storing ingredient related metadata.

    The database is intended to be public and shareable, thus it is not encrypted.
    """

    def __init__(self) -> None:
        """Create new IngredientDatabase object."""
        ensure_dir(Directories.USERDATA.value)
        path_to_db = f'{Directories.USERDATA.value}/{DatabaseFileNames.INGREDIENT_DATABASE.value}'
        self.connection = sqlite3.connect(path_to_db)

        self.table = IngredientDB.TABLE_NAME.value

        self.cursor = self.connection.cursor()
        self.connection.isolation_level = None
        self.create_table()

    def create_table(self) -> None:
        """Create the database table procedurally."""
        sql_command = f'CREATE TABLE IF NOT EXISTS {self.table} ('

        for key, value in ingredient_metadata.items():
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

        sql_command = f'INSERT INTO {self.table} ('
        sql_command += ', '.join(ingredient_keys)
        sql_command += ') VALUES ('
        sql_command += ', '.join(['?' for _ in range(len(ingredient_keys))])
        sql_command += ')'

        self.cursor.execute(sql_command, ingredient_values)
        self.cursor.connection.commit()

    def has_ingredient(self, ingredient: Ingredient) -> bool:
        """Returns True if ingredient exists in the database."""
        return any(i == ingredient for i in self.get_list_of_ingredients())

    def get_list_of_ingredients(self) -> list:
        """Get list of Ingredients in the database."""
        sql_command  =  'SELECT '
        sql_command +=  ', '.join(list(ingredient_metadata.keys()))
        sql_command += f' FROM {self.table}'

        results     = self.cursor.execute(sql_command).fetchall()
        ingredients = [Ingredient(*data) for data in results]
        return ingredients

    def get_ingredient(self,
                       name         : str,
                       manufacturer : str = ''
                       ) -> Ingredient:
        """Get Ingredient from database by name (and manufacturer)."""
        validate_params(self.get_ingredient, locals())

        sql_command  =  'SELECT '
        sql_command +=  ', '.join(list(ingredient_metadata.keys())[1:])
        sql_command += f' FROM {self.table}'
        sql_command += f" WHERE {ingredient_metadata['name'][0]} == '{name}'"

        if manufacturer:
            manuf_col    = 'manufacturer'
            sql_command += f" AND {manuf_col} == '{manufacturer}'"

        results = self.cursor.execute(sql_command).fetchall()

        if results:
            return Ingredient(name, *results[0])

        manuf_info = f" by '{manufacturer}'" if manufacturer else ''
        raise IngredientNotFound(f"Could not find ingredient '{name}'{manuf_info}.")

    def remove(self, ingredient: Ingredient) -> None:
        """Remove ingredient from database."""
        if not self.has_ingredient(ingredient):
            raise IngredientNotFound(f"No ingredient {ingredient.name} in database.")

        sql_command  = f'DELETE FROM {self.table}'
        sql_command += f" WHERE {ingredient_metadata['name'][0]} == '{ingredient.name}'"
        self.cursor.execute(sql_command)

    def replace(self, ingredient: Ingredient) -> None:
        """Replace ingredient in database."""
        self.remove(ingredient)
        self.insert(ingredient)
