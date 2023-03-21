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

from src.common.Exceptions import IngredientNotFound
from src.common.statics    import DatabaseFileNames
from src.common.types      import NonEmptyStr, NonNegativeFloat, DatabaseTypes
from src.common.validation import validate_params
from src.diet.ingredient   import Ingredient


column_type_dict = {
    str              : DatabaseTypes.TEXT.value,
    NonEmptyStr      : DatabaseTypes.TEXT.value,
    NonNegativeFloat : DatabaseTypes.REAL.value,
    float            : DatabaseTypes.REAL.value
}


class IngredientDB(Enum):
    """Ingredient database literals."""
    table_name      = 'Ingredients'


class IngredientDBCol(Enum):
    """Ingredient database Columns and their types."""
    # Columns
    name            = ('name',         NonEmptyStr)
    manufacturer    = ('manufacturer', str)

    # Macronutrients
    kcal            = ('kcal',          NonNegativeFloat)
    carbohydrates   = ('carbohydrates', NonNegativeFloat)
    protein         = ('protein',       NonNegativeFloat)
    fat             = ('fat',           NonNegativeFloat)
    satisfied_fat   = ('satisfied_fat', NonNegativeFloat)
    fiber           = ('fiber',         NonNegativeFloat)
    salt            = ('salt',          NonNegativeFloat)

    # Micronutrients

    # Omega-3 fatty acids
    omega3_dha = ('omega3_dha', NonNegativeFloat)
    omega3_epa = ('omega3_epa', NonNegativeFloat)

    # Fat soluble vitamins
    vitamin_a = ('vitamin_a', NonNegativeFloat)
    vitamin_d = ('vitamin_d', NonNegativeFloat)
    vitamin_e = ('vitamin_e', NonNegativeFloat)
    vitamin_k = ('vitamin_k', NonNegativeFloat)

    # Water soluble vitamins
    vitamin_b1  = ('vitamin_b1',  NonNegativeFloat)
    vitamin_b2  = ('vitamin_b2',  NonNegativeFloat)
    vitamin_b3  = ('vitamin_b3',  NonNegativeFloat)
    vitamin_b5  = ('vitamin_b5',  NonNegativeFloat)
    vitamin_b6  = ('vitamin_b6',  NonNegativeFloat)
    vitamin_b7  = ('vitamin_b7',  NonNegativeFloat)
    vitamin_b9  = ('vitamin_b9',  NonNegativeFloat)
    vitamin_b12 = ('vitamin_b12', NonNegativeFloat)
    vitamin_c   = ('vitamin_c',   NonNegativeFloat)

    # Minerals etc.
    calcium   = ('calcium',   NonNegativeFloat)
    chromium  = ('chromium',  NonNegativeFloat)
    iodine    = ('iodine',    NonNegativeFloat)
    potassium = ('potassium', NonNegativeFloat)
    iron      = ('iron',      NonNegativeFloat)
    magnesium = ('magnesium', NonNegativeFloat)
    zinc      = ('zinc',      NonNegativeFloat)
    caffeine  = ('caffeine',  NonNegativeFloat)
    creatine  = ('creatine',  NonNegativeFloat)


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

        for enum in IngredientDBCol:
            tup          = enum.value
            column_name  = tup[0]
            sql_command += f"{column_name} {column_type_dict[tup[1]]}, "

        sql_command  = sql_command [:-2]  # Remove trailing comma and space
        sql_command += ')'

        self.cursor.execute(sql_command)

    def insert(self,
               *                                     ,  # Require keyword args
               name          : NonEmptyStr           ,
               manufacturer  : str              = '' ,
               kcal          : NonNegativeFloat = 0.0,
               carbohydrates : NonNegativeFloat = 0.0,
               protein       : NonNegativeFloat = 0.0,
               fat           : NonNegativeFloat = 0.0,
               satisfied_fat : NonNegativeFloat = 0.0,
               fiber         : NonNegativeFloat = 0.0,
               salt          : NonNegativeFloat = 0.0,

               # Micronutrients

               # Omega-3 fatty acids
               omega3_dha: NonNegativeFloat = 0.0,
               omega3_epa: NonNegativeFloat = 0.0,

               # Fat soluble vitamins
               vitamin_a: NonNegativeFloat = 0.0,
               vitamin_d: NonNegativeFloat = 0.0,
               vitamin_e: NonNegativeFloat = 0.0,
               vitamin_k: NonNegativeFloat = 0.0,

               # Water soluble vitamins
               vitamin_b1:  NonNegativeFloat = 0.0,
               vitamin_b2:  NonNegativeFloat = 0.0,
               vitamin_b3:  NonNegativeFloat = 0.0,
               vitamin_b5:  NonNegativeFloat = 0.0,
               vitamin_b6:  NonNegativeFloat = 0.0,
               vitamin_b7:  NonNegativeFloat = 0.0,
               vitamin_b9:  NonNegativeFloat = 0.0,
               vitamin_b12: NonNegativeFloat = 0.0,
               vitamin_c:   NonNegativeFloat = 0.0,

               # Minerals etc.
               calcium   : NonNegativeFloat = 0.0,
               chromium  : NonNegativeFloat = 0.0,
               iodine    : NonNegativeFloat = 0.0,
               potassium : NonNegativeFloat = 0.0,
               iron      : NonNegativeFloat = 0.0,
               magnesium : NonNegativeFloat = 0.0,
               zinc      : NonNegativeFloat = 0.0,
               caffeine  : NonNegativeFloat = 0.0,
               creatine  : NonNegativeFloat = 0.0,
               ) -> None:
        """Insert Ingredient into the database."""
        validate_params(self.insert, locals())

        sql_command = f'INSERT INTO {IngredientDB.table_name.value} ('
        sql_command += ', '.join([enum.value[0] for enum in IngredientDBCol])
        sql_command += ') VALUES ('
        sql_command += ', '.join(['?' for _ in range(len(IngredientDBCol))])
        sql_command += ')'

        self.cursor.execute(sql_command,
                            (name, manufacturer, kcal,
                             carbohydrates, protein, fat, satisfied_fat, fiber, salt,
                             omega3_dha, omega3_epa,
                             vitamin_a, vitamin_d, vitamin_e, vitamin_k,
                             vitamin_b1, vitamin_b2, vitamin_b3, vitamin_b5,
                             vitamin_b6, vitamin_b7, vitamin_b9, vitamin_b12, vitamin_c,
                             calcium, chromium, iodine, potassium, iron, magnesium, zinc, caffeine, creatine))

        self.cursor.connection.commit()

    def get_ingredient(self,
                       name         : NonEmptyStr,
                       manufacturer : str = ''
                       ) -> Ingredient:
        """Get Ingredient from database by name (and manufacturer)."""
        validate_params(self.get_ingredient, locals())

        sql_command  = f'SELECT '
        sql_command += f', '.join([enum.value[0] for enum in IngredientDBCol][1:])
        sql_command += f' FROM {IngredientDB.table_name.value}'
        sql_command += f" WHERE {IngredientDBCol.name.value[0]} == '{name}'"

        if manufacturer:
            manuf_col    = IngredientDBCol.manufacturer.value[0]
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

    ingredient = db.get_ingredient('Nacho', manufacturer='Atria')
    print(repr(ingredient))
