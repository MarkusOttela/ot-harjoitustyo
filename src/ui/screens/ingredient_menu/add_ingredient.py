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

import typing

from typing import Any

from src.common.conversion import convert_input_fields
from src.common.statics    import Color, ColorScheme
from src.common.validation import floats

from src.diet.ingredient import Ingredient, ingredient_metadata

from src.ui.gui_menu                 import GUIMenu
from src.ui.screens.callback_classes import Button, StringInput
from src.ui.screens.get_yes          import get_yes
from src.ui.screens.show_message     import show_message

if typing.TYPE_CHECKING:
    from src.ui.gui import GUI
    from src.database.ingredient_database import IngredientDatabase


def add_ingredient_menu(gui           : 'GUI',
                        ingredient_db : 'IngredientDatabase'
                        ) -> None:
    """Render the `Add Ingredient` menu."""
    title       = 'Add Ingredient'
    keys        = list(ingredient_metadata.keys())
    fields      = [ingredient_metadata[k][0] for k in keys]  # type: list[Any]
    field_types = [ingredient_metadata[k][1] for k in keys]  # type: list[Any]

    failed_conversions : dict[str, None] = {}

    string_inputs = {k: StringInput() for k in keys}

    # Testing code TODO: Remove
    debug = True
    if debug:
        string_inputs['name'].value = 'Mansikkahillo'
        string_inputs['manufacturer'].value = 'Atria'

        attr_list = ['kcal',
                     'carbohydrates', 'protein', 'fat', 'satisfied_fat',
                     'fiber', 'salt',
                     'omega3_dha', 'omega3_epa',
                     'vitamin_a', 'vitamin_d', 'vitamin_e', 'vitamin_k',
                     'vitamin_b1', 'vitamin_b2', 'vitamin_b3', 'vitamin_b5',
                     'vitamin_b6', 'vitamin_b7', 'vitamin_b9', 'vitamin_b12',
                     'vitamin_c',
                     'calcium', 'chromium', 'iodine', 'potassium', 'iron', 'magnesium', 'zinc',
                     'caffeine', 'creatine']

        for attr in attr_list:
            string_inputs[attr].value = '1.0'

    while True:
        menu = GUIMenu(gui, title, columns=3, rows=18, column_max_width=532)

        add_ingredient_attributes(menu, keys, string_inputs, failed_conversions, fields)

        return_button = Button(menu, closes_menu=True)
        done_button   = Button(menu, closes_menu=True)
        menu.menu.add.label('\n', font_size=5)
        menu.menu.add.button('Done',   action=done_button.set_pressed)
        menu.menu.add.button('Return', action=return_button.set_pressed)

        menu.start()

        if return_button.pressed:
            return

        if done_button.pressed:
            success, value_dict = convert_input_fields(string_inputs, keys, fields, field_types)
            new_ingredient      = Ingredient.from_dict(value_dict)

            if not success:
                failed_conversions = value_dict
                continue

            if not ingredient_db.has_ingredient(new_ingredient):
                ingredient_db.insert(new_ingredient)
                show_message(gui, title, 'Ingredient has been added.')
                return

            if get_yes(gui, title,
                       f'Ingredient {str(new_ingredient)} already exists. Overwrite(?)',
                       default_str='No'):
                ingredient_db.replace(new_ingredient)
                show_message(gui, title, 'Ingredient has been replaced.')
                return


def add_ingredient_attributes(menu:               GUIMenu,
                              keys:               list[Any],
                              string_inputs:      dict[str, StringInput],
                              failed_conversions: dict[str, None],
                              fields:             list[Any]) -> None:
    """Add the ingredient attributes."""
    for i, k in enumerate(keys):

        if i in [2, 3, 9, 11, 15, 23, 24]:
            menu.menu.add.label('\n', font_size=5)  # Spacing

        warning_color = Color.RED.value
        normal_color = ColorScheme.FONT_COLOR.value

        valid_chars = None if ingredient_metadata[k][1] == str else floats
        font_color = warning_color if k in failed_conversions else normal_color
        menu.menu.add.text_input(f'{fields[i]}: ',
                                 onchange=string_inputs[k].set_value,
                                 default=string_inputs[k].value,
                                 valid_chars=valid_chars,
                                 maxchar=19,
                                 font_color=font_color)
    failed_conversions.clear()
