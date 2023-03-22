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

from src.common.conversion import convert_input_fields
from src.common.statics    import Color, ColorScheme
from src.common.types      import NonEmptyStr
from src.common.validation import floats

from src.diet.ingredient import ingredient_metadata, Ingredient

from src.gui.gui_menu                 import GUIMenu
from src.gui.screens.callback_classes import Button, StringInput
from src.gui.screens.show_message     import show_message

if typing.TYPE_CHECKING:
    from src.gui.gui import GUI
    from src.database.ingredient_database import IngredientDatabase


def edit_ingredient(gui           : 'GUI',
                    ingredient_db : 'IngredientDatabase',
                    ingredient    : Ingredient,
                    ) -> None:
    """Render the `Edit Ingredient` menu."""
    title       = 'Edit Ingredient'
    keys        = list(ingredient_metadata.keys())
    fields      = [ingredient_metadata[k][0] for k in keys]  # type: list[Any]
    field_types = [ingredient_metadata[k][1] for k in keys]  # type: list[Any]

    failed_conversions : dict[str, None] = {}

    string_inputs = {k: StringInput() for k in keys}  # type: dict[str, StringInput]

    for k, v in string_inputs.items():
        string_inputs[k].set_value(getattr(ingredient, k))

    while True:
        menu = GUIMenu(gui, title, columns=3, rows=18, column_max_width=532)

        for i, k in enumerate(keys):

            if i in [2, 3, 9, 11, 15, 23, 24]:
                menu.menu.add.label('\n', font_size=5)  # Spacing

            valid_chars = None if ingredient_metadata[k][1] in [str, NonEmptyStr] else floats
            font_color  = Color.RED.value if k in failed_conversions else ColorScheme.FONT_COLOR.value
            menu.menu.add.text_input(f'{fields[i]}: ',
                                     onchange=string_inputs[k].set_value,
                                     default=string_inputs[k].value,
                                     valid_chars=valid_chars,
                                     maxchar=19,
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
                new_ingredient = Ingredient.from_dict(value_dict)
                ingredient_db.replace_ingredient(ingredient, new_ingredient)
                show_message(gui, title, 'Ingredient has been updated.')
                return
            else:
                failed_conversions = value_dict
                continue

        if return_button.pressed:
            return
