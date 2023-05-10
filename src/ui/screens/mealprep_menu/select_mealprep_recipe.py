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

from src.ui.gui_menu                              import GUIMenu
from src.ui.screens.mealprep_menu.create_mealprep import create_mealprep
from src.ui.screens.show_message                  import show_message
from src.ui.screens.callback_classes              import Button

from src.ui.screens.recipe_menu.edit_recipe import edit_recipe

if typing.TYPE_CHECKING:
    from src.database.unencrypted_database import IngredientDatabase, MealprepDatabase, RecipeDatabase
    from src.ui.gui import GUI


def select_mealprep_recipe(gui           : 'GUI',
                           ingredient_db : 'IngredientDatabase',
                           recipe_db     : 'RecipeDatabase',
                           mealprep_db   : 'MealprepDatabase',
                            ) -> None:
    """Render the `Select Mealprep Recipe` menu."""
    title = 'Select Mealprep Recipe'
    while True:
        menu = GUIMenu(gui, title)

        list_of_recipes = recipe_db.get_list_of_recipes()

        if not list_of_recipes:
            show_message(gui, title, 'No recipes yet in database.')
            return

        buttons       = {recipe.name: Button(menu, closes_menu=True) for recipe in list_of_recipes}
        cancel_button = Button(menu, closes_menu=True)

        for recipe in list_of_recipes:
            menu.menu.add.button(f'{recipe.name} ({recipe.author})',
                                 action=buttons[recipe.name].set_pressed)
        menu.menu.add.button('Cancel', action=cancel_button.set_pressed)

        menu.start()

        if cancel_button.pressed:
            return

        for name, button in buttons.items():
            if button.pressed:
                create_mealprep(gui, ingredient_db, recipe_db, mealprep_db, recipe_db.get_recipe(name))
