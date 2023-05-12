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

import sys

import pygame

from src.common.exceptions import EscPressed
from src.common.enums      import Program, ColorScheme, AssetFiles, Color


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
        self.display = pygame.display.set_mode(Program.RESOLUTION.value)

    @staticmethod
    def init_pygame() -> None:
        """Initialize pygame."""
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(Program.NAME.value)
        pygame.display.set_icon(pygame.image.load(AssetFiles.ICON_FILE.value))

    def tick(self) -> None:
        """Advance the clock by one tick."""
        self.clock.tick(Program.FPS.value)

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
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    raise EscPressed

    @property
    def drop_multi_selection_theme(self) -> dict:
        """Drop-selection theme for multiple choice boxes.."""
        return dict(selection_box_bgcolor=Color.MGREY.value,

                    selection_option_border_color=Color.BLACK.value,
                    selection_option_font_color=Color.LGREY.value,

                    selection_option_selected_font_color=Color.WHITE.value,
                    selection_option_selected_bgcolor=Color.CELESTE.value,
                    selection_option_selected_box_color=Color.WHITE.value,

                    selection_option_active_font_color=Color.LGREY.value,

                    selection_box_arrow_color=Color.GREY.value,
                    selection_box_border_color=Color.BLACK.value,

                    scrollbar_slider_color=Color.GREY.value,
                    scrollbar_slider_hover_color=Color.BLACK.value,
                    scrollbar_color=Color.LGREY.value,
                    scrollbar_shadow_color=Color.BLACK.value,
                    )

    @property
    def drop_selection_theme(self) -> dict:
        """Drop-selection theme."""
        return dict(selection_box_bgcolor=Color.MGREY.value,

                    selection_option_border_color=Color.BLACK.value,
                    selection_option_font_color=Color.LGREY.value,

                    selection_option_selected_font_color=Color.WHITE.value,
                    selection_option_selected_bgcolor=Color.CELESTE.value,

                    selection_box_arrow_color=Color.GREY.value,
                    selection_box_border_color=Color.BLACK.value,

                    scrollbar_slider_color=Color.GREY.value,
                    scrollbar_slider_hover_color=Color.BLACK.value,
                    scrollbar_color=Color.LGREY.value,
                    scrollbar_shadow_color=Color.BLACK.value,
                    )

    @property
    def toggle_switch_theme(self) -> dict:
        """Toggle switch theme."""
        return dict(font_color=Color.LGREY.value,
                    border_color=Color.LGREY.value,
                    switch_border_color=Color.LGREY.value,
                    state_text_font_color=(Color.WHITE.value, Color.WHITE.value),
                    slider_color=Color.GREY.value,
                    state_color=(Color.CELESTE.value, Color.CELESTE.value)
                    )
