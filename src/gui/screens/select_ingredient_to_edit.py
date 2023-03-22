#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

"""
Calorienator - Diet tracker
Copyright (C) Markus Ottela

This file is part of Calorienator.
Calorienator is free software: you can redistribute it and/or modify it under the 
terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version. Calorienator is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
details. You should have received a copy of the GNU General Public License
along with Calorienator. If not, see <https://www.gnu.org/licenses/>.
"""

import typing

from src.gui.gui_menu                 import GUIMenu
from src.gui.screens.edit_ingredient  import edit_ingredient
from src.gui.screens.show_message     import show_message
from src.gui.screens.callback_classes import Button

if typing.TYPE_CHECKING:
    from src.database.ingredient_database import IngredientDatabase
    from src.gui.gui import GUI


def select_ingredient_to_edit(gui: 'GUI', ingredient_db: 'IngredientDatabase') -> None:
    """Render the `Select Ingredient to Edit` menu."""
    title = 'Select Ingredient to Edit'
    while True:
        menu = GUIMenu(gui, title)

        list_of_ingredients = ingredient_db.get_list_of_ingredients()

        if not list_of_ingredients:
            show_message(gui, title, 'No ingredients yet in database.')
            return

        buttons       = {i.name: Button(menu, closes_menu=True) for i in list_of_ingredients}
        cancel_button = Button(menu, closes_menu=True)

        for ingredient in list_of_ingredients:
            menu.menu.add.button(f'{ingredient.name} ({ingredient.manufacturer})', action=buttons[ingredient.name].set_pressed)
        menu.menu.add.button('Cancel', action=cancel_button.set_pressed)

        menu.start()

        if cancel_button.pressed:
            return

        for name, button in buttons.items():
            if button.pressed:
                edit_ingredient(gui, ingredient_db, ingredient_db.get_ingredient(name))
