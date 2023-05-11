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

from src.common.conversion             import convert_input_fields
from src.common.statics                import Format
from src.database.unencrypted_database import IngredientDatabase, RecipeDatabase
from src.diet.meal                     import Meal
from src.diet.mealprep                 import Mealprep
from src.entities.user                 import User

from src.ui.gui_menu                              import GUIMenu
from src.ui.callback_classes                      import Button, StringInput
from src.ui.screens.mealprep_menu.create_mealprep import add_ingredient_gram_inputs
from src.ui.screens.show_message                  import show_message

if typing.TYPE_CHECKING:
    from src.ui.gui import GUI


def log_meal(gui           : 'GUI',
             user          : 'User',
             mealprep      : Mealprep,
             recipe_db     : 'RecipeDatabase',
             ingredient_db : IngredientDatabase
             ) -> None:
    """Render the `Log Meal` menu."""
    title  = 'Log Meal'
    recipe = recipe_db.get_recipe(mealprep.recipe_name)
    keys   = [mealprep.recipe_name] + recipe.accompaniment_names

    metadata           = {k: (k, float) for k in keys}
    failed_conversions = {}  # type: dict
    string_inputs      = {k: StringInput() for k in keys}

    for k in string_inputs.keys():
        string_inputs[k].set_value(k)

    while True:
        menu = GUIMenu(gui, title)

        return_button = Button(menu, closes_menu=True)
        done_button   = Button(menu, closes_menu=True)

        add_ingredient_gram_inputs(menu, metadata, string_inputs, failed_conversions)

        menu.menu.add.label('\n', font_size=5)
        menu.menu.add.button('Done',   action=done_button.set_pressed)
        menu.menu.add.button('Return', action=return_button.set_pressed)
        menu.start()

        if return_button.pressed:
            return

        if done_button.pressed:
            success, weight_dict = convert_input_fields(string_inputs, metadata)

            mp_grams = weight_dict[mealprep.recipe_name]
            meal_nv  = mealprep.get_nv(for_grams=mp_grams)

            for ac_name in recipe.accompaniment_names:
                ac_nv    = ingredient_db.get_ingredient(
                    ac_name).get_nv(for_grams=weight_dict[ac_name])
                meal_nv += ac_nv

            eat_tstamp = datetime.now().strftime(Format.DATETIME_TSTAMP.value)
            weight_dict.pop(mealprep.recipe_name)

            meal = Meal(recipe.name, eat_tstamp, mp_grams, weight_dict, meal_nv)

            user.add_meal(meal)

            show_message(gui, title, 'Meal has been successfully recorded.')
            return
