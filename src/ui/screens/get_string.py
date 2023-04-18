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

from src.ui.gui_menu                 import GUIMenu
from src.ui.screens.callback_classes import StringInput

if typing.TYPE_CHECKING:
    from src.ui.gui import GUI


def get_string(gui:         'GUI',
               title:       str,
               message:     str,
               description: str,
               is_password: bool = False,
               ) -> str:
    """Get a string from the user."""
    user_input = StringInput()

    menu = GUIMenu(gui, title)

    menu.menu.add.label(f'{message}\n')
    menu.menu.add.text_input(
        f'{description}: ',
        onchange=user_input.set_value,
        password=is_password)
    menu.menu.add.button(f'Done', action=menu.menu.disable)
    menu.start()

    return user_input.value
