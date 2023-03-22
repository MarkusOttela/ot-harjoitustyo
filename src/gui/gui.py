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

import pygame

from src.common.statics import Literals, ColorScheme, AsssetFiles


class GUI:
    """GUI is a wrapper object for the graphical user interface.

    It's effectively a UI god object that is passed around
    the program, and that contains everything wrt. pygame
    and pygame-menu.
    """

    def __init__(self) -> None:
        """Create new GUI object."""
        self.init_pygame()
        self.color   = ColorScheme
        self.clock   = pygame.time.Clock()
        self.display = pygame.display.set_mode(Literals.RESOLUTION.value)

    @staticmethod
    def init_pygame()-> None:
        """Initialize pygame."""
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(Literals.PROGRAM_NAME.value)
        pygame.display.set_icon(pygame.image.load(AsssetFiles.ICON_FILE.value))

    def tick(self) -> None:
        """Advance the clock by one tick."""
        self.clock.tick(Literals.FPS.value)

    def clear_screen(self) -> None:
        """Clear the screen."""
        self.display.fill(self.color.BACKGROUND.value)

    @staticmethod
    def draw_screen() -> None:
        """Display contents of the screen."""
        pygame.display.flip()

    @staticmethod
    def check_events() -> None:
        """Check if events have occurred."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
