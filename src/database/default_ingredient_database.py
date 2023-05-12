#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

"""
Calorinator - Diet tracker
Copyright (C) 2023 Markus Ottela

This fiber_gle is part of Calorinator.
Calorinator is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. Calorinator is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License
along with Calorinator. If not, see <https://www.gnu.org/licenses/>.
"""

from src.diet.ingredient         import Ingredient
from src.diet.nutritional_values import NutritionalValues

# pylint: skip-file
# Lines are left long to improve readability

default_ingredients = [
    Ingredient('Blueberry',              NutritionalValues(kcal=64.7,  carbohydrates_g=10.2, sugar_g=8.4,  protein_g=0.8, fat_g=1.1, fiber_g=3.3,           salt_g=0.0 ),              manufacturer=''),
    Ingredient('Margarin',               NutritionalValues(kcal=515.0, carbohydrates_g=0.3,  sugar_g=0.3,  protein_g=0.2, fat_g=57.0, satisfied_fat_g=19.0, salt_g=0.98),              manufacturer='Arla-Ingman'),
    Ingredient('Rye Oatmeal',            NutritionalValues(kcal=369.0, carbohydrates_g=65.2, sugar_g=1.1,  protein_g=8.9, fat_g=1.6, satisfied_fat_g=0.2,  fiber_g=14.0, salt_g=0.01), manufacturer='Raisio'),
    Ingredient('Water',                  NutritionalValues()),
    Ingredient('Salt',                   NutritionalValues(kcal=400.0, carbohydrates_g=97.0, sugar_g=0.0,  protein_g=0.0,  fat_g=0.0,  satisfied_fat_g=0.0,  fiber_g=0.0, salt_g=100.0,
                                                           iodine_ug=2.5),                                                                                                              manufacturer='Jozo'),
    Ingredient('Fat-free Milk',          NutritionalValues(kcal=33.8,  carbohydrates_g=4.9,  sugar_g=4.9,  protein_g=3.1,  fat_g=0.1,  satisfied_fat_g=0.1,  fiber_g=0.0, salt_g=0.01,
                                                           vitamin_b2_mg=0.2, vitamin_b12_ug=0.4, vitamin_d_ug=1.0, calcium_mg=120.0),                                                  manufacturer='Arla-Ingman', ),
    Ingredient('Butter',                 NutritionalValues(kcal=720.0, carbohydrates_g=1.0,  sugar_g=1.0,  protein_g=1.0,  fat_g=80.0, satisfied_fat_g=54.0, fiber_g=0.0, salt_g=1.5),  manufacturer='Arla-Ingman'),
    Ingredient('Cellery',                NutritionalValues(kcal=12.7,  carbohydrates_g=1.1,  sugar_g=1.1,  protein_g=1.1,  fat_g=0.2,  satisfied_fat_g=0.1,  fiber_g=1.0, salt_g=0.3),  manufacturer=''),
    Ingredient('Carrot',                 NutritionalValues(kcal=32.7,  carbohydrates_g=5.6,  sugar_g=5.4,  protein_g=0.6,  fat_g=0.2,  satisfied_fat_g=0.0,  fiber_g=2.6, salt_g=0.1),  manufacturer=''),
    Ingredient('Yellow onion',           NutritionalValues(kcal=29.4,  carbohydrates_g=4.8,  sugar_g=4.8,  protein_g=1.3,  fat_g=0.1,  satisfied_fat_g=0.0,  fiber_g=1.7, salt_g=0.0),  manufacturer=''),
    Ingredient('Minced pork/cow (23%)',  NutritionalValues(kcal=275.0, carbohydrates_g=0.0,  sugar_g=0.0,  protein_g=17.0, fat_g=23.0, satisfied_fat_g=11.0, fiber_g=0.0, salt_g=0.15), manufacturer='Kotimaista'),
    Ingredient('Bacon',                  NutritionalValues(kcal=317.0, carbohydrates_g=0.0,  sugar_g=0.0,  protein_g=14.0, fat_g=29.0, satisfied_fat_g=11.0, fiber_g=0.0, salt_g=2.2),  manufacturer='Dulano'),
    Ingredient('Tomato pyre' ,           NutritionalValues(kcal=145.0, carbohydrates_g=25.8, sugar_g=17.0, protein_g=5.9,  fat_g=0.7,  satisfied_fat_g=0.0,  fiber_g=0.0, salt_g=1.0),  manufacturer='Freshona'),
    Ingredient('Parmesan',               NutritionalValues(kcal=402.0, carbohydrates_g=0.0,  sugar_g=0.0,  protein_g=32.0, fat_g=30.0, satisfied_fat_g=20.0, fiber_g=0.0, salt_g=1.6),  manufacturer='Lovilio'),
    Ingredient('Pasta (full-grain)',     NutritionalValues(kcal=348.0, carbohydrates_g=65.8, sugar_g=2.8,  protein_g=14.0, fat_g=1.9,  satisfied_fat_g=0.4,  fiber_g=6.2, salt_g=0.01), manufacturer='Rummo'),
]
