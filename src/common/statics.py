#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

"""
Calorienator - Diet tracker
Copyright (C) Markus Ottela

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

from enum import Enum


class Literals(Enum):
    PROGRAM_NAME = 'Calorienator'
    VERSION      = '0.23.03'
    ICON_FILE    = 'icon.png'
    RESOLUTION   = (1600, 900)
    FPS          = 60

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


class ColorSchemeDark(Enum):
    """Dark mode ColorScheme."""
    BACKGROUND = Color.GREY.value
    FONT_COLOR = Color.LGREY.value
