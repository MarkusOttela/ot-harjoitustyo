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

from src.common.enums      import ColorScheme
from src.common.exceptions import ReturnToMainMenu
from src.common.validation import floats, validate_positive_float

from src.ui.callback_classes import Button, StringInput
from src.ui.gui_menu         import GUIMenu

if typing.TYPE_CHECKING:
    from src.ui.gui import GUI


def get_body_measurements(gui: 'GUI') -> tuple:
    """Get initial body measurements (weight and height) from the user."""
    title         = 'Initial Diet Survey'
    error_message = ''

    weight = StringInput()
    height = StringInput()

    while True:
        menu      = GUIMenu(gui, title)
        done_bt   = Button(menu, closes_menu=True)
        return_bt = Button(menu, closes_menu=True)

        try:
            if weight.value is not None:
                try:
                    default_weight = str(validate_positive_float(weight.value))
                except ValueError:
                    default_weight = ''
            else:
                default_weight = ''

            if height.value is not None:
                try:
                    default_height = str(validate_positive_float(height.value))
                except ValueError:
                    default_height = ''
            else:
                default_height = ''

            menu.menu.add.text_input('Your height (cm) : ',
                                     onchange=height.set_value,
                                     default=default_height,
                                     valid_chars=floats,
                                     maxchar=5,
                                     font_color=ColorScheme.FONT_COLOR.value)

            menu.menu.add.text_input('Your weight (kg) : ',
                                     onchange=weight.set_value,
                                     default=default_weight,
                                     valid_chars=floats,
                                     maxchar=5,
                                     font_color=ColorScheme.FONT_COLOR.value)

            menu.menu.add.button('Done', done_bt.set_pressed)
            menu.menu.add.label('')
            menu.menu.add.button('Cancel', return_bt.set_pressed)

            menu.show_error_message(error_message)
            menu.start()

            if return_bt.pressed:
                raise ReturnToMainMenu

            if done_bt.pressed:

                if height.value == '':
                    raise ValueError("Please enter your height")
                height_f = validate_positive_float(height.value)

                # Tallest and shortest adults who ever lived as limits.
                if height_f > 272.0 or height_f < 54.6:
                    raise ValueError("Please enter a valid height.")

                if weight.value == '':
                    raise ValueError("Please enter your current weight")
                weight_f = validate_positive_float(weight.value)

                bmi = weight_f / ((height_f / 100) ** 2)

                if bmi > 40:
                    raise ValueError(
                        f"Invalid weight (BMI of value {bmi:.1f} is dangerously high!)")
                elif bmi < 16:
                    raise ValueError(
                        f"Invalid weight (BMI of value {bmi:.1f} is dangerously low!)")

                return weight_f, height_f

        except ValueError as e:
            error_message = e.args[0]
            continue
