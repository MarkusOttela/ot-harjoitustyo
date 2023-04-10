#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

"""
Calorienator - Diet tracker
Copyright (C) 2023 Markus Ottela

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
from src.common.statics    import Color

from src.diet.ingredient import ingredient_metadata, Ingredient

from src.gui.gui_menu                 import GUIMenu
from src.gui.screens.callback_classes import Button, StringInput
from src.gui.screens.get_yes          import get_yes
from src.gui.screens.show_message     import show_message

from src.gui.screens.ingredient_menu.add_ingredient import add_ingredient_attributes

if typing.TYPE_CHECKING:
    from src.gui.gui import GUI
    from src.database.ingredient_database import IngredientDatabase


def edit_ingredient(gui             : 'GUI',  # pylint: disable=too-many-locals
                    ingredient_db   : 'IngredientDatabase',
                    orig_ingredient : Ingredient,
                    ) -> None:
    """Render the `Edit Ingredient` menu."""
    title              = 'Edit Ingredient'
    failed_conversions = {}  # type: dict[str, None]

    while True:
        keys        = list(ingredient_metadata.keys())
        fields      = [ingredient_metadata[k][0] for k in keys]  # type: list[Any]
        field_types = [ingredient_metadata[k][1] for k in keys]  # type: list[Any]

        string_inputs = {k: StringInput() for k in keys}  # type: dict[str, StringInput]

        for k in string_inputs.keys():
            string_inputs[k].set_value(getattr(orig_ingredient, k))

        menu = GUIMenu(gui, title, columns=3, rows=18, column_max_width=532)

        add_ingredient_attributes(menu, keys, string_inputs, failed_conversions, fields)

        return_button = Button(menu, closes_menu=True)
        done_button   = Button(menu, closes_menu=True)
        delete_button = Button(menu, closes_menu=True)

        menu.menu.add.label('\n', font_size=5)
        menu.menu.add.button('Done',   action=done_button.set_pressed)
        menu.menu.add.button('Delete', action=delete_button.set_pressed, font_color=Color.RED.value)
        menu.menu.add.button('Return', action=return_button.set_pressed)
        menu.start()

        if return_button.pressed:
            return

        if delete_button.pressed:
            if get_yes(gui, title, f"Delete {str(orig_ingredient)}?", 'No'):
                ingredient_db.remove(orig_ingredient)
                show_message(gui, title, 'Ingredient has been removed.')
                return

        if done_button.pressed:
            success, value_dict   = convert_input_fields(string_inputs, keys, fields, field_types)
            new_ingredient        = Ingredient.from_dict(value_dict)
            ingredient_id_changed = new_ingredient != orig_ingredient

            if not success:
                failed_conversions = value_dict
                continue

            if not ingredient_id_changed:
                ingredient_db.replace(new_ingredient)
                show_message(gui, title, 'Ingredient has been updated.')
                return

            if not ingredient_db.has_ingredient(new_ingredient):
                ingredient_db.remove(orig_ingredient)
                ingredient_db.insert(new_ingredient)
                show_message(gui, title, 'Ingredient has been renamed and updated.')
                return

            if get_yes(gui, title,
                       f'Another ingredient {str(new_ingredient)} already exists. Overwrite(?)',
                       default_str='No'):
                ingredient_db.remove(orig_ingredient)
                ingredient_db.replace(new_ingredient)
                show_message(gui, title, 'Ingredient has been replaced.')
                return
