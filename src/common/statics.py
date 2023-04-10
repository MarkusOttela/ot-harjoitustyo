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

from enum import Enum


class Program(Enum):
    """Program information and global settings."""
    NAME       = 'Calorinator'
    VERSION    = '0.23.03'
    RESOLUTION = (1600, 900)
    FPS        = 60


class AsssetFiles(Enum):
    """Paths to assets."""
    ICON_FILE  = 'Assets/icon.png'
    BACKGROUND = 'Assets/background.jpg'


class Directories(Enum):
    """Program directories"""
    USERDATA = 'user_data'


class DatabaseFileNames(Enum):
    """Names of database files."""
    INGREDIENT_DATABASE = 'ingredient_database.sqlite3'


class Color(Enum):
    """Pygame colors."""
    WHITE    = (255, 255, 255)
    RED      = (255,   0,   0)
    BLACK    = (  0,   0,   0)
    GREY     = ( 30,  30,  30)
    MGREY    = (59,   59,  59)
    LGREY    = (180, 180, 180)
    CELESTE  = (14,  128, 113)


class ColorScheme(Enum):
    """Program's color scheme."""
    BACKGROUND = Color.GREY.value
    FONT_COLOR = Color.LGREY.value
