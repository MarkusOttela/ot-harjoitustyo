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

from src.common.enums      import ColorScheme
from src.common.exceptions import ReturnToMainMenu
from src.common.utils      import get_list_of_user_account_names
from src.common.validation import strings

from src.ui.gui_menu         import GUIMenu
from src.ui.callback_classes import Button, StringInput

if typing.TYPE_CHECKING:
    from src.ui.gui import GUI


def register_credentials(gui: 'GUI') -> tuple:
    """Get credentials for new user."""
    title         = 'Create Account'
    message       = 'Welcome! To start, enter your desired credentials.'
    error_message = ''

    user_name = StringInput()

    while True:
        try:
            menu = GUIMenu(gui, title)

            password_1 = StringInput()
            password_2 = StringInput()

            done_bt   = Button(menu, closes_menu=True)
            return_bt = Button(menu, closes_menu=True)

            menu.menu.add.label(f'{message}\n')

            menu.menu.add.text_input(f'Your name: ',
                                     onchange=user_name.set_value,
                                     default=user_name.value,
                                     maxchar=20,
                                     valid_chars=strings,
                                     font_color=ColorScheme.FONT_COLOR.value)

            menu.menu.add.text_input(f'Password: ',
                                     onchange=password_1.set_value,
                                     password=True,
                                     font_color=ColorScheme.FONT_COLOR.value)

            menu.menu.add.text_input(f'Password (again): ',
                                     onchange=password_2.set_value,
                                     password=True,
                                     font_color=ColorScheme.FONT_COLOR.value)

            menu.menu.add.button('Done', done_bt.set_pressed)
            menu.menu.add.label('')
            menu.menu.add.button('Cancel', return_bt.set_pressed)

            menu.show_error_message(error_message)
            menu.start()

            if return_bt.pressed:
                raise ReturnToMainMenu

            if done_bt.pressed:

                if user_name.value == '':
                    raise ValueError("Please specify a user name")

                if user_name.value in get_list_of_user_account_names():
                    raise ValueError(f"Error: The user account {user_name.value} already exists!")

                if password_1.value != password_2.value:
                    raise ValueError("Error: Passwords did not match!")

                return user_name.value, password_1.value

        except ValueError as e:
            error_message = e.args[0]
            continue
