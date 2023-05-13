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


in_metadata = {
    'name':            ('Name',              str),
    'grams_per_unit':  ('Grams per unit',    float),
    'fixed_portion_g': ('Fixed portion (g)', float),
}  # type: dict


class Ingredient:
    """\
    Food ingredient is an object that represents something
    drinks, servings, and mealpreps are cooked from.
    """

    def __init__(self,
                 name            : str,
                 nv_per_g        : NutritionalValues,
                 grams_per_unit  : float = 100.0,
                 fixed_portion_g : int   = 0,
                 ) -> None:
        """Create new Ingredient."""
        self.name            = name
        self.nv_per_g        = nv_per_g
        self.grams_per_unit  = grams_per_unit
        self.fixed_portion_g = fixed_portion_g

    def __eq__(self, other: Any) -> bool:
        """Return True if two Ingredients are equal."""
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name

    def __ne__(self, other: Any) -> bool:
        """Return True if two Ingredients are not equal."""
        return not self.__eq__(other)

    def __str__(self) -> str:
        """Identifying version of the Ingredient."""
        return f'{self.name}'

    def __repr__(self) -> str:
        """Format Ingredient attributes."""
        lines  = [f"<Ingredient-object {id(self)}>",
                  "General Info",
                  f"  Name: {self.name}",
                  'Nutrients: ']
        nv_lines = repr(self.nv_per_g).split('\n')
        string   = '\n'.join(lines)
        string  += '\n  '.join(nv_lines)

        return string

    @classmethod
    def from_dict(cls, purp_dictionary: dict) -> 'Ingredient':
        """Initialize Ingredient from dictionary."""
        if purp_dictionary['fixed_portion_g'] > 0.0:
            divider = purp_dictionary['fixed_portion_g']
        else:
            divider = purp_dictionary['grams_per_unit']

        parsed_nv = NutritionalValues()

        for key in parsed_nv.__dict__:
            if key not in purp_dictionary.keys():
                raise KeyError(f"Missing key '{key}'")
            setattr(parsed_nv, key, purp_dictionary[key])

        parsed_nv  = parsed_nv / divider
        ingredient = Ingredient(purp_dictionary['name'], parsed_nv)

        return ingredient

    def get_nv(self, for_grams: float) -> NutritionalValues:
        """Return the nutritional values of the ingredient for specified portion of grams."""
        return self.nv_per_g * for_grams
