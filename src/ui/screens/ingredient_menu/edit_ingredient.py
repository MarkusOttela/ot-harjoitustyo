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
from src.common.enums      import Color

from src.entities.ingredient         import in_metadata, Ingredient
from src.entities.nutritional_values import nv_metadata

from src.ui.callback_classes import Button, StringInput
from src.ui.gui_menu         import GUIMenu
from src.ui.shared           import add_ingredient_attributes

from src.ui.screens.get_yes      import get_yes
from src.ui.screens.show_message import show_message

if typing.TYPE_CHECKING:
    from src.database.unencrypted_database import IngredientDatabase
    from src.ui.gui import GUI


def edit_ingredient(gui             : 'GUI',
                    ingredient_db   : 'IngredientDatabase',
                    orig_ingredient : Ingredient,
                    ) -> None:
    """Render the `Edit Ingredient` menu."""
    title = 'Edit Ingredient'

    joined_metadata = dict()
    joined_metadata.update(in_metadata)
    joined_metadata.update(nv_metadata)

    failed_conversions = {}  # type: dict
    keys               = list(in_metadata.keys()) + list(nv_metadata.keys())
    string_inputs      = {k: StringInput() for k in keys}

    gram_multiplier = orig_ingredient.grams_per_unit
    if orig_ingredient.fixed_portion_g:
        gram_multiplier = orig_ingredient.fixed_portion_g

    # Prefill fields with earlier values
    for k in string_inputs.keys():
        if k in in_metadata.keys():
            string_inputs[k].value = getattr(orig_ingredient, k)
        else:
            string_inputs[k].value = getattr(orig_ingredient.nv_per_g, k) * gram_multiplier

        # Round displayed values to two decimals
        try:
            string_inputs[k].value = str(round(float(string_inputs[k].value), 2))
        except ValueError:
            pass

    while True:
        menu = GUIMenu(gui, title, columns=3, rows=18, column_max_width=532)

        add_ingredient_attributes(menu, joined_metadata, string_inputs, failed_conversions)

        done_bt   = Button(menu, closes_menu=True)
        delete_bt = Button(menu, closes_menu=True)
        return_bt = Button(menu, closes_menu=True)

        menu.menu.add.label('\n', font_size=5)
        menu.menu.add.button('Done',   action=done_bt.set_pressed)
        menu.menu.add.button('Delete', action=delete_bt.set_pressed, font_color=Color.RED.value)
        menu.menu.add.button('Return', action=return_bt.set_pressed)

        menu.start()

        if return_bt.pressed:
            return

        if delete_bt.pressed:
            if get_yes(gui, title, f"Delete {str(orig_ingredient)}?", 'No'):
                ingredient_db.remove_ingredient(orig_ingredient)
                show_message(gui, title, 'Ingredient has been removed.')
                return

        if done_bt.pressed:
            if not string_inputs['name'].value:
                failed_conversions['name'] = ''
                continue

            success, value_dict = convert_input_fields(string_inputs, joined_metadata)

            if not success:
                failed_conversions = value_dict
                continue

            new_ingredient        = Ingredient.from_dict(value_dict)
            ingredient_id_changed = new_ingredient != orig_ingredient

            orig_f_grams  = float(orig_ingredient.grams_per_unit)
            input_f_grams = float(string_inputs['grams_per_unit'].value)

            if orig_f_grams != input_f_grams:
                multiplier = orig_ingredient.grams_per_unit / value_dict['grams_per_unit']
                if multiplier > 1.0:
                    adjective = 'larger'
                else:
                    adjective  = 'smaller'
                    multiplier = 1 / multiplier

                if not get_yes(gui, 'Warning: Grams Per Unit has been changed.',
                               f'Change all values to {multiplier} times {adjective}?', 'No'):
                    continue

            if not ingredient_id_changed:
                ingredient_db.replace_ingredient(new_ingredient)
                show_message(gui, title, 'Ingredient has been updated.')
                return

            if not ingredient_db.has_ingredient(new_ingredient):
                ingredient_db.insert(new_ingredient)
                show_message(gui, title, 'New ingredient has been added.')
                return

            if get_yes(gui, title,
                       f'Another ingredient {str(new_ingredient)} already exists. Overwrite(?)',
                       default_str='No'):
                ingredient_db.remove_ingredient(orig_ingredient)
                ingredient_db.replace_ingredient(new_ingredient)
                show_message(gui, title, 'Ingredient has been replaced.')
                return
