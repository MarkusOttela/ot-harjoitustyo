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

from src.common.conversion import convert_input_fields
from src.common.statics    import Color, ColorScheme, FontSize
from src.common.validation import floats

from src.diet.ingredient         import Ingredient, in_metadata
from src.diet.nutritional_values import nv_metadata

from src.ui.gui_menu             import GUIMenu
from src.ui.callback_classes     import Button, StringInput
from src.ui.screens.get_yes      import get_yes
from src.ui.screens.show_message import show_message

if typing.TYPE_CHECKING:
    from src.database.unencrypted_database import IngredientDatabase
    from src.ui.gui import GUI


def add_ingredient_menu(gui           : 'GUI',
                        ingredient_db : 'IngredientDatabase'
                        ) -> None:
    """Render the `Add Ingredient` menu."""
    title              = 'Add Ingredient'

    joined_metadata = dict()
    joined_metadata.update(in_metadata)
    joined_metadata.update(nv_metadata)

    failed_conversions = {}  # type: dict
    keys               = list(in_metadata.keys()) + list(nv_metadata.keys())
    string_inputs      = {k: StringInput() for k in keys}

    # Prefill less commonly used fields with zeroes
    excluded = ['kcal', 'carbohydrates_g', 'protein_g', 'fat_g',
                'satisfied_fat_g', 'fiber_g', 'salt_g']
    for k in string_inputs.keys():
        if k in nv_metadata.keys() and k not in excluded:
            string_inputs[k].value = '0.0'
    string_inputs['grams_per_unit'].value  = '100.0'
    string_inputs['fixed_portion_g'].value = '0.0'

    while True:
        menu = GUIMenu(gui, title, columns=3, rows=18, column_max_width=532)

        add_ingredient_attributes(menu, joined_metadata, string_inputs, failed_conversions)

        return_button = Button(menu, closes_menu=True)
        done_button   = Button(menu, closes_menu=True)

        menu.menu.add.label('\n', font_size=5)
        menu.menu.add.button('Done',   action=done_button.set_pressed)
        menu.menu.add.button('Cancel', action=return_button.set_pressed)
        menu.start()

        if return_button.pressed:
            return

        if done_button.pressed:
            success, value_dict = convert_input_fields(string_inputs, joined_metadata)

            if not success:
                failed_conversions = value_dict
                continue

            new_ingredient = Ingredient.from_dict(value_dict)

            if not ingredient_db.has_ingredient(new_ingredient):
                ingredient_db.insert(new_ingredient)
                show_message(gui, title, 'Ingredient has been added.')
                return

            if get_yes(gui, title,
                       f'Ingredient {str(new_ingredient)} already exists. Overwrite(?)',
                       default_str='No'):
                ingredient_db.replace_ingredient(new_ingredient)
                show_message(gui, title, 'Ingredient has been replaced.')
                return


def add_ingredient_attributes(menu               : GUIMenu,
                              metadata           : dict,
                              string_inputs      : dict,
                              failed_conversions : dict,
                              ) -> None:
    """Add the ingredient attributes."""
    for i, k in enumerate(list(metadata.keys())):
        if i in [4, 11, 13, 17, 26]:
            menu.menu.add.label('\n', font_size=5)  # Spacing

        warning_color = Color.RED.value
        normal_color  = ColorScheme.FONT_COLOR.value

        valid_chars = None if metadata[k][1] == str else floats
        font_color  = warning_color if k in failed_conversions else normal_color
        units       = f' ({metadata[k][2]})' if len(metadata[k]) == 4 else ''
        menu.menu.add.text_input(f'{metadata[k][0]}{units}: ',
                                 onchange=string_inputs[k].set_value,
                                 default=string_inputs[k].value,
                                 valid_chars=valid_chars,
                                 maxchar=19,
                                 font_color=font_color,
                                 font_size=FontSize.FONT_SIZE_SMALL.value)
    failed_conversions.clear()
