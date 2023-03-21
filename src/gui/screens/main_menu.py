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
from src.gui.screens.add_ingredient   import add_ingredient_menu
from src.gui.screens.callback_classes import Button

if typing.TYPE_CHECKING:
    from src.gui.gui import GUI


def main_menu(gui: 'GUI') -> None:
    """Render the main menu."""

    while True:
        menu = GUIMenu(gui, 'Calorinator')

        add_ingredient_button = Button(menu, closes_menu=True)
        exit_button           = Button(menu, closes_menu=True)

        menu.menu.add.button('Add Ingredient', action=add_ingredient_button.set_pressed)
        menu.menu.add.button('Exit',           action=exit_button.set_pressed)

        menu.start()

        if add_ingredient_button.pressed:
            add_ingredient_menu(gui)
            continue

        if exit_button.pressed:
            exit()
