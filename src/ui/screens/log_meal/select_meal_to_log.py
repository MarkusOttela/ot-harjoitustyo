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

from src.common.exceptions import AbortMenuOperation

from src.ui.gui_menu                  import GUIMenu
from src.ui.screens.log_meal.log_meal import log_meal
from src.ui.screens.show_message      import show_message
from src.ui.callback_classes          import Button

if typing.TYPE_CHECKING:
    from src.database.unencrypted_database import MealprepDatabase, IngredientDatabase, RecipeDatabase
    from src.entities.user import User
    from src.ui.gui        import GUI


def select_meal_to_log(gui           : 'GUI',
                       user          : 'User',
                       mealprep_db   : 'MealprepDatabase',
                       recipe_db     : 'RecipeDatabase',
                       ingredient_db : 'IngredientDatabase',

                       ) -> None:
    """Render the `Select Meal` menu."""
    title = 'Select Meal'
    while True:
        menu = GUIMenu(gui, title)

        list_of_mealpreps = mealprep_db.get_list_of_mealpreps()

        if not list_of_mealpreps:
            show_message(gui, title, 'No mealpreps yet in database.')
            return

        buttons       = {mealprep.recipe_name: Button(
            menu, closes_menu=True) for mealprep in list_of_mealpreps}
        cancel_button = Button(menu, closes_menu=True)

        for mealprep in list_of_mealpreps:
            menu.menu.add.button(f'{str(mealprep)}',
                                 action=buttons[mealprep.recipe_name].set_pressed)
        menu.menu.add.button('Cancel', action=cancel_button.set_pressed)

        menu.start()

        if cancel_button.pressed:
            return

        for mealprep_name, button in buttons.items():

            if button.pressed:
                mealprep = mealprep_db.get_mealprep(mealprep_name)
                log_meal(gui, user, mealprep, recipe_db, ingredient_db)

                raise AbortMenuOperation('Meal added')
