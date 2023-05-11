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
from src.common.statics    import Color

from src.diet.mealprep           import Mealprep
from src.diet.nutritional_values import NutritionalValues

from src.ui.gui_menu         import GUIMenu
from src.ui.callback_classes import Button, StringInput

from src.ui.screens.get_yes                       import get_yes
from src.ui.screens.mealprep_menu.create_mealprep import add_ingredient_gram_inputs
from src.ui.screens.show_message                  import show_message

if typing.TYPE_CHECKING:
    from src.database.unencrypted_database import MealprepDatabase, IngredientDatabase
    from src.ui.gui import GUI


def edit_mealprep(gui           : 'GUI',
                  mealprep_db   : 'MealprepDatabase',
                  ingredient_db : 'IngredientDatabase',
                  orig_mealprep : Mealprep,
                  ) -> None:
    """Render the `Edit Mealprep` menu."""
    title    = 'Edit Mealprep'
    keys     = list(orig_mealprep.ingredient_grams.keys()) + ['total_grams']
    metadata = {k: (k, float) for k in keys}

    metadata['total_grams'] = ('Total Weight', float)
    failed_conversions      = {}  # type: dict
    string_inputs           = {k: StringInput() for k in keys}

    # Prefill fields with previous data
    for k in orig_mealprep.ingredient_grams.keys():
        string_inputs[k].set_value(orig_mealprep.ingredient_grams[k])
    string_inputs['total_grams'].value = str(orig_mealprep.total_grams)

    while True:
        menu = GUIMenu(gui, title)

        return_button = Button(menu, closes_menu=True)
        done_button   = Button(menu, closes_menu=True)
        delete_button = Button(menu, closes_menu=True)

        add_ingredient_gram_inputs(menu, metadata, string_inputs, failed_conversions)

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
            success, weight_dict = convert_input_fields(string_inputs, metadata)
            total_grams          = weight_dict['total_grams']
            weight_dict.pop('total_grams')

            mealprep_nv = NutritionalValues()

            for ingredient_name in orig_mealprep.ingredient_grams.keys():
                ingredient   = ingredient_db.get_ingredient(ingredient_name)
                in_nv        = ingredient.get_nv(for_grams=weight_dict[ingredient_name])
                mealprep_nv += in_nv

            new_mealprep = Mealprep(orig_mealprep.recipe_name, total_grams,
                                    orig_mealprep.cook_date,   weight_dict, mealprep_nv)

            recipe_id_changed = new_mealprep != orig_mealprep

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
                mealprep_db.replace_mealprep(new_mealprep)
                show_message(gui, title, 'Mealprep has been replaced.')
                return
