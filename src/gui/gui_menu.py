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

from typing import Optional

from pygame_menu import BaseImage, Menu, Theme

from src.common.statics import AsssetFiles, ColorScheme, Program

if typing.TYPE_CHECKING:
    from src.gui.gui import GUI


class GUIMenu:
    """GUIMenu is a wrapper for Calorinator's Pygame-menu that holds settings etc."""

    def __init__(self,  # pylint: disable=too-many-arguments
                 gui              : 'GUI',
                 menu_title       : str,
                 columns          : int           = 1,
                 rows             : Optional[int] = None,
                 column_max_width : Optional[int] = None
                 ) -> None:
        """Create new GUIMenu with pygame-menu."""
        self.gui = gui

        self.background_image = BaseImage(image_path=AsssetFiles.BACKGROUND.value)

        self.theme = self.get_theme()
        self.theme.set_background_color_opacity(0.75)

        resolution_x = Program.RESOLUTION.value[0]
        resolution_y = Program.RESOLUTION.value[1]
        self.menu = Menu(width=resolution_x, height=resolution_y,
                         title=menu_title, theme=self.theme,
                         columns=columns, rows=rows,
                         column_max_width=column_max_width)

    @staticmethod
    def get_theme() -> Theme:
        """Get the theme for the menu."""
        return Theme(background_color=ColorScheme.BACKGROUND.value,
                     cursor_color=(255, 255, 255),
                     cursor_selection_color=(80, 80, 80, 120),
                     scrollbar_color=(39, 41, 42),
                     scrollbar_slider_color=(65, 66, 67),
                     scrollbar_slider_hover_color=(90, 89, 88),
                     selection_color=ColorScheme.FONT_COLOR.value,
                     title_background_color=(47, 48, 51),
                     title_font_color=(215, 215, 215),
                     widget_font_color=ColorScheme.FONT_COLOR.value,
                     widget_box_background_color=ColorScheme.BACKGROUND.value)

    def get_background(self) -> BaseImage:
        """Get the background image."""
        return self.background_image.draw(self.gui.display)

    def start(self) -> None:
        """Start the menu."""
        self.menu.mainloop(self.gui.display,
                           bgfun=self.get_background,
                           fps_limit=Program.FPS.value)
