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

import datetime
import typing

from src.common.conversion import convert_input_fields
from src.common.enums      import Format

from src.database.unencrypted_database import IngredientDatabase, MealprepDatabase

from src.entities.mealprep           import Mealprep
from src.entities.nutritional_values import NutritionalValues
from src.entities.recipe             import Recipe

from src.ui.gui_menu         import GUIMenu
from src.ui.callback_classes import Button, StringInput
from src.ui.shared           import add_ingredient_gram_inputs

from src.ui.screens.get_yes      import get_yes
from src.ui.screens.show_message import show_message

if typing.TYPE_CHECKING:
    from src.ui.gui import GUI


def create_mealprep(gui           : 'GUI',
                    ingredient_db : IngredientDatabase,
                    mealprep_db   : MealprepDatabase,
                    recipe        : Recipe
                    ) -> None:
    """Render the `Create New Mealprep` menu."""
    title    = 'Create New Mealprep'
    keys     = list(recipe.ingredient_names) + ['Total Weight']
    metadata = {k: (k, float) for k in keys}

    failed_conversions = {}  # type: dict

    string_inputs = {k: StringInput() for k in keys}

    while True:
        menu = GUIMenu(gui, title)

        menu.menu.add.label('Please specify grams for each mealprep ingredient\n')
        add_ingredient_gram_inputs(menu, metadata, string_inputs, failed_conversions)

        menu.menu.add.label('\n', font_size=5)

        return_bt = Button(menu, closes_menu=True)
        done_bt   = Button(menu, closes_menu=True)

        menu.menu.add.button('Done',   action=done_bt.set_pressed)
        menu.menu.add.button('Cancel', action=return_bt.set_pressed)

        menu.start()

        if return_bt.pressed:
            return

        if done_bt.pressed:
            success, weight_dict = convert_input_fields(string_inputs, metadata)

            if not success:
                failed_conversions = weight_dict
                continue

            total_grams = weight_dict['Total Weight']
            weight_dict.pop('Total Weight')

            mealprep_nv = NutritionalValues()

            for ingredient_name in recipe.ingredient_names:
                ingredient   = ingredient_db.get_ingredient(ingredient_name)
                in_nv        = ingredient.get_nv(for_grams=weight_dict[ingredient_name])
                mealprep_nv += in_nv

            cook_date    = datetime.datetime.now().date().strftime(Format.DATETIME_DATE.value)
            new_mealprep = Mealprep(recipe.name, total_grams, cook_date, weight_dict, mealprep_nv)

            if not success:
                failed_conversions = weight_dict
                continue

            if not mealprep_db.has_mealprep(new_mealprep):
                mealprep_db.insert_mealprep(new_mealprep)
                show_message(gui, title, 'Mealprep has been added.')
                return

            if get_yes(gui, title,
                       f'Mealprep {new_mealprep.recipe_name} already exists. Overwrite(?)',
                       default_str='No'):
                mealprep_db.replace_mealprep(new_mealprep)
                show_message(gui, title, 'Mealprep has been replaced.')
                return
