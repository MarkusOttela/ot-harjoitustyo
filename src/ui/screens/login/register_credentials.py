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

from src.ui.screens.get_string import get_string
from src.ui.screens.show_message import show_message

if typing.TYPE_CHECKING:
    from src.ui.gui import GUI


def register_credentials(gui: 'GUI') -> tuple:
    """Get credentials for new user."""
    title = 'Create Account'
    message = 'Welcome! To start, enter your desired credentials.'

    user_name = get_string(gui, title, message, 'Username')

    while True:
        password1 = get_string(gui, title, message, 'Password',          is_password=True)
        password2 = get_string(gui, title, message, 'Password (repeat)', is_password=True)
        if password1 != password2:
            show_message(gui, title, "Error: Passwords did not match!")
            continue
        break

    return user_name, password1
