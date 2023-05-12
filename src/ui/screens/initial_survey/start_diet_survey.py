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

from src.common.exceptions import AbortMenuOperation
from src.common.enums      import FontSize, PhysicalActivityLevel, DietType

from src.ui.gui_menu         import GUIMenu
from src.ui.callback_classes import DropSelection, Button

if typing.TYPE_CHECKING:
    from src.ui.gui import GUI


def start_diet_survey(gui: 'GUI') -> tuple:
    """Start initial diet survey."""
    pal_options        = [(member.value, member) for member in PhysicalActivityLevel]
    diet_type_options = [(member.value, member) for member in DietType]

    pal_ds        = DropSelection()
    diet_type_ds = DropSelection()

    error_message = ''
    while True:
        menu      = GUIMenu(gui, 'Initial Diet Survey')
        return_bt = Button(menu, closes_menu=True)

        try:
            default_pal = None
            for i, tup in enumerate(pal_options):
                if tup[1] == pal_ds.value:
                    default_pal = i
                    break

            default_ds = None
            for i, tup in enumerate(diet_type_options):
                if tup[1] == diet_type_ds.value:
                    default_ds = i
                    break

            menu.menu.add.dropselect(f'Non-exercise PAL: ',
                                     onchange=pal_ds.set_value,
                                     items=pal_options,  # type: ignore
                                     selection_box_height=len(pal_options),
                                     selection_option_font_size=FontSize.FONT_SIZE_SMALL.value,
                                     selection_box_width=300,
                                     default=default_pal,
                                     **gui.drop_selection_theme)

            menu.menu.add.dropselect(f'Diet Type: ',
                                     onchange=diet_type_ds.set_value,
                                     items=diet_type_options,  # type: ignore
                                     selection_box_height=len(diet_type_options),
                                     selection_option_font_size=FontSize.FONT_SIZE_SMALL.value,
                                     selection_box_width=300,
                                     default=default_ds,
                                     **gui.drop_selection_theme)

            menu.menu.add.button('Done', action=menu.menu.disable)

            menu.menu.add.label(f'')
            menu.menu.add.button('Cancel', return_bt.set_pressed)

            menu.show_error_message(error_message)
            menu.start()

            if return_bt.pressed:
                raise AbortMenuOperation

            if not pal_ds.value or not diet_type_ds.value:
                raise ValueError("Please select one option from each drop-down menu.")

            return pal_ds.value, diet_type_ds.value

        except ValueError as e:
            error_message = e.args[0]
            continue
