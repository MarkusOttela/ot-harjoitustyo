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

import typing

from typing import Any

from src.common.conversion import str_to_float
from src.common.exceptions import ConversionError, ValidationError
from src.common.statics    import Color, ColorScheme
from src.common.types      import NonNegativeFloat, NonEmptyStr, NonNegativeInt
from src.common.validation import validate_str

from src.diet.ingredient import IngredientMetadata, Ingredient

from src.gui.gui_menu                 import GUIMenu
from src.gui.screens.callback_classes import Button, StringInput

if typing.TYPE_CHECKING:
    from src.gui.gui import GUI
    from src.database.ingredient_database import IngredientDatabase


def add_ingredient_menu(gui: 'GUI', ingredient_db: 'IngredientDatabase') -> None:
    """Render the `add ingredient` menu."""
    keys        = [enum.value[0] for enum in IngredientMetadata]
    fields      = [enum.value[1] for enum in IngredientMetadata]
    field_types = [enum.value[2] for enum in IngredientMetadata]

    failed_conversions : dict[str, None] = {}

    string_inputs = {k: StringInput() for k in keys}

    # Testing code TODO: Remove
    debug = False
    if debug:
        string_inputs['name'].value = 'Mansikkahillo'
        string_inputs['manufacturer'].value = 'Atria'
        attr_list = ['kcal', 'carbohydrates', 'protein', 'fat', 'satisfied_fat', 'fiber', 'salt', 'omega3_dha',
                     'omega3_epa', 'vitamin_a', 'vitamin_d', 'vitamin_e', 'vitamin_k', 'vitamin_b1', 'vitamin_b2',
                     'vitamin_b3', 'vitamin_b5', 'vitamin_b6', 'vitamin_b7', 'vitamin_b9', 'vitamin_b12', 'vitamin_c',
                     'calcium', 'chromium', 'iodine', 'potassium', 'iron', 'magnesium', 'zinc', 'caffeine', 'creatine']
        for attr in attr_list:
            string_inputs[attr].value = 1.0

    while True:
        menu = GUIMenu(gui, 'Add ingredient', columns=3, rows=18)

        for i, k in enumerate(keys):

            if i in [2, 3, 9, 11, 15, 23, 24]:
                menu.menu.add.label('\n', font_size=5)  # Spacing

            font_color = Color.RED.value if k in failed_conversions else ColorScheme.FONT_COLOR.value
            menu.menu.add.text_input(f'{fields[i]}: ',
                                     onchange=string_inputs[k].set_value,
                                     default=string_inputs[k].value,
                                     font_color=font_color)

        failed_conversions.clear()

        return_button = Button(menu, closes_menu=True)
        done_button   = Button(menu, closes_menu=True)
        menu.menu.add.label('\n', font_size=5)
        menu.menu.add.button('Done',   action=done_button.set_pressed)
        menu.menu.add.button('Return', action=return_button.set_pressed)

        menu.start()

        if done_button.pressed:
            success, value_dict = convert_input_fields(string_inputs, keys, fields, field_types)

            if success:
                ingredient_db.insert(Ingredient.from_dict(value_dict))
                return
            else:
                failed_conversions = value_dict
                continue

        if return_button.pressed:
            return


def convert_input_fields(string_inputs : dict[str, StringInput],
                         keys          : list[str],
                         fields        : list[str],
                         field_types   : list[type]
                         ) -> tuple[bool, dict[str, Any]]:
    """Convert input fields of `Add Ingredient` menu to correct data types."""
    converted_values   : dict[str, Any ] = {}
    failed_conversions : dict[str, None] = {}

    for key, name, field_type in zip(keys, fields, field_types):
        try:
            string_value = string_inputs[key].value

            if field_type in [int, NonNegativeInt]:
                converted_value = str_to_float(name, string_value)

            elif field_type in [float, NonNegativeFloat]:
                converted_value = str_to_float(name, string_value)

            elif field_type == NonEmptyStr:
                validate_str(key, string_value, empty_allowed=False)
                converted_value = string_value

            elif field_type == str:
                converted_value = string_value

            else:
                raise ValueError(f"Unknown field type {field_type}.")

            converted_values[key] = converted_value

        except (ConversionError, ValidationError):
            failed_conversions[key] = None

    if failed_conversions:
        return False, failed_conversions
    else:
        return True, converted_values
