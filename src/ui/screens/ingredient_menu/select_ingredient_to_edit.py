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

from src.ui.callback_classes     import Button
from src.ui.gui_menu             import GUIMenu
from src.ui.screens.show_message import show_message

from src.ui.screens.ingredient_menu.edit_ingredient import edit_ingredient

if typing.TYPE_CHECKING:
    from src.database.unencrypted_database import IngredientDatabase
    from src.ui.gui import GUI


def select_ingredient_to_edit(gui           : 'GUI',
                              ingredient_db : 'IngredientDatabase'
                              ) -> None:
    """Render the `Select Ingredient to Edit` menu."""
    title = 'Select Ingredient to Edit'
    while True:
        menu = GUIMenu(gui, title)

        list_of_ingredients = ingredient_db.get_list_of_ingredients()

        if not list_of_ingredients:
            show_message(gui, title, 'No ingredients yet in database.')
            return

        buttons   = {i.name: Button(menu, closes_menu=True) for i in list_of_ingredients}
        cancel_bt = Button(menu, closes_menu=True)

        for ingredient in list_of_ingredients:
            menu.menu.add.button(ingredient.name, action=buttons[ingredient.name].set_pressed)
        menu.menu.add.button('Cancel', action=cancel_bt.set_pressed)

        menu.start()

        if cancel_bt.pressed:
            return

        for name, button in buttons.items():
            if button.pressed:
                edit_ingredient(gui, ingredient_db, ingredient_db.get_ingredient(name))

                # edit_ingredient might delete the last Ingredient before it returns
                if not ingredient_db.get_list_of_ingredients():
                    return
