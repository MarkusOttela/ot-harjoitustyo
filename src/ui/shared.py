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

from src.common.enums      import Color, ColorScheme
from src.common.validation import floats

from src.ui.gui_menu import GUIMenu


def add_ingredient_gram_inputs(menu               : GUIMenu,
                               metadata           : dict,
                               string_inputs      : dict,
                               failed_conversions : dict,
                               ) -> None:
    """Add text inputs on screen."""
    for i, k in enumerate(list(metadata.keys())):
        warning_color = Color.RED.value
        normal_color  = ColorScheme.FONT_COLOR.value

        valid_chars = None if metadata[k][1] == str else floats
        font_color  = warning_color if k in failed_conversions else normal_color
        menu.menu.add.text_input(f'{metadata[k][0]} (g): ',
                                 onchange=string_inputs[k].set_value,
                                 default=string_inputs[k].value,
                                 valid_chars=valid_chars,
                                 maxchar=19,
                                 font_color=font_color)
    failed_conversions.clear()
