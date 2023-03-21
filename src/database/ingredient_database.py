#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

"""
Calorienator - Diet tracker
Copyright (C) Markus Ottela

This file is part of Calorienator.
Calorienator is free software: you can redistribute it and/or modify it under the 
terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version. Calorienator is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
details. You should have received a copy of the GNU General Public License
along with Calorienator. If not, see <https://www.gnu.org/licenses/>.
"""

import sqlite3
import time

from enum import Enum

from src.common.exceptions import IngredientNotFound
from src.common.statics    import DatabaseFileNames
from src.common.types      import NonEmptyStr, NonNegativeFloat, DatabaseTypes
from src.common.validation import validate_params
from src.diet.ingredient   import Ingredient, IngredientMetadata


column_type_dict = {
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
        self.connection = sqlite3.connect(DatabaseFileNames.INGREDIENT_DATABASE.value)
        self.cursor     = self.connection.cursor()
        self.connection.isolation_level = None
        self.create_table()

    def create_table(self) -> None:
        """Create the database table procedurally from Enum fields."""
        sql_command = f'CREATE TABLE IF NOT EXISTS {IngredientDB.table_name.value} ('

        for enum in IngredientMetadata:
            tup          = enum.value
            column_name  = tup[0]
            sql_command += f"{column_name} {column_type_dict[tup[2]]}, "

        sql_command  = sql_command[:-2]  # Remove trailing comma and space
        sql_command += ')'

        self.cursor.execute(sql_command)

    def insert(self, ingredient: Ingredient) -> None:
        """Insert Ingredient into the database."""

        ingredient_keys   = [enum.value[0]            for enum in IngredientMetadata]
        ingredient_values = [getattr(ingredient, key) for key  in ingredient_keys]

        sql_command = f'INSERT INTO {IngredientDB.table_name.value} ('
        sql_command += ', '.join(ingredient_keys)
        sql_command += ') VALUES ('
        sql_command += ', '.join(['?' for _ in range(len(IngredientMetadata))])
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
        sql_command += f', '.join([enum.value[0] for enum in IngredientMetadata][1:])
        sql_command += f' FROM {IngredientDB.table_name.value}'
        sql_command += f" WHERE {IngredientMetadata.name.value[0]} == '{name}'"

        if manufacturer:
            manuf_col    = IngredientMetadata.manufacturer.value[0]
            sql_command += f" AND {manuf_col} == '{manufacturer}'"

        results = self.cursor.execute(sql_command).fetchall()

        if results:
            return Ingredient(name, *results[0])
        else:
            manuf_info = f" by '{manufacturer}'" if manufacturer else ''
            raise IngredientNotFound(f"Could not find ingredient '{name}'{manuf_info}.")


if __name__ == '__main__':

    # Testing code

    try:
        import os
        os.remove('ingredient_database.sqlite3')
        time.sleep(0.1)
    except FileNotFoundError:
        pass

    db = IngredientDatabase()
    db.insert(name='Nacho',
              manufacturer='Atria',
              kcal=100.1,
              carbohydrates=1.0,
              protein=1.0,
              fat=1.0,
              satisfied_fat=1.0,
              fiber=1.0,
              salt=1.0)

    ingredient_ = db.get_ingredient('Nacho', manufacturer='Atria')
    print(repr(ingredient_))
