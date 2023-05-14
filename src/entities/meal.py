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

import ast

from typing import Any

from src.entities.nutritional_values import NutritionalValues


class Meal:
    """Meal is an instance of a (mealprep) recipe.

    Meal contains the ingredients and grams that were eaten the day.
    """

    def __init__(self,
                 name                : str,
                 eat_tstamp          : str,
                 main_grams          : float,
                 meal_nv             : NutritionalValues,
                 accompaniment_grams : dict
                 ) -> None:
        """Create new Meal object."""
        self.name                = name
        self.eat_tstamp          = eat_tstamp
        self.main_grams          = main_grams
        self.meal_nv             = meal_nv
        self.accompaniment_grams = accompaniment_grams

    def __repr__(self) -> str:
        """Format Meal attributes."""
        lines = [f"<Meal-object {id(self)}>",
                 '  General Information:',
                 f'    Name         : {self.name}',
                 f'    Meal tstamp  : {self.eat_tstamp}',
                 f'    Total weight : {self.total_weight:.1f}g',
                 f'    Energy       : {self.meal_nv.kcal:.1f}kcal',
                 '  Accompaniments:']
        for ac_name, ac_grams in self.accompaniment_grams.items():
            lines.append(f'    {ac_name}: {ac_grams}g')

        return '\n'.join(lines)

    def __eq__(self, other: Any) -> bool:
        """Return True if two Meal objects are the same."""
        if not isinstance(other, Meal):
            return False
        return self.name == other.name and self.eat_tstamp == other.eat_tstamp

    def __ne__(self, other) -> bool:
        """Return True if two Meal objects are not the same."""
        return not self.__eq__(other)

    @property
    def eat_date(self) -> str:
        """Return the date when the meal was eaten."""
        return self.eat_tstamp.split('-')[0]

    @property
    def eat_time(self) -> str:
        """Return the time of day when the meal was eaten."""
        return self.eat_tstamp.split('-')[1]

    @property
    def total_weight(self) -> float:
        """Returns the total weight of the meal (main recipe plus accompaniments)."""
        total_weight = self.main_grams
        if self.accompaniment_grams:
            total_weight += sum(self.accompaniment_grams.values())
        return total_weight

    def serialize(self) -> str:
        """Return the serialized version of the object."""
        return str({'name':                self.name,
                    'eat_tstamp':          self.eat_tstamp,
                    'main_grams':          self.main_grams,
                    'accompaniment_grams': str(self.accompaniment_grams),
                    'meal_nv':             self.meal_nv.serialize()
                    })

    @classmethod
    def from_serialized_string(cls, serialized_string: str) -> 'Meal':
        """Instantiate the object from a serialized string."""
        ast_dict = ast.literal_eval(serialized_string)

        return Meal(name=ast_dict['name'],
                    eat_tstamp=ast_dict['eat_tstamp'],
                    main_grams=ast_dict['main_grams'],
                    accompaniment_grams=ast.literal_eval(ast_dict['accompaniment_grams']),
                    meal_nv=NutritionalValues.from_serialized(ast_dict['meal_nv']))
