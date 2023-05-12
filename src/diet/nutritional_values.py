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
import sys

from typing import Union

from src.diet.enums import CalContent, TefMultipliers


nv_metadata = {

    # Macronutrients
    # key             GUI name    db format  unit    multiplier_to_grams
    'kcal':            ('KCal',     float,     'g',    1),
    'carbohydrates_g': ('Carbs',    float,     'g',    1),
    'sugar_g':         ('Sugar',    float,     'g',    1),
    'protein_g':       ('Protein',  float,     'g',    1),
    'fat_g':           ('Fat',      float,     'g',    1),
    'satisfied_fat_g': ('Sat. Fat', float,     'g',    1),
    'fiber_g':         ('Fiber',    float,     'g',    1),
    'salt_g':          ('Salt',     float,     'g',    1),

    # Micronutrients

    # Omega-3 fatty acids
    'omega3_dha_mg': ('Ω3 DHA',      float,     'mg',   1_000),
    'omega3_epa_mg': ('Ω3 EPA',      float,     'mg',   1_000),

    # Fat soluble vitamins
    'vitamin_a_ug': ('Vit. A',       float,     'ug',   1_000_000),
    'vitamin_d_ug': ('Vit. D',       float,     'ug',   1_000_000),
    'vitamin_e_mg': ('Vit. E',       float,     'mg',   1_000),
    'vitamin_k_ug': ('Vit. K',       float,     'ug',   1_000_000),

    # Water soluble vitamins
    'vitamin_b1_mg':  ('Vit. B1',    float,     'mg',   1_000),
    'vitamin_b2_mg':  ('Vit. B2',    float,     'mg',   1_000),
    'vitamin_b3_mg':  ('Vit. B3',    float,     'mg',   1_000),
    'vitamin_b5_mg':  ('Vit. B5',    float,     'mg',   1_000),
    'vitamin_b6_mg':  ('Vit. B6',    float,     'mg',   1_000),
    'vitamin_b7_ug':  ('Vit. B7',    float,     'ug',   1_000_000),
    'vitamin_b9_ug':  ('Vit. B9',    float,     'ug',   1_000_000),
    'vitamin_b12_ug': ('Vit. B12',   float,     'ug',   1_000_000),

    'vitamin_c_mg':   ('Vit. C',     float,     'mg',   1_000),

    # Minerals etc.
    'calcium_mg':   ('Calcium',      float,     'mg',   1_000),
    'chromium_ug':  ('Chromium',     float,     'ug',   1_000_000),
    'iodine_ug':    ('Iodine',       float,     'ug',   1_000_000),
    'potassium_mg': ('Potassium',    float,     'mg',   1_000),
    'iron_mg':      ('Iron',         float,     'mg',   1_000),
    'magnesium_mg': ('Magnesium',    float,     'mg',   1_000),
    'zinc_mg':      ('Zinc',         float,     'mg',   1_000),
    'caffeine_mg':  ('Caffeine',     float,     'mg',   1_000),
    'creatine_g':   ('Creatine',     float,     'g',    1),
}


