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

from src.common.crypto import derive_database_key
from src.common.enums  import Gender

from src.entities.user             import User
from src.entities.user_credentials import UserCredentials

from src.ui.screens.initial_survey.get_body_measurements    import get_body_measurements
from src.ui.screens.initial_survey.initial_survey           import get_dob_and_gender
from src.ui.screens.initial_survey.start_diet_survey        import start_diet_survey
from src.ui.screens.account_management.register_credentials import register_credentials

if typing.TYPE_CHECKING:
    from src.ui.gui import GUI


def register_new_user(gui: 'GUI') -> User:
    """Get initial information from user and create a new User object."""
    username, password = register_credentials(gui)
    dob, is_male       = get_dob_and_gender(gui)
    weight, height     = get_body_measurements(gui)
    pal, diet_stage    = start_diet_survey(gui)
    salt, database_key = derive_database_key(password)

    # We have all values, now we can generate the database entries
    user_credentials = UserCredentials(username, salt, database_key)
    user             = User(user_credentials,
                            dob,
                            Gender.MALE if is_male else Gender.FEMALE,
                            weight,
                            height,
                            pal,
                            diet_stage)

    user.set_morning_weight(weight)
    return user
