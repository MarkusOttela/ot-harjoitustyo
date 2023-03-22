#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

"""
Calorinator - Diet tracker
Copyright (C) Markus Ottela

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

from enum   import Enum
from typing import Any

from src.common.exceptions import IngredientNotFound
from src.common.statics    import DatabaseFileNames, Directories
from src.common.types      import NonEmptyStr, NonNegativeFloat, DatabaseTypes
from src.common.utils      import ensure_dir
from src.common.validation import validate_params
from src.diet.ingredient   import Ingredient, ingredient_metadata


column_type_dict : dict[Any, str] = {
    str              : DatabaseTypes.TEXT.value,
    NonEmptyStr      : DatabaseTypes.TEXT.value,
    NonNegativeFloat : DatabaseTypes.REAL.value,
    float            : DatabaseTypes.REAL.value
}


class IngredientDB(Enum):
    """Ingredient database literals."""
    table_name = 'Ingredients'


class IngredientDatabase:

    def __init__(self) -> None:
        """Create new IngredientDatabase object."""
        ensure_dir(f'{Directories.USERDATA.value}/')
        path_to_db = f'{Directories.USERDATA.value}/{DatabaseFileNames.INGREDIENT_DATABASE.value}'
        self.connection = sqlite3.connect(path_to_db)

        self.cursor = self.connection.cursor()
        self.connection.isolation_level = None
        self.create_table()

    def create_table(self) -> None:
        """Create the database table procedurally from Enum fields."""
        sql_command = f'CREATE TABLE IF NOT EXISTS {IngredientDB.table_name.value} ('

        for key in ingredient_metadata.keys():
            tup          = ingredient_metadata[key]
            column_name  = key
            sql_command += f"{column_name} {column_type_dict[tup[1]]}, "

        sql_command  = sql_command[:-2]  # Remove trailing comma and space
        sql_command += ')'

        self.cursor.execute(sql_command)

    def insert(self, ingredient: Ingredient) -> None:
        """Insert Ingredient into the database."""

        ingredient_keys   = list(ingredient_metadata.keys())
        ingredient_values = [getattr(ingredient, key) for key in ingredient_keys]

        sql_command = f'INSERT INTO {IngredientDB.table_name.value} ('
        sql_command += ', '.join(ingredient_keys)
        sql_command += ') VALUES ('
        sql_command += ', '.join(['?' for _ in range(len(ingredient_keys))])
        sql_command += ')'

        self.cursor.execute(sql_command, ingredient_values)
        self.cursor.connection.commit()

    def get_ingredient(self,
                       name         : NonEmptyStr,
                       manufacturer : str = ''
                       ) -> Ingredient:
        """Get Ingredient from database by name (and manufacturer)."""
        validate_params(self.get_ingredient, locals())

        sql_command  = f'SELECT '
        sql_command += f', '.join(list(ingredient_metadata.keys())[1:])
        sql_command += f' FROM {IngredientDB.table_name.value}'
        sql_command += f" WHERE {ingredient_metadata['name'][0]} == '{name}'"

        if manufacturer:
            manuf_col    = 'manufacturer'
            sql_command += f" AND {manuf_col} == '{manufacturer}'"

        results = self.cursor.execute(sql_command).fetchall()

        if results:
            return Ingredient(name, *results[0])
        else:
            manuf_info = f" by '{manufacturer}'" if manufacturer else ''
            raise IngredientNotFound(f"Could not find ingredient '{name}'{manuf_info}.")
