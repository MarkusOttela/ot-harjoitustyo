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

from typing import Any

if typing.TYPE_CHECKING:
    from src.ui.gui_menu import GUIMenu


class Button:
    """Button callback-object."""

    def __init__(self, menu: 'GUIMenu', closes_menu: bool = False) -> None:
        """Create new Button object."""
        self.menu        = menu
        self.closes_menu = closes_menu
        self.pressed     = False

    def set_pressed(self) -> None:
        """Set value of the button to True (=pressed)."""
        self.pressed = True
        if self.closes_menu:
            self.menu.menu.disable()


class StringInput:
    """String input callback-object."""

    def __init__(self) -> None:
        """Create new StringInput object."""
        self.value = ''

    def set_value(self, value: str) -> None:
        """Set value to the string input field."""
        self.value = value


class DropSelection:
    """DropSelection input callback-object."""

    def __init__(self) -> None:
        """Create new DropSelection object."""
        self.value = ''

    def set_value(self, _: Any, value: Any) -> None:
        """Set value to the string input field."""
        self.value = value


class BooleanSelector:
    """Boolean selection callback-object."""

    def __init__(self, default_value: bool) -> None:
        """Create new BooleanSelector object."""
        self.value = default_value

    def set_value(self, value: bool) -> None:
        """Set the boolean value to the object."""
        self.value = value


class MultiSelection:
    """Dropdown-menu selection callback-object."""

    def __init__(self) -> None:
        self.sel_list: list = []

    def set_value(self, selection_: Any) -> None:
        """Set the selection values to the object."""
        self.sel_list = [enum_ for name, enum_ in selection_[0]]

    @property
    def values(self) -> list:
        """Get the values."""
        return self.sel_list
