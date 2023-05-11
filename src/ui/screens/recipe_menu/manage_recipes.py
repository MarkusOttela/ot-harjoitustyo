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

from typing import Optional

from src.ui.gui_menu         import GUIMenu
from src.ui.callback_classes import Button

from src.ui.screens.recipe_menu.add_recipe            import add_recipe_menu
from src.ui.screens.recipe_menu.select_recipe_to_edit import select_recipe_to_edit
from src.ui.screens.show_message                      import show_message

if typing.TYPE_CHECKING:
    from src.database.unencrypted_database import IngredientDatabase, RecipeDatabase
    from src.entities.user import User
    from src.ui.gui        import GUI


def manage_recipes_menu(gui           : 'GUI',
                        user          : Optional['User'],
                        recipe_db     : 'RecipeDatabase',
                        ingredient_db : 'IngredientDatabase'
                        ) -> None:
    """Render the Manage Recipes sub menu."""
    if not ingredient_db.has_ingredients():
        show_message(gui, 'Error', 'No ingredients have been created yet.')
        return

    while True:
        menu = GUIMenu(gui, 'Manage Recipes')

        add_recipe_button  = Button(menu, closes_menu=True)
        edit_recipe_button = Button(menu, closes_menu=True)
        return_button      = Button(menu, closes_menu=True)

        menu.menu.add.button('Add Recipe',  action=add_recipe_button.set_pressed)
        menu.menu.add.button('Edit Recipe', action=edit_recipe_button.set_pressed)
        menu.menu.add.button('Return',      action=return_button.set_pressed)

        menu.start()

        if add_recipe_button.pressed:
            add_recipe_menu(gui, user, recipe_db, ingredient_db)
            continue

        if edit_recipe_button.pressed:
            select_recipe_to_edit(gui, recipe_db, ingredient_db)
            continue

        if return_button.pressed:
            return
