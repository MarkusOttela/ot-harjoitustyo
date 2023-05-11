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

from src.common.validation   import validate_positive_float, floats
from src.ui.gui_menu         import GUIMenu
from src.ui.callback_classes import StringInput

if typing.TYPE_CHECKING:
    from src.entities.user import User
    from src.ui.gui        import GUI


def get_morning_weight(gui: 'GUI', user: 'User') -> None:
    """Get morning weight from the user."""
    weight = StringInput()

    error_message = ''

    while True:
        menu = GUIMenu(gui, "Morning Weight")
        try:

            # Pre-fill only valid inputs if an error occurred.
            if weight.value is not None:
                try:
                    default_weight = str(validate_positive_float(weight.value))
                except ValueError:
                    default_weight = ''
            else:
                default_weight = ''

            menu.menu.add.label('Good Morning!\n')
            menu.menu.add.text_input('Your weight (kg) : ',
                                     onchange=weight.set_value,
                                     default=default_weight,
                                     valid_chars=floats,
                                     maxchar=5)
            menu.menu.add.button('Done', action=menu.menu.disable)
            menu.show_error_message(error_message)
            menu.start()

            weight_kg = validate_positive_float(weight.value)

            user.set_morning_weight(weight_kg)
            return

        except ValueError as e:
            error_message = e.args[0]
            continue
