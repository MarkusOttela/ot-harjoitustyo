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

from src.gui.gui_menu import GUIMenu

if typing.TYPE_CHECKING:
    from src.gui.gui import GUI


class Button:
    """Button callback-object."""

    def __init__(self, menu: GUIMenu) -> None:
        self.menu    = menu
        self.pressed = False

    def set_pressed(self) -> None:
        self.pressed = True
        self.menu.menu.disable()


def main_menu(gui: 'GUI') -> None:
    """Render the main menu."""

    menu = GUIMenu(gui, 'Calorinator')

    exit_button = Button(menu)

    menu.menu.add.button('Exit', action=exit_button.set_pressed)
    menu.start()

    if exit_button.pressed:
        exit()
