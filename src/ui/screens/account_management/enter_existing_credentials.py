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
from src.common.exceptions import IncorrectPassword, ReturnToMainMenu
from src.common.utils      import get_list_of_user_account_names

from src.entities.user_credentials import UserCredentials

from src.ui.callback_classes import Button, DropSelection, StringInput
from src.ui.gui_menu         import GUIMenu

if typing.TYPE_CHECKING:
    from src.ui.gui import GUI


def enter_existing_credentials(gui: 'GUI') -> UserCredentials:
    """Login with existing user account."""
    title         = 'Login existing user'
    error_message = ''

    accounts = get_list_of_user_account_names()
    ds_items = [(a, a) for a in accounts]

    user_name_ds        = DropSelection()
    default_uname_index = None

    # If there's only one user, automatically select it from the drop-down list.
    if len(accounts) == 1:
        default_uname_index = 0
        user_name_ds.set_value(None, accounts[0])

    while True:
        try:
            menu = GUIMenu(gui, title)

            done_bt   = Button(menu, closes_menu=True)
            return_bt = Button(menu, closes_menu=True)
            password  = StringInput()

            menu.menu.add.dropselect('Select User Account',
                                     onreturn=user_name_ds.set_value,
                                     items=ds_items,  # type: ignore
                                     default=default_uname_index,
                                     selection_box_width=280,
                                     **gui.drop_selection_theme)

            menu.menu.add.text_input('Password: ',
                                     onchange=password.set_value,
                                     password=True,
                                     password_char=' ',
                                     font_color=ColorScheme.FONT_COLOR.value)

            menu.menu.add.button('Done', done_bt.set_pressed)
            menu.menu.add.label('')
            menu.menu.add.button('Return', return_bt.set_pressed)

            menu.show_error_message(error_message)
            menu.start()

            if return_bt.pressed:
                raise ReturnToMainMenu

            if done_bt.pressed:

                if not user_name_ds.value:
                    raise ValueError('Error: No account selected')

                default_uname_index = accounts.index(user_name_ds.value)

                try:
                    return UserCredentials.from_password(user_name_ds.value, password.value)
                except IncorrectPassword as exception:
                    raise ValueError(f"Error: {exception}") from IncorrectPassword

        except ValueError as exception:
            error_message = exception.args[0]
            continue
