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
import shutil
import typing

from src.common.enums import Gender, PhysicalActivityLevel, DietType
from src.entities.user import User
from src.entities.user_credentials import UserCredentials

if typing.TYPE_CHECKING:
    pass


def cd_unit_test() -> str:
    """Create a directory for the unit test and change to it.

    Separate working directory for unit test protects existing user data
    and allows running tests in parallel.
    """
    name = f"unit_test_{(os.urandom(16)).hex()}/"
    try:
        os.mkdir(name)
    except FileExistsError:
        pass
    os.chdir(name)
    return name


def cleanup(name) -> None:
    """Remove unit test related directory."""
    os.chdir('..')
    shutil.rmtree(f'{name}/')


def create_mock_user() -> User:
    """Create mock user for unit testing purposes."""
    user_credentials = UserCredentials('unittest', salt=32*b'a', database_key=32*b'a')
    user = User(user_credentials,
                dob='01/01/1990',
                gender=Gender.MALE,
                init_weight=80.0,
                height=180,
                pal=PhysicalActivityLevel.MODERATELY_ACTIVE,
                diet_type=DietType.DIET)
    user.set_morning_weight(80.1)
    return user
