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

from src.common.enums        import ColorScheme
from src.common.validation   import floats, validate_positive_float

from src.ui.callback_classes import StringInput
from src.ui.gui_menu         import GUIMenu

if typing.TYPE_CHECKING:
    from src.entities.user import User
    from src.ui.gui        import GUI


def get_morning_weight(gui: 'GUI', user: 'User') -> None:
    """Get morning weight from the user."""
    title         = 'Morning Weight'
    error_message = ''

    weight = StringInput()

    while True:
        menu = GUIMenu(gui, title)
        try:
            menu.menu.add.label('Good Morning!\n')

            menu.menu.add.text_input('Your weight (kg) : ',
                                     onchange=weight.set_value,
                                     valid_chars=floats,
                                     maxchar=5,
                                     font_color=ColorScheme.FONT_COLOR.value)

            menu.menu.add.button('Done', action=menu.menu.disable)

            menu.show_error_message(error_message)
            menu.start()

            weight_f = validate_positive_float(weight.value)
            bmi      = weight_f / ((user.height_cm / 100) ** 2)

            if bmi > 40:
                raise ValueError(f"Invalid weight (BMI of value {bmi:.1f} is dangerously high!)")
            elif bmi < 16:
                raise ValueError(f"Invalid weight (BMI of value {bmi:.1f} is dangerously low!)")

            user.set_morning_weight(weight_f)
            return

        except ValueError as exception:
            error_message = exception.args[0]
            continue
