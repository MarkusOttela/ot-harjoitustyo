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

from src.common.validation import validate_params


ingredient_metadata = {

    # General information
    'name':         ('Name',   str),
    'manufacturer': ('Manuf.', str),

    # Macronutrients
    'kcal':          ('KCal',     float),
    'carbohydrates': ('Carbs',    float),
    'protein':       ('Protein',  float),
    'fat':           ('Fat',      float),
    'satisfied_fat': ('Sat. Fat', float),
    'fiber':         ('Fiber',    float),
    'salt':          ('Salt',     float),

    # Micronutrients

    # Omega-3 fatty acids
    'omega3_dha': ('Ω3 DHA', float),
    'omega3_epa': ('Ω3 EPA', float),

    # Fat soluble vitamins
    'vitamin_a': ('Vit. A', float),
    'vitamin_d': ('Vit. D', float),
    'vitamin_e': ('Vit. E', float),
    'vitamin_k': ('Vit. K', float),

    # Water soluble vitamins
    'vitamin_b1':  ('Vit. B1',  float),
    'vitamin_b2':  ('Vit. B2',  float),
    'vitamin_b3':  ('Vit. B3',  float),
    'vitamin_b5':  ('Vit. B5',  float),
    'vitamin_b6':  ('Vit. B6',  float),
    'vitamin_b7':  ('Vit. B7',  float),
    'vitamin_b9':  ('Vit. B9',  float),
    'vitamin_b12': ('Vit. B12', float),
    'vitamin_c':   ('Vit. C',   float),

    # Minerals etc.
    'calcium':   ('Calcium',   float),
    'chromium':  ('Chromium',  float),
    'iodine':    ('Iodine',    float),
    'potassium': ('Potassium', float),
    'iron':      ('Iron',      float),
    'magnesium': ('Magnesium', float),
    'zinc':      ('Zinc',      float),
    'caffeine':  ('Caffeine',  float),
    'creatine':  ('Creatine',  float),
}


class Ingredient:  # pylint: disable=too-many-instance-attributes
    """\
    Food ingredient is an object that represents something
    drinks, servings, and mealpreps are cooked from.

    Note: The pylint suppressions here are because Ingredient is more or less
          a data-class that holds all metadata for the specified ingredient.
    """

    def __init__(self,  # pylint: disable=too-many-arguments, too-many-locals, too-many-statements
                 name         : str,
                 manufacturer : str = '',

                 # Energy
                 kcal : float = 0.0,

                 # Macronutrients
                 carbohydrates : float = 0.0,
                 protein       : float = 0.0,
                 fat           : float = 0.0,
                 satisfied_fat : float = 0.0,
                 fiber         : float = 0.0,
                 salt          : float = 0.0,

                 # Micronutrients

                 # Omega-3 fatty acids
                 omega3_dha : float = 0.0,
                 omega3_epa : float = 0.0,

                 # Fat soluble vitamins
                 vitamin_a : float = 0.0,
                 vitamin_d : float = 0.0,
                 vitamin_e : float = 0.0,
                 vitamin_k : float = 0.0,

                 # Water soluble vitamins
                 vitamin_b1  : float = 0.0,
                 vitamin_b2  : float = 0.0,
                 vitamin_b3  : float = 0.0,
                 vitamin_b5  : float = 0.0,
                 vitamin_b6  : float = 0.0,
                 vitamin_b7  : float = 0.0,
                 vitamin_b9  : float = 0.0,
                 vitamin_b12 : float = 0.0,
                 vitamin_c   : float = 0.0,

                 # Minerals etc.
                 calcium   : float = 0.0,
                 chromium  : float = 0.0,
                 iodine    : float = 0.0,
                 potassium : float = 0.0,
                 iron      : float = 0.0,
                 magnesium : float = 0.0,
                 zinc      : float = 0.0,
                 caffeine  : float = 0.0,
                 creatine  : float = 0.0,

                 ) -> None:
        """Create new Ingredient.

        Macronutrients are given in grams / 100g.
        """
        validate_params(self.__init__, locals())  # type: ignore

        self.name         = name
        self.manufacturer = manufacturer

        # Energy
        self.kcal = kcal

        # Macronutrients
        self.carbohydrates = carbohydrates
        self.protein       = protein
        self.fat           = fat
        self.satisfied_fat = satisfied_fat
        self.fiber         = fiber
        self.salt          = salt

        # Micronutrients

        # Omega-3 fatty acids
        self.omega3_dha = omega3_dha
        self.omega3_epa = omega3_epa

        # Fat soluble vitamins
        self.vitamin_a = vitamin_a
        self.vitamin_d = vitamin_d
        self.vitamin_e = vitamin_e
        self.vitamin_k = vitamin_k

        # Water soluble vitamins
        self.vitamin_b1  = vitamin_b1
        self.vitamin_b2  = vitamin_b2
        self.vitamin_b3  = vitamin_b3
        self.vitamin_b5  = vitamin_b5
        self.vitamin_b6  = vitamin_b6
        self.vitamin_b7  = vitamin_b7
        self.vitamin_b9  = vitamin_b9
        self.vitamin_b12 = vitamin_b12
        self.vitamin_c   = vitamin_c

        # Minerals etc.
        self.calcium   = calcium
        self.chromium  = chromium
        self.iodine    = iodine
        self.potassium = potassium
        self.iron      = iron
        self.magnesium = magnesium
        self.zinc      = zinc
        self.caffeine  = caffeine
        self.creatine  = creatine

    def __eq__(self, other: Any) -> bool:
        """Return True if two Ingredients are equal."""
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.manufacturer == other.manufacturer

    def __neq__(self, other: Any) -> bool:
        """Return True if two Ingredients are not equal."""
        return not self.__eq__(other)

    def __str__(self) -> str:
        """Identifying version of the Ingredient"""
        return f'{self.name} ({self.manufacturer})'

    def __repr__(self) -> str:
        """Format Ingredient attributes."""
        lines  = [f"<Ingredient-object {id(self)}>"]
        indent = len(max(self.__dict__.keys(), key=len)) + 1
        lines.extend([f'    <{k:{indent}}: {v}>' for k, v in self.__dict__.items()])

        # Sub-headers for lines
        for index, txt in [( 1, 'General Info'),
                           ( 4, 'Energy'),
                           ( 6, 'Macronutrients'),
                           (13, 'Micronutrients')]:
            lines.insert(index, f'  {txt}')
        return '\n'.join(lines)

    @classmethod
    def from_dict(cls, purp_dictionary: dict) -> 'Ingredient':
        """Initialize Ingredient from dictionary."""
        ingredient = Ingredient(purp_dictionary['name'])

        for key in ingredient.__dict__:
            if key not in purp_dictionary.keys():
                raise KeyError(f"Missing key '{key}'")
            setattr(ingredient, key, purp_dictionary[key])

        return ingredient
