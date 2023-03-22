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

from typing import TYPE_CHECKING

from src.gui.gui_menu                 import GUIMenu
from src.gui.screens.callback_classes import BooleanSelector

if TYPE_CHECKING:
    from src.gui.gui import GUI


def get_yes(gui:         'GUI',
            title:       str,
            description: str,
            default_str: str,
            ) -> bool:
    """Get a boolean value from a yes/no question from the user."""
    yes = 'Yes'
    no  = 'No'

    if default_str not in [yes, no]:
        raise ValueError("Invalid answer.")

    default_bool   = default_str.lower().capitalize()==yes
    bool_selection = BooleanSelector(default_value=default_bool)

    menu = GUIMenu(gui, title)
    menu.menu.add.toggle_switch(f'{description}:',
                                onchange=bool_selection.set_value,
                                state_text=(yes, no),
                                default=not default_bool,
                                state_values=(True, False))

    menu.menu.add.button('Done', action=menu.menu.disable)

    menu.start()

    return bool_selection.value