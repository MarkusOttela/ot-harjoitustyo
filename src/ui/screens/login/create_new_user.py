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

from src.common.security import derive_database_key

from src.entities.user import User

from src.ui.screens.login.register_credentials import register_credentials

if typing.TYPE_CHECKING:
    from src.ui.gui import GUI


def create_new_user(gui: 'GUI') -> User:
    """Create new user."""
    username, password = register_credentials(gui)
    salt, database_key = derive_database_key(password)
    user               = User(username, salt, database_key)

    return user
