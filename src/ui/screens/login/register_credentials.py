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

from src.common.exceptions           import ReturnToMainMenu
from src.ui.gui_menu                 import GUIMenu
from src.ui.screens.callback_classes import StringInput, Button
from src.ui.screens.show_message import show_message

if typing.TYPE_CHECKING:
    from src.ui.gui import GUI


def register_credentials(gui: 'GUI') -> tuple:
    """Get credentials for new user."""
    title   = 'Create Account'
    message = 'Welcome! To start, enter your desired credentials.'

    user_name = StringInput()

    while True:
        menu = GUIMenu(gui, title)

        password_1 = StringInput()
        password_2 = StringInput()
        return_bt  = Button(menu, closes_menu=True)

        menu.menu.add.label(f'{message}\n')

        menu.menu.add.text_input(f'Your name: ',
                                 onchange=user_name.set_value,
                                 default=user_name.value)

        menu.menu.add.text_input(f'Password: ',         onchange=password_1.set_value, password=True)
        menu.menu.add.text_input(f'Password (again): ', onchange=password_2.set_value, password=True)

        menu.menu.add.button('Done',   action=menu.menu.disable)
        menu.menu.add.label(f'')
        menu.menu.add.button('Return', return_bt.set_pressed)

        menu.start()

        if return_bt.pressed:
            raise ReturnToMainMenu

        if password_1.value == password_2.value:
            return user_name.value, password_1.value

        else:
            show_message(gui, title, "Error: passwords did not match!")