class NutritionalValues:  # pylint: disable=too-many-instance-attributes
    """\
    NutritionalValues is a data-class that contains the nutritional values of an object such as
        * An ingredient
        * A fixed item such as a supplement pill
        * A Mealprep constructed from ingredients
        * A Serving taken from a MealPrep
        * Total daily consumption
        * Daily consumption goals

    Note: The `pylint: disable=` suppressions here are because NutritionalValues is more
          or less a data-class that holds all nutritional metadata for the specified ingredient.
    """

    def __init__(self,  # pylint: disable=too-many-arguments, too-many-locals, too-many-statements
                 # Energy
                 kcal : float = 0.0,

                 # Macronutrients
                 carbohydrates_g : float = 0.0,
                 sugar_g         : float = 0.0,
                 protein_g       : float = 0.0,
                 fat_g           : float = 0.0,
                 satisfied_fat_g : float = 0.0,
                 fiber_g         : float = 0.0,
                 salt_g          : float = 0.0,

                 # Micronutrients

                 # Omega-3 fatty acids
                 omega3_dha_mg : float = 0.0,
                 omega3_epa_mg : float = 0.0,

                 # Fat soluble vitamins
                 vitamin_a_ug : float = 0.0,
                 vitamin_d_ug : float = 0.0,
                 vitamin_e_mg : float = 0.0,
                 vitamin_k_ug : float = 0.0,

                 # Water soluble vitamins
                 vitamin_b1_mg  : float = 0.0,
                 vitamin_b2_mg  : float = 0.0,
                 vitamin_b3_mg  : float = 0.0,
                 vitamin_b5_mg  : float = 0.0,
                 vitamin_b6_mg  : float = 0.0,
                 vitamin_b7_ug  : float = 0.0,
                 vitamin_b9_ug  : float = 0.0,
                 vitamin_b12_ug : float = 0.0,
                 vitamin_c_mg   : float = 0.0,

                 # Minerals etc.
                 calcium_mg   : float = 0.0,
                 chromium_ug  : float = 0.0,
                 iodine_ug    : float = 0.0,
                 potassium_mg : float = 0.0,
                 iron_mg      : float = 0.0,
                 magnesium_mg : float = 0.0,
                 zinc_mg      : float = 0.0,
                 caffeine_mg  : float = 0.0,
                 creatine_g   : float = 0.0,
                 ) -> None:
        """Create new NutritionalValues object."""

        # Energy
        self.kcal = kcal

        # Macronutrients
        self.carbohydrates_g = carbohydrates_g
        self.sugar_g         = sugar_g
        self.protein_g       = protein_g
        self.fat_g           = fat_g
        self.satisfied_fat_g = satisfied_fat_g
        self.fiber_g         = fiber_g
        self.salt_g          = salt_g

        # Micronutrients

        # Omega-3 fatty acids
        self.omega3_dha_mg = omega3_dha_mg
        self.omega3_epa_mg = omega3_epa_mg

        # Fat soluble vitamins
        self.vitamin_a_ug = vitamin_a_ug
        self.vitamin_d_ug = vitamin_d_ug
        self.vitamin_e_mg = vitamin_e_mg
        self.vitamin_k_ug = vitamin_k_ug

        # Water soluble vitamins
        self.vitamin_b1_mg  = vitamin_b1_mg
        self.vitamin_b2_mg  = vitamin_b2_mg
        self.vitamin_b3_mg  = vitamin_b3_mg
        self.vitamin_b5_mg  = vitamin_b5_mg
        self.vitamin_b6_mg  = vitamin_b6_mg
        self.vitamin_b7_ug  = vitamin_b7_ug
        self.vitamin_b9_ug  = vitamin_b9_ug
        self.vitamin_b12_ug = vitamin_b12_ug
        self.vitamin_c_mg   = vitamin_c_mg

        # Minerals etc.
        self.calcium_mg   = calcium_mg
        self.chromium_ug  = chromium_ug
        self.iodine_ug    = iodine_ug
        self.potassium_mg = potassium_mg
        self.iron_mg      = iron_mg
        self.magnesium_mg = magnesium_mg
        self.zinc_mg      = zinc_mg
        self.caffeine_mg  = caffeine_mg
        self.creatine_g   = creatine_g

    def __repr__(self) -> str:
        """Format NutritionalValues attributes."""
        lines  = [f"<NutritionalValues-object {id(self)}>"]
        indent = len(max(self.__dict__.keys(), key=len)) + 1
        lines.extend([f'    {k:{indent}}: {v}' for k, v in self.__dict__.items()])

        # Sub-headers for lines
        for index, txt in [( 1, 'Energy (per 1 g of ingredient)'),
                           ( 3, 'Macronutrients (per 1g of ingredient)'),
                           (10, 'Micronutrients (per 1g of ingredient)')]:
            lines.insert(index, f'  {txt}')
        return '\n'.join(lines)

    def __add__(self, other: 'NutritionalValues') -> 'NutritionalValues':
        """Add two NutritionalValues objects together."""
        new = NutritionalValues()
        for key, value in self.__dict__.items():
            new.__dict__[key] = value + other.__dict__[key]
        return new

    def __sub__(self, other: 'NutritionalValues') -> 'NutritionalValues':
        """Subtract one NutritionalValues object from another."""
        new = NutritionalValues()
        for key, value in self.__dict__.items():
            new.__dict__[key] = value - other.__dict__[key]
        return new

    def __mul__(self, multiplier: Union[int, float]) -> 'NutritionalValues':
        """Multiply NutritionalValues object with an integer/float."""
        if not isinstance(multiplier, (int, float)):
            raise ValueError("NutritionalValues object can only be multiplied with a number.")

        new = NutritionalValues()
        for key, value in self.__dict__.items():
            new.__dict__[key] = value * multiplier
        return new

    def __truediv__(self, divider: Union[int, float, 'NutritionalValues']) -> 'NutritionalValues':
        """Divide NutritionalValues object with another NV or an integer/float.

        Note: If the divider is another NutritionalValues object, the values
              in the resulting object will be ratios, not actual grams/kCals.
              Dividing with another NV object should only be used when e.g.
              determining what percentage of daily nutritional goals have been met.
        """
        if not isinstance(divider, (int, float, NutritionalValues)):
            raise ValueError("NutritionalValues object can only be divided with "
                             "a number or another NutritionalValues object.")

        new = NutritionalValues()

        if isinstance(divider, (float, int)):
            for key, value in self.__dict__.items():
                new.__dict__[key] = value / divider

        elif isinstance(divider, NutritionalValues):
            for key, value in self.__dict__.items():
                new.__dict__[key] = value / getattr(divider, key)

        return new

    def apply_tef_multipliers(self):
        """\
        Apply TEF[1] multipliers to the nutritional values
        to calculate actually usable energy in the food.

        [1] https://en.wikipedia.org/wiki/Specific_dynamic_action

        This function should only be called when observing the nutritional
        values usable by the user, e.g., when observing the daily calorie
        balance.
        """
        carbs_kcal = (self.carbohydrates_g
                      * CalContent.KCAL_PER_GRAM_CARB.value
                      * TefMultipliers.TEF_CARB_EFFICIENCY.value)

        protein_kcal = (self.protein_g
                        * CalContent.KCAL_PER_GRAM_PROTEIN.value
                        * TefMultipliers.TEF_PROTEIN_EFFICIENCY.value)

        fat_kcal = (self.fat_g
                    * CalContent.KCAL_PER_GRAM_FAT.value
                    * TefMultipliers.TEF_FAT_EFFICIENCY.value)

        self.kcal = carbs_kcal + protein_kcal + fat_kcal

    def serialize(self) -> str:
        """Return the object has a string."""
        return str(self.__dict__)

    @classmethod
    def from_serialized(cls, serialized_string: str) -> 'NutritionalValues':
        """Instantiate the object from a serialized string."""
        new_nv = NutritionalValues()
        dict_  = ast.literal_eval(serialized_string)
        for key, value, in dict_.items():
            setattr(new_nv, key, value)
        return new_nv
