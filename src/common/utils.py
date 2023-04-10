#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

"""
Calorienator - Diet tracker
Copyright (C) 2023 Markus Ottela

This file is part of Calorienator.
Calorienator is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. Calorienator is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License
along with Calorienator. If not, see <https://www.gnu.org/licenses/>.
"""

import os
import typing

from src.common.exceptions import ignored

if typing.TYPE_CHECKING:
    pass


def ensure_dir(directory: str) -> None:
    """Ensure directory exists."""
    name = os.path.dirname(directory)
    if not os.path.exists(name):
        with ignored(FileExistsError):
            os.makedirs(name)
