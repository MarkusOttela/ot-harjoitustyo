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

from src.common.statics    import Gender, Color, FontSize
from src.common.validation import date

from src.ui.gui_menu import GUIMenu

if typing.TYPE_CHECKING:
    from src.entities.user import User
    from src.ui.gui        import GUI


def get_dob_and_gender(gui: 'GUI', user: 'User') -> None:
    """Get the date of birth, and the gender of the user."""
    error_message = ''

    # Default
    user.set_gender(gender=Gender.MALE)

    if user.get_birthday():
        return

    while True:

        menu = GUIMenu(gui, "Initial Survey")

        try:
            menu.menu.add.text_input('Your DoB <dd/mm/yyyy> : ',
                                     valid_chars=date, maxchar=10,
                                     onchange=user.set_birthday,
                                     default=user.get_birthday())

            menu.menu.add.toggle_switch('Your gender :',
                                        onchange=user.set_gender,
                                        state_text=(Gender.FEMALE.value, Gender.MALE.value),
                                        state_values=(Gender.FEMALE, Gender.MALE),
                                        default=user.get_gender() != Gender.MALE.value)

            menu.menu.add.button('Done', action=menu.menu.disable)

            if error_message:
                menu.menu.add.label(error_message,
                                    font_color=Color.RED.value,
                                    font_size=FontSize.FONT_SIZE_SMALL.value)

            menu.start()

            # Validate inputs
            for requested_action, var in [( 'enter your birthday', user.get_birthday() ),
                                          ( 'select your gender',  user.get_gender()   )]:
                if var is None or var == '' or var == []:
                    raise ValueError(f'Please {requested_action}')

            return

        except ValueError as e:
            error_message = e.args[0]
            continue
