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

from typing import Any

from src.entities.nutritional_values import NutritionalValues


mealprep_metadata = {
    'recipe_name':      ('RecipeName',      str  ),
    'total_grams':      ('TotalGrams',      float),
    'cook_date':        ('CookDate',        str  ),
    'ingredient_grams': ('IngredientGrams', list ),
    'mealprep_nv':      ('MealprepNV',      str  ),
}


class Mealprep:
    """Mealprep object is an object that contains a cooked instances of a Recipe that is

    1) Larger than one portion and thus
    2) Something from which multiple portions can be taken

    The total grams is not tied to the amount of ingredient grams, because the amount of
    water will vary depending on how much is added, and how much evaporates during the
    cooking process. Weighing the final mealprep will ensure correct estimation of
    nutrient density.
    """

    def __init__(self,
                 recipe_name      : str,
                 total_grams      : float,
                 cook_date        : str,
                 ingredient_grams : dict,
                 mealprep_nv      : NutritionalValues
                 ) -> None:
        """Create new Mealprep object."""
        self.recipe_name      = recipe_name
        self.total_grams      = total_grams
        self.cook_date        = cook_date
        self.ingredient_grams = ingredient_grams
        self.mealprep_nv      = mealprep_nv / self.total_grams

    def __eq__(self, other: Any) -> bool:
        """Returns True if the two Mealpreps are the same"""
        if not isinstance(other, Mealprep):
            return False
        return self.recipe_name == other.recipe_name

    def __ne__(self, other: Any) -> bool:
        """Returns True if the two Mealpreps are not the same."""
        return not self.__eq__(other)

    def __str__(self) -> str:
        """Return string-representation of the Mealprep."""
        return f'{self.recipe_name} ({self.cook_date})'

    def __repr__(self) -> str:
        """Format Mealprep attributes."""
        string = (f'<Mealprep-object {id(self)}>\n'
                  f'  Cook_date: {self.cook_date}\n'
                  f'  Grams:     {self.total_grams}\n'
                  '   Ingredients:')
        for ingredient, grams in self.ingredient_grams.items():
            string += f'    {ingredient}: {grams}g'
        return string

    def get_nv(self, for_grams: float) -> NutritionalValues:
        """Get the nutritional values of the mealprep for portion grams."""
        return self.mealprep_nv * for_grams
