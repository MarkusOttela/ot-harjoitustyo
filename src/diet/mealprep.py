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
import datetime

mealprep_metadata = {
    'recipe_name':      ('RecipeName',      str),
    'ingredient_grams': ('IngredientGrams', list),
}


class Mealprep:
    """Mealprep object is an object that contains a cooked instances of a Recipe that is

    1) Larger than one portion and thus
    2) Something from which multiple portions can be taken
    """

    def __init__(self,
                 recipe_name      : str,
                 ingredient_grams : dict,
                 cook_date        : datetime.date
                 ) -> None:
        """Create new Mealprep object."""
        self.recipe_name      = recipe_name
        self.ingredient_grams = ingredient_grams
        self.cook_date        = cook_date

    def __str__(self) -> str:
        """Return string-representation of the Mealprep"""
        return self.recipe_name
