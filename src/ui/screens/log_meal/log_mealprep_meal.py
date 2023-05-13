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
from src.common.enums      import Format
from src.common.exceptions import ReturnToMainMenu

from src.database.unencrypted_database import IngredientDatabase, RecipeDatabase

from src.entities.meal     import Meal
from src.entities.mealprep import Mealprep

from src.ui.callback_classes import Button, StringInput
from src.ui.gui_menu         import GUIMenu
from src.ui.shared           import add_ingredient_gram_inputs

from src.ui.screens.show_message import show_message

if typing.TYPE_CHECKING:
    from src.entities.user import User
    from src.ui.gui        import GUI


def log_mealprep_meal(gui           : 'GUI',
                      user          : 'User',
                      recipe_db     : 'RecipeDatabase',
                      ingredient_db : IngredientDatabase,
                      mealprep      : Mealprep
                      ) -> None:
    """Render the `Log Mealprep Meal` menu."""
    title         = 'Log Mealprep Meal'
    error_message = ''

    recipe = recipe_db.get_recipe(mealprep.recipe_name)
    keys   = [mealprep.recipe_name] + recipe.accompaniment_names

    failed_conversions = {}  # type: dict
    metadata           = {k: (k, float)    for k in keys}
    string_inputs      = {k: StringInput() for k in keys}

    for k in string_inputs.keys():
        string_inputs[k].set_value(k)

    while True:
        menu = GUIMenu(gui, title)

        done_bt   = Button(menu, closes_menu=True)
        return_bt = Button(menu, closes_menu=True)

        add_ingredient_gram_inputs(menu, metadata, string_inputs, failed_conversions)

        menu.menu.add.label('\n', font_size=5)
        menu.menu.add.button('Done',   action=done_bt.set_pressed)
        menu.menu.add.button('Return', action=return_bt.set_pressed)

        menu.show_error_message(error_message)
        menu.start()

        if return_bt.pressed:
            return

        if done_bt.pressed:
            success, weight_dict = convert_input_fields(string_inputs, metadata)

            if not success:
                failed_conversions = weight_dict
                continue

            main_grams = weight_dict[mealprep.recipe_name]
            meal_nv    = mealprep.get_nv(for_grams=main_grams)

            for ac_name in recipe.accompaniment_names:
                ingredient = ingredient_db.get_ingredient(ac_name)
                ac_nv      = ingredient.get_nv(for_grams=weight_dict[ac_name])
                meal_nv   += ac_nv

            eat_tstamp = datetime.now().strftime(Format.DATETIME_TSTAMP.value)
            weight_dict.pop(mealprep.recipe_name)

            meal = Meal(recipe.name, eat_tstamp, main_grams, meal_nv, weight_dict)

            user.add_meal(meal)

            show_message(gui, title, 'Meal has been successfully recorded.')
            raise ReturnToMainMenu('Meal successfully added')
