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
from src.common.statics    import FontSize

from src.diet.enums import PhysicalActivityLevel

from src.ui.gui_menu                 import GUIMenu
from src.ui.screens.callback_classes import DropSelection, Button

if typing.TYPE_CHECKING:
    from src.entities.user import User
    from src.ui.gui        import GUI


def start_diet_survey(gui: 'GUI', user: 'User') -> None:
    """Start initial diet survey."""
    options   = [(member.value, member) for member in PhysicalActivityLevel]
    selection = DropSelection()

    error_message = ''
    while True:
        menu      = GUIMenu(gui, 'Initial Diet Survey')
        return_bt = Button(menu, closes_menu=True)

        try:
            menu.menu.add.dropselect(f'Non-exercise PAL: ',
                                     onchange=selection.set_value,
                                     items=options,
                                     selection_box_height=len(options),
                                     selection_option_font_size=FontSize.FONT_SIZE_SMALL.value,
                                     selection_box_width=300)
            menu.menu.add.button('Done', action=menu.menu.disable)

            menu.menu.add.label(f'')
            menu.menu.add.button('Cancel', return_bt.set_pressed)

            menu.show_error_message(error_message)
            menu.start()

            if return_bt.pressed:
                raise AbortMenuOperation

            if selection.value is None:
                raise ValueError("Please select an option from the drop menu.")

            user.set_pal(selection.value)
            return

        except ValueError as e:
            error_message = e.args[0]
            continue
