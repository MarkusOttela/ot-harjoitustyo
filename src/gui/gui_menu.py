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

from pygame_menu import Menu

from src.common.statics import Literals

if typing.TYPE_CHECKING:
    from src.gui.gui import GUI


class GUIMenu:

    def __init__(self,
                 gui        : 'GUI',
                 menu_title : str
                 ) -> None:
        """Create new GUIMenu with pygame-menu."""
        self.gui = gui

        resolution_x = Literals.RESOLUTION.value[0]
        resolution_y = Literals.RESOLUTION.value[1]
        self.menu = Menu(width=resolution_x, height=resolution_y,
                         title=menu_title)

    def start(self) -> None:
        """Start the menu."""
        self.menu.mainloop(self.gui.display, fps_limit=Literals.FPS.value)
