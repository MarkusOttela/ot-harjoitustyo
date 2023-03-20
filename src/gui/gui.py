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

import pygame

from src.common.statics import Literals, ColorSchemeDark


class GUI:
    """GUI is a wrapper object for the graphical user interface.

    It's effectively a UI god object that is passed around
    the program, and that contains everything wrt. pygame
    and pygame-menu.
    """

    def __init__(self) -> None:
        """Create new GUI object."""
        self.init_pygame()
        self.color = ColorSchemeDark
        self.clock = pygame.time.Clock()

    @staticmethod
    def init_pygame()-> None:
        """Initialize pygame."""
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(Literals.PROGRAM_NAME.value)
        pygame.display.set_icon(pygame.image.load(Literals.ICON_FILE.value))
        pygame.display.set_mode(Literals.RESOLUTION.value)

    def tick(self) -> None:
        """Advance the clock by one tick."""
        self.clock.tick(Literals.FPS.value)
