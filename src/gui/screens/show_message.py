#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

"""
Calorienator - Diet tracker
Copyright (C) 2023 Markus Ottela

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

from typing import TYPE_CHECKING

from src.gui.gui_menu import GUIMenu

if TYPE_CHECKING:
    from src.gui.gui import GUI


def show_message(gui     : 'GUI',
                 title   : str,
                 message : str,
                 ) -> None:
    """Display a message to the user and wait for them to dismiss it."""
    menu = GUIMenu(gui, title)
    menu.menu.add.label(f'{message}\n')
    menu.menu.add.button('Done', action=menu.menu.disable)
    menu.start()
    return None
