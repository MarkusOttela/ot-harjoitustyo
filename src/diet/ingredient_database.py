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

from src.common.statics import DatabaseFileNames


class IngredientDB(Enum):
    """Ingredient database literals."""
    table_name      = 'Ingredients'
    name            = 'name'
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
                 name : str,

                 # Energy
                 kcal          : float = 0,

                 # Macronutrients
                 carbohydrates : float = 0,
                 protein       : float = 0,
                 fat           : float = 0,
                 satisfied_fat : float = 0,
                 fiber         : float = 0,
                 salt          : float = 0
                 ) -> None:
        """Create new Ingredient.

        Macronutrients are given in grams / 100g.
        """
        self.name          = name
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
                f"  * {self.name          = }\n"
                f"  * {self.kcal          = }\n"
                f"  * {self.carbohydrates = }\n"
                f"  * {self.protein       = }\n"
                f"  * {self.fat           = }\n"
                f"  * {self.satisfied_fat = }\n"
                f"  * {self.fiber         = }\n"
                f"  * {self.salt          = }\n")


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
                            f"{IngredientDB.name.value} TEXT, "
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
               ingredient_name : str,
               kcal            : float,
               carbohydrates   : float,
               protein         : float,
               fat             : float,
               satisfied_fat   : float,
               fiber           : float,
               salt            : float,
               ) -> None:
        """Insert into database."""
        self.cursor.execute(f"INSERT INTO {IngredientDB.table_name.value} ("
                            f"{IngredientDB.name.value}, "
                            f"{IngredientDB.kcal.value           }, "
                            f"{IngredientDB.carbohydrates.value  }, "
                            f"{IngredientDB.protein.value        }, "
                            f"{IngredientDB.fat.value            }, "
                            f"{IngredientDB.satisfied_fat.value  }, "
                            f"{IngredientDB.fiber.value          }, "
                            f"{IngredientDB.salt.value           }"
                            f") VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (ingredient_name, kcal, carbohydrates, protein, fat, satisfied_fat, fiber, salt)
                            )
        self.cursor.connection.commit()

    def get_ingredient_by_name(self, name: str) -> Ingredient:
        """Get ingredient from database by name."""

        kcal, carbohydrates, protein, fat, satisfied_fat, fiber, salt \
            = self.cursor.execute(f"SELECT "
                                  f"{IngredientDB.kcal.value         }, "
                                  f"{IngredientDB.carbohydrates.value}, "
                                  f"{IngredientDB.protein.value      }, "
                                  f"{IngredientDB.fat.value          }, "
                                  f"{IngredientDB.satisfied_fat.value}, "
                                  f"{IngredientDB.fiber.value        }, "
                                  f"{IngredientDB.salt.value         } "
                                  f"FROM {IngredientDB.table_name.value} "
                                  f"WHERE {IngredientDB.name.value} == '{name}'"
                                  ).fetchone()
        return Ingredient(name, kcal, carbohydrates, protein, fat, satisfied_fat, fiber, salt)


if __name__ == '__main__':

    # Testing code

    try:
        import os
        os.remove('ingredient_database.sqlite3')
        time.sleep(0.1)
    except FileNotFoundError:
        pass

    db = IngredientDatabase()
    db.insert(ingredient_name='Nacho',
              kcal=100.1,
              carbohydrates=1,
              protein=1,
              fat=1,
              satisfied_fat=1,
              fiber=1,
              salt=1)

    ingredient = db.get_ingredient_by_name('Nacho')
    print(repr(ingredient))
