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

from enum import Enum, unique


class Program(Enum):
    """Program information and global settings."""
    NAME       = 'Calorinator'
    VERSION    = '0.23.05'
    RESOLUTION = (1920 - 80, 1080 - 80)
    FPS        = 60


@unique
class AssetFiles(Enum):
    """Paths to assets."""
    ICON_FILE  = 'Assets/icon.png'
    BACKGROUND = 'Assets/background.jpg'


class CalContent(Enum):
    """Calorie content of macros."""
    KCAL_PER_GRAM_CARB    = 4
    KCAL_PER_GRAM_PROTEIN = 4
    KCAL_PER_GRAM_FAT     = 9


@unique
class Color(Enum):
    """Pygame colors."""
    WHITE   = (255, 255, 255)
    RED     = (255,   0,   0)
    BLACK   = (  0,   0,   0)
    GREY    = ( 30,  30,  30)
    MGREY   = ( 59,  59,  59)
    LGREY   = (180, 180, 180)
    CELESTE = ( 14, 128, 113)


@unique
class ColorScheme(Enum):
    """Program's color scheme."""
    BACKGROUND = Color.GREY.value
    FONT_COLOR = Color.LGREY.value


class Conversion(Enum):
    """Conversion values."""
    DAYS_PER_YEAR = 365.25


@unique
class DatabaseFileName(Enum):
    """Names of database file names."""
    USER_DATABASE   = 'UserData'
    SHARED_DATABASE = 'SharedData'


@unique
class DatabaseTableName(Enum):
    """Database table names."""
    INGREDIENTS = 'Ingredients'
    RECIPES     = 'Recipes'
    MEALPREPS   = 'Mealpreps'


class DatabaseTypes(Enum):
    """SQL Database types."""
    TEXT = 'TEXT'
    REAL = 'REAL'
    LIST = 'TEXT'


@unique
class DietType(Enum):
    """Diet types."""
    DIET                   = 'Diet'
    MUSCLE_MASS_GROWTH     = 'Muscle mass growth'
    BODY_BUILDING          = 'Body building'
    SHREDDED_BODY_BUILDING = 'Shredded body building'


class Directories(Enum):
    """Program directories"""
    USER_DATA = 'user_data'


@unique
class FontSize(Enum):
    """Font sizes."""
    FONT_SIZE_NORMAL = 40
    FONT_SIZE_SMALL  = 30
    FONT_SIZE_XSMALL = 20


class Format(Enum):
    """String formats."""
    DATETIME_DATE   = '%d/%m/%Y'
    DATETIME_TSTAMP = '%d/%m/%Y-%H:%M:%S'


@unique
class Gender(Enum):
    """Gender for approximation algorithms."""
    MALE   = 'Male'
    FEMALE = 'Female'


@unique
class PhysicalActivityLevel(Enum):
    """Activity lifestyle types."""
    SEDENTARY         = 'Sedentary'
    LIGHTLY_ACTIVE    = 'Lightly Active'
    MODERATELY_ACTIVE = 'Moderately Active'
    HIGHLY_ACTIVE     = 'Highly Active'


class TefMultipliers(Enum):
    """TEF-multipliers.

    For explanation, see
        https://en.wikipedia.org/wiki/Specific_dynamic_action
    """
    TEF_CARB_EFFICIENCY    = 0.9
    TEF_PROTEIN_EFFICIENCY = 0.725
    TEF_FAT_EFFICIENCY     = 0.9


@unique
class DBKeys(Enum):
    """JSON Database keys."""
    NAME           = 'name'
    BIRTHDAY       = 'birthday'
    GENDER         = 'gender'
    HEIGHT_CM      = 'height_cm'
    INIT_WEIGHT_KG = 'init_weight_kg'
    PAL            = 'pal'
    DIET_TYPE      = 'diet_type'
    WEIGHT_LOG     = 'weight_log'
    MEAL_LOG       = 'meal_log'
