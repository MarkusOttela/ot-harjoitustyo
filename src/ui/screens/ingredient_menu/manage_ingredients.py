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

from src.ui.callback_classes import Button
from src.ui.gui_menu         import GUIMenu

from src.ui.screens.ingredient_menu.add_ingredient            import add_ingredient_menu
from src.ui.screens.ingredient_menu.select_ingredient_to_edit import select_ingredient_to_edit

if typing.TYPE_CHECKING:
    from src.database.unencrypted_database import IngredientDatabase
    from src.ui.gui import GUI


def manage_ingredients_menu(gui           : 'GUI',
                            ingredient_db : 'IngredientDatabase'
                            ) -> None:
    """Render the Manage Ingredient sub menu."""
    while True:
        menu = GUIMenu(gui, 'Manage Ingredients')

        add_ingredient_bt  = Button(menu, closes_menu=True)
        edit_ingredient_bt = Button(menu, closes_menu=True)
        return_bt          = Button(menu, closes_menu=True)

        menu.menu.add.button('Add Ingredient',  action=add_ingredient_bt.set_pressed)
        menu.menu.add.button('Edit Ingredient', action=edit_ingredient_bt.set_pressed)
        menu.menu.add.button('Return',          action=return_bt.set_pressed)

        menu.start()

        if add_ingredient_bt.pressed:
            add_ingredient_menu(gui, ingredient_db)
            continue

        if edit_ingredient_bt.pressed:
            select_ingredient_to_edit(gui, ingredient_db)
            continue

        if return_bt.pressed:
            return
