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

from src.common.exceptions                import IncorrectPassword, AbortMenuOperation
from src.common.security.user_credentials import UserCredentials
from src.common.statics                   import Directories
from src.common.utils                     import ensure_dir, get_list_of_user_account_names

from src.entities.user import User

from src.ui.gui_menu                 import GUIMenu
from src.ui.screens.callback_classes import DropSelection, Button, StringInput
from src.ui.screens.show_message     import show_message

if typing.TYPE_CHECKING:
    from src.ui.gui import GUI


def login_existing_user(gui: 'GUI') -> User:
    """Login with existing user account"""
    ensure_dir(Directories.USERDATA.value)

    accounts  = get_list_of_user_account_names()
    sel_items = [(a, a) for a in accounts]

    title = 'Login existing user'

    user_name_ds = DropSelection()
    default_un   = None

    while True:
        menu = GUIMenu(gui, title)

        return_bt = Button(menu, closes_menu=True)
        password  = StringInput()

        menu.menu.add.dropselect('Select User Account',
                                 onreturn=user_name_ds.set_value,
                                 items=sel_items,  # type: ignore
                                 default=default_un,
                                 selection_box_width=280)

        menu.menu.add.text_input(f'Password: ', onchange=password.set_value, password=True)
        menu.menu.add.button('Done', action=menu.menu.disable)
        menu.menu.add.label(f'')
        menu.menu.add.button('Return', return_bt.set_pressed)

        menu.start()

        if return_bt.pressed:
            raise AbortMenuOperation

        if not user_name_ds.value:
            show_message(gui, title, 'Error: No account selected')
            continue

        default_un = accounts.index(user_name_ds.value)

        try:
            user_credentials = UserCredentials.from_password(user_name_ds.value, password.value)
        except IncorrectPassword as f:
            show_message(gui, title, f"Error: {f}")
            continue

        return User(user_credentials)
