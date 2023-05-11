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


recipe_metadata = {
    'name':                ('Name',                str),
    'author':              ('Author',              str),
    'ingredient_names':    ('IngredientNames',    list),
    'accompaniment_names': ('AccompanimentNames', list),
}


class Recipe:
    """Recipe contains metadata about a recipe and its ingredients."""

    def __init__(self,
                 name                : str,
                 author              : str,
                 ingredient_names    : list,
                 accompaniment_names : list,
                 ) -> None:
        """Create new Recipe object."""
        self.name                = name
        self.author              = author
        self.ingredient_names    = ingredient_names
        self.accompaniment_names = accompaniment_names

    def __eq__(self, other: Any) -> bool:
        """Return True if two Recipes are equal."""
        if not isinstance(other, Recipe):
            return False
        return self.name == other.name and self.author == other.author

    def __ne__(self, other: Any) -> bool:
        """Return True if two Recipes are not equal."""
        return not self.__eq__(other)

    def __str__(self) -> str:
        """Identifying version of the Recipe"""
        return f'{self.name} (by {self.author})'

    def __repr__(self) -> str:
        """Format Ingredient attributes."""
        lines = [f"<Recipe-object {id(self)}>",
                 f'  <name>       : {self.name}',
                 f'  <author>     : {self.author}',
                 '  <ingredients>:']
        for ingredient in self.ingredient_names:
            lines.append(f'    {ingredient.name}')
        return '\n'.join(lines)
