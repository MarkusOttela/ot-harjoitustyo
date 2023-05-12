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

from datetime import datetime

from src.common.exceptions import AbortMenuOperation
from src.common.enums      import Gender, Format
from src.common.validation import date

from src.ui.gui_menu         import GUIMenu
from src.ui.callback_classes import Button, StringInput, BooleanSelector

if typing.TYPE_CHECKING:
    from src.ui.gui import GUI


def get_dob_and_gender(gui: 'GUI') -> tuple:
    """Get the date of birth, and the gender of the user."""
    error_message = ''

    dob     = StringInput()
    is_male = BooleanSelector(True)

    while True:

        menu = GUIMenu(gui, "Initial Survey")

        try:
            return_bt = Button(menu, closes_menu=True)

            menu.menu.add.text_input('Your DoB <dd/mm/yyyy> : ',
                                     valid_chars=date, maxchar=10,
                                     onchange=dob.set_value,
                                     default=dob.value)

            menu.menu.add.toggle_switch('Your gender :',
                                        onchange=is_male.set_value,
                                        state_text=(Gender.FEMALE.value, Gender.MALE.value),
                                        state_values=(False, True),
                                        default=is_male.value,
                                        **gui.toggle_switch_theme)

            menu.menu.add.button('Done', action=menu.menu.disable)
            menu.menu.add.label(f'')
            menu.menu.add.button('Cancel', return_bt.set_pressed)

            menu.show_error_message(error_message)
            menu.start()

            if return_bt.pressed:
                raise AbortMenuOperation

            # Validate inputs
            if dob.value == '':
                raise ValueError(f'Please enter your birthday')

            try:
                datetime.strptime(dob.value, Format.DATETIME_DATE.value)
            except ValueError:
                raise ValueError("Error: Invalid birthday format")

            return dob.value, is_male.value

        except ValueError as e:
            error_message = e.args[0]
            continue
