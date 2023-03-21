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

import typing

from typing import Optional

if typing.TYPE_CHECKING:
    from src.gui.gui_menu import GUIMenu


class Button:
    """Button callback-object."""

    def __init__(self, menu: 'GUIMenu', closes_menu: bool = False) -> None:
        self.menu        = menu
        self.closes_menu = closes_menu
        self.pressed     = False

    def set_pressed(self) -> None:
        self.pressed = True
        if self.closes_menu:
            self.menu.menu.disable()

class StringInput:
    """String input callback-object."""

    def __init__(self) -> None:
        self.value = ''

    def set_value(self, g: str) -> None:
        self.value = g


class UserInput:
    """User input callback-object."""

    def __init__(self) -> None:
        self.value:   Optional[str] = None
        self.default: Optional[str] = None

    def set_value(self, value: str) -> None:
        self.value = value
