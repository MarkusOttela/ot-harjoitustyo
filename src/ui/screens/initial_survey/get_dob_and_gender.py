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

from src.common.enums      import ColorScheme, Format, Gender
from src.common.exceptions import ReturnToMainMenu
from src.common.validation import date

from src.ui.callback_classes import BooleanSelector, Button, StringInput
from src.ui.gui_menu         import GUIMenu

if typing.TYPE_CHECKING:
    from src.ui.gui import GUI


def get_dob_and_gender(gui: 'GUI') -> tuple:
    """Get the date of birth, and the gender of the user."""
    title         = 'Initial Diet Survey'
    error_message = ''

    dob     = StringInput()
    is_male = BooleanSelector(True)

    while True:
        try:
            menu = GUIMenu(gui, title)

            done_bt   = Button(menu, closes_menu=True)
            return_bt = Button(menu, closes_menu=True)

            menu.menu.add.text_input('Your DoB <dd/mm/yyyy> : ',
                                     onchange=dob.set_value,
                                     valid_chars=date,
                                     maxchar=10,
                                     default=dob.value,
                                     font_color=ColorScheme.FONT_COLOR.value)

            menu.menu.add.toggle_switch('Your gender :',
                                        onchange=is_male.set_value,
                                        state_text=(Gender.FEMALE.value, Gender.MALE.value),
                                        state_values=(False, True),
                                        default=is_male.value,
                                        **gui.toggle_switch_theme)

            menu.menu.add.button('Done', done_bt.set_pressed)
            menu.menu.add.label('')
            menu.menu.add.button('Cancel', return_bt.set_pressed)

            menu.show_error_message(error_message)
            menu.start()

            if return_bt.pressed:
                raise ReturnToMainMenu

            if done_bt.pressed:

                if dob.value == '':
                    raise ValueError('Please enter your birthday')

                try:
                    datetime.strptime(dob.value, Format.DATETIME_DATE.value)
                except ValueError:
                    raise ValueError('Error: Invalid birthday format')

                return dob.value, is_male.value

        except ValueError as exception:
            error_message = exception.args[0]
            continue
