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
from src.common.types      import NonEmptyStr, NonNegativeFloat
from src.common.validation import validate_params


class IngredientDB(Enum):
    """Ingredient database literals."""
    table_name      = 'Ingredients'

    # Columns
    name            = 'name'
    manufacturer    = 'manufacturer'
    kcal            = 'kcal'
    carbohydrates   = 'carbohydrates'
    protein         = 'protein'
    fat             = 'fat'
    satisfied_fat   = 'satisfied_fat'
    fiber           = 'fiber'
    salt            = 'salt'


class Ingredient:
    """\
    Food ingredient is an object that represents something drinks, servings,
    and mealpreps are cooked from.
    """
    def __init__(self,
                 name         : NonEmptyStr,
                 manufacturer : str = '',

                 # Energy
                 kcal          : NonNegativeFloat = 0.0,

                 # Macronutrients
                 carbohydrates : NonNegativeFloat = 0.0,
                 protein       : NonNegativeFloat = 0.0,
                 fat           : NonNegativeFloat = 0.0,
                 satisfied_fat : NonNegativeFloat = 0.0,
                 fiber         : NonNegativeFloat = 0.0,
                 salt          : NonNegativeFloat = 0.0
                 ) -> None:
        """Create new Ingredient.

        Macronutrients are given in grams / 100g.
        """
        validate_params(self.__init__, locals())

        self.name          = name
        self.manufacturer  = manufacturer

        self.kcal          = kcal
        self.carbohydrates = carbohydrates
        self.protein       = protein
        self.fat           = fat
        self.satisfied_fat = satisfied_fat
        self.fiber         = fiber
        self.salt          = salt

    def __repr__(self) -> str:
        """Format Ingredient attributes."""
        return (f"<Ingredient-object {id(self)}>\n"
                f"  <{self.name          = }>\n"
                f"  <{self.manufacturer  = }>\n"
                f"  <{self.kcal          = }>\n"
                f"  <{self.carbohydrates = }>\n"
                f"  <{self.protein       = }>\n"
                f"  <{self.fat           = }>\n"
                f"  <{self.satisfied_fat = }>\n"
                f"  <{self.fiber         = }>\n"
                f"  <{self.salt          = }>\n")


class IngredientDatabase:

    def __init__(self) -> None:
        """Create new IngredientDatabase object."""
        self.connection = sqlite3.connect(DatabaseFileNames.INGREDIENT_DATABASE.value)
        self.cursor     = self.connection.cursor()
        self.connection.isolation_level = None
        self.create_table()

    def create_table(self) -> None:
        """Create the database table."""
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {IngredientDB.table_name.value} ("
                            f"{IngredientDB.name.value           } TEXT, "
                            f"{IngredientDB.manufacturer.value   } TEXT, "
                            f"{IngredientDB.kcal.value           } REAL, "
                            f"{IngredientDB.carbohydrates.value  } REAL, "
                            f"{IngredientDB.protein.value        } REAL, "
                            f"{IngredientDB.fat.value            } REAL, "
                            f"{IngredientDB.satisfied_fat.value  } REAL, "
                            f"{IngredientDB.fiber.value          } REAL, "
                            f"{IngredientDB.salt.value           } REAL"
                            ")")

    def insert(self,
               *,  # Require keyword args
               name          : NonEmptyStr,
               manufacturer  : str = '',
               kcal          : NonNegativeFloat,
               carbohydrates : NonNegativeFloat,
               protein       : NonNegativeFloat,
               fat           : NonNegativeFloat,
               satisfied_fat : NonNegativeFloat,
               fiber         : NonNegativeFloat,
               salt          : NonNegativeFloat,
               ) -> None:
        """Insert into database."""
        validate_params(self.insert, locals())

        self.cursor.execute(f"INSERT INTO {IngredientDB.table_name.value} ("
                            f"{IngredientDB.name.value}, "
                            f"{IngredientDB.manufacturer.value}, "
                            f"{IngredientDB.kcal.value           }, "
                            f"{IngredientDB.carbohydrates.value  }, "
                            f"{IngredientDB.protein.value        }, "
                            f"{IngredientDB.fat.value            }, "
                            f"{IngredientDB.satisfied_fat.value  }, "
                            f"{IngredientDB.fiber.value          }, "
                            f"{IngredientDB.salt.value           }"
                            f") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (name, manufacturer, kcal, carbohydrates, protein, fat, satisfied_fat, fiber, salt)
                            )
        self.cursor.connection.commit()

    def get_ingredient_by_name(self,
                               name: NonEmptyStr
                               ) -> Ingredient:
        """Get ingredient from database by name."""
        validate_params(self.get_ingredient_by_name, locals())

        results = self.cursor.execute(f"SELECT "
                                  f"{IngredientDB.manufacturer.value }, "
                                  f"{IngredientDB.kcal.value         }, "
                                  f"{IngredientDB.carbohydrates.value}, "
                                  f"{IngredientDB.protein.value      }, "
                                  f"{IngredientDB.fat.value          }, "
                                  f"{IngredientDB.satisfied_fat.value}, "
                                  f"{IngredientDB.fiber.value        }, "
                                  f"{IngredientDB.salt.value         } "
                                  f"FROM {IngredientDB.table_name.value} "
                                  f"WHERE {IngredientDB.name.value} == '{name}'"
                                  ).fetchall()
        if results:
            return Ingredient(name, *results[0])
        else:
            raise IngredientNotFound(f"Could not find ingredient '{name}'.")


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

    ingredient = db.get_ingredient_by_name('Nacho')
    print(repr(ingredient))
