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
from src.gui.screens.callback_classes import Button, UserInput

if typing.TYPE_CHECKING:
    from src.gui.gui import GUI


def add_ingredient_menu(gui: 'GUI') -> None:
    """Render the `add ingredient` menu."""

    while True:
        menu = GUIMenu(gui, 'Calorinator')

        # Input blocks
        name_field = UserInput()

        return_button = Button(menu, closes_menu=True)
        done_button   = Button(menu, closes_menu=True)

        menu.menu.add.text_input(f'Name: ', onchange=name_field.set_value)

        menu.menu.add.button('Done',   action=done_button.set_pressed)
        menu.menu.add.button('Return', action=return_button.set_pressed)
        menu.start()

        if return_button.pressed:
            return

        if done_button.pressed:
            print(name_field.value)
            return
