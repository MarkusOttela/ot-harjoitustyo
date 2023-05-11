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

from src.ui.gui_menu         import GUIMenu
from src.ui.callback_classes import Button

from src.ui.screens.mealprep_menu.select_mealprep_recipe  import select_mealprep_recipe_to_create
from src.ui.screens.mealprep_menu.select_mealprep_to_edit import select_mealprep_to_edit

if typing.TYPE_CHECKING:
    from src.database.unencrypted_database import MealprepDatabase, IngredientDatabase, RecipeDatabase
    from src.ui.gui import GUI


def manage_mealpreps_menu(gui           : 'GUI',
                          mealprep_db   : 'MealprepDatabase',
                          recipe_db     : 'RecipeDatabase',
                          ingredient_db : 'IngredientDatabase',
                          ) -> None:
    """Render the Manage Mealprep sub menu."""
    while True:
        menu = GUIMenu(gui, 'Manage Mealpreps')

        create_mealprep      = Button(menu, closes_menu=True)
        edit_mealprep_button = Button(menu, closes_menu=True)
        return_button        = Button(menu, closes_menu=True)

        menu.menu.add.button('Create Mealprep', action=create_mealprep.set_pressed)
        menu.menu.add.button('Edit Mealprep',   action=edit_mealprep_button.set_pressed)
        menu.menu.add.button('Return',          action=return_button.set_pressed)

        menu.start()

        if create_mealprep.pressed:
            select_mealprep_recipe_to_create(gui, mealprep_db, recipe_db, ingredient_db)
            continue

        if edit_mealprep_button.pressed:
            select_mealprep_to_edit(gui, mealprep_db, ingredient_db)
            continue

        if return_button.pressed:
            return
