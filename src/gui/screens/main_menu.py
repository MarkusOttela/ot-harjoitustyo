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

from src.common.statics                 import Literals
from src.gui.gui_menu                   import GUIMenu
from src.gui.screens.callback_classes   import Button
from src.gui.screens.manage_ingredients import manage_ingredients_menu

if typing.TYPE_CHECKING:
    from src.gui.gui import GUI
    from src.database.ingredient_database import IngredientDatabase


def main_menu(gui           : 'GUI',
              ingredient_db : 'IngredientDatabase'
              ) -> None:
    """Render the Main Menu."""
    while True:
        menu = GUIMenu(gui, Literals.PROGRAM_NAME.value)

        ingredient_menu = Button(menu, closes_menu=True)
        exit_button     = Button(menu, closes_menu=True)

        menu.menu.add.button('Manage Ingredients',  action=ingredient_menu.set_pressed)
        menu.menu.add.button('Exit',                action=exit_button.set_pressed)

        menu.start()

        if ingredient_menu.pressed:
            manage_ingredients_menu(gui, ingredient_db)
            continue

        if exit_button.pressed:
            exit()
