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

import os
import typing

from src.common.exceptions import IncorrectPassword
from src.common.security.user_credentials import UserCredentials
from src.common.statics                   import Directories
from src.common.utils                     import ensure_dir, get_list_of_user_account_names

from src.entities.user import User

from src.ui.gui_menu                 import GUIMenu
from src.ui.screens.callback_classes import DropSelection
from src.ui.screens.get_string       import get_string
from src.ui.screens.show_message import show_message

if typing.TYPE_CHECKING:
    from src.ui.gui import GUI


def login_existing_user(gui: 'GUI') -> User:
    """Login with existing user account"""
    ensure_dir(Directories.USERDATA.value)

    accounts  = get_list_of_user_account_names()
    sel_items = [(a, a) for a in accounts]

    title = 'Login existing user'

    while True:
        menu  = GUIMenu(gui, title)

        user_name_ds = DropSelection()

        menu.menu.add.dropselect('Select User Account',
                                 onreturn=user_name_ds.set_value,
                                 items=sel_items,
                                 default=None,
                                 selection_box_width=280)

        menu.menu.add.button('Done', action=menu.menu.disable)
        menu.start()

        if not user_name_ds.value:
            show_message(gui, title, 'Error: No account selected')
            continue

        password = get_string(gui, title, 'To log in, please enter your password.', 'Password', is_password=True)

        try:
            user_credentials = UserCredentials.from_password(user_name_ds.value, password)
        except IncorrectPassword as f:
            show_message(gui, title, f"Error: {f}")
            continue
        return User(user_credentials)
