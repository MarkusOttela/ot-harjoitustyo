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

from src.common.types      import NonEmptyStr, NonNegativeFloat
from src.common.validation import validate_params


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
                 salt          : NonNegativeFloat = 0.0,

                 # Micronutrients

                 # Omega-3 fatty acids
                 omega3_dha: NonNegativeFloat = 0.0,
                 omega3_epa: NonNegativeFloat = 0.0,

                 # Fat soluble vitamins
                 vitamin_a : NonNegativeFloat = 0.0,
                 vitamin_d : NonNegativeFloat = 0.0,
                 vitamin_e : NonNegativeFloat = 0.0,
                 vitamin_k : NonNegativeFloat = 0.0,

                 # Water soluble vitamins
                 vitamin_b1   : NonNegativeFloat = 0.0,
                 vitamin_b2   : NonNegativeFloat = 0.0,
                 vitamin_b3   : NonNegativeFloat = 0.0,
                 vitamin_b5   : NonNegativeFloat = 0.0,
                 vitamin_b6   : NonNegativeFloat = 0.0,
                 vitamin_b7   : NonNegativeFloat = 0.0,
                 vitamin_b9   : NonNegativeFloat = 0.0,
                 vitamin_b12  : NonNegativeFloat = 0.0,
                 vitamin_c    : NonNegativeFloat = 0.0,

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
        """Create new Ingredient.

        Macronutrients are given in grams / 100g.
        """
        validate_params(self.__init__, locals())

        self.name          = name
        self.manufacturer  = manufacturer

        # Energy
        self.kcal          = kcal

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

    def __repr__(self) -> str:
        """Format Ingredient attributes."""
        return (f"<Ingredient-object {id(self)}>\n"
                f"  <{self.name          = }>\n"
                f"  <{self.manufacturer  = }>\n"
                f" Energy\n"
                f"  <{self.kcal          = }>\n"
                f" Macronutrients\n"
                f"  <{self.carbohydrates = }>\n"
                f"  <{self.protein       = }>\n"
                f"  <{self.fat           = }>\n"
                f"  <{self.satisfied_fat = }>\n"
                f"  <{self.fiber         = }>\n"
                f"  <{self.salt          = }>\n"
                f" Micronutrients\n"
                f"  <{self.omega3_dha    =}>\n"
                f"  <{self.omega3_epa    =}>\n"
                f"  <{self.vitamin_a     =}>\n"
                f"  <{self.vitamin_d     =}>\n"
                f"  <{self.vitamin_e     =}>\n"
                f"  <{self.vitamin_k     =}>\n"
                f"  <{self.vitamin_b1    =}>\n"
                f"  <{self.vitamin_b2    =}>\n"
                f"  <{self.vitamin_b3    =}>\n"
                f"  <{self.vitamin_b5    =}>\n"
                f"  <{self.vitamin_b6    =}>\n"
                f"  <{self.vitamin_b7    =}>\n"
                f"  <{self.vitamin_b9    =}>\n"
                f"  <{self.vitamin_b12   =}>\n"
                f"  <{self.vitamin_c     =}>\n"
                f"  <{self.calcium       =}>\n"
                f"  <{self.chromium      =}>\n"
                f"  <{self.iodine        =}>\n"
                f"  <{self.potassium     =}>\n"
                f"  <{self.iron          =}>\n"
                f"  <{self.magnesium     =}>\n"
                f"  <{self.zinc          =}>\n"
                f"  <{self.caffeine      =}>\n"
                f"  <{self.creatine      =}>\n")
