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
