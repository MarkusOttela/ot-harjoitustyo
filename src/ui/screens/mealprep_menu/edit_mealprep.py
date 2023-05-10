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

from datetime import datetime

from src.common.conversion import convert_input_fields
from src.common.statics import Color

from src.diet.mealprep import Mealprep


from src.ui.gui_menu                              import GUIMenu
from src.ui.callback_classes                      import Button, StringInput
from src.ui.screens.get_yes                       import get_yes
from src.ui.screens.mealprep_menu.create_mealprep import add_ingredient_attributes
from src.ui.screens.show_message                  import show_message

if typing.TYPE_CHECKING:
    from src.ui.gui import GUI
    from src.database.unencrypted_database import MealprepDatabase


def edit_mealprep(gui           : 'GUI',
                  mealprep_db   : 'MealprepDatabase',
                  orig_mealprep : Mealprep,
                  ) -> None:
    """Render the `Edit Recipe` menu."""
    title = 'Edit Recipe'

    keys        = list(orig_mealprep.ingredient_grams.keys())
    fields      = list(orig_mealprep.ingredient_grams.keys())
    field_types = [float for _ in range(len(keys))]

    failed_conversions : dict = {}

    string_inputs = {k: StringInput() for k in keys}

    while True:
        menu = GUIMenu(gui, title)

        return_button = Button(menu, closes_menu=True)
        done_button   = Button(menu, closes_menu=True)
        delete_button = Button(menu, closes_menu=True)

        add_ingredient_attributes(menu, keys, string_inputs, failed_conversions, fields)

        menu.menu.add.label('\n', font_size=5)
        menu.menu.add.button('Done',   action=done_button.set_pressed)
        menu.menu.add.button('Delete', action=delete_button.set_pressed, font_color=Color.RED.value)
        menu.menu.add.button('Return', action=return_button.set_pressed)
        menu.start()

        if return_button.pressed:
            return

        if delete_button.pressed:
            if get_yes(gui, title, f"Delete {str(orig_mealprep)}?", 'No'):
                mealprep_db.remove_mealprep(orig_mealprep)
                show_message(gui, title, 'Mealprep has been removed.')
                return

        if done_button.pressed:
            success, value_dict = convert_input_fields(string_inputs, keys, fields, field_types)
            new_mealprep        = Mealprep(orig_mealprep.recipe_name, value_dict, datetime.now().date())
            recipe_id_changed   = new_mealprep != orig_mealprep

            if not recipe_id_changed:
                mealprep_db.replace_mealprep(new_mealprep)
                show_message(gui, title, 'Mealprep has been updated.')
                return

            if not mealprep_db.has_mealprep(new_mealprep):
                mealprep_db.remove_mealprep(orig_mealprep)
                mealprep_db.insert_mealprep(new_mealprep)
                show_message(gui, title, 'Mealprep has been renamed and updated.')
                return

            if get_yes(gui, title,
                       f'Another mealprep {str(new_mealprep)} already exists. Overwrite(?)',
                       default_str='No'):
                mealprep_db.remove_mealprep(orig_mealprep)
                mealprep_db.replace_mealprep(new_mealprep)
                show_message(gui, title, 'Mealprep has been replaced.')
                return
