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

from src.ui.callback_classes     import Button
from src.ui.gui_menu             import GUIMenu
from src.ui.screens.get_yes      import get_yes
from src.ui.screens.show_message import show_message

if typing.TYPE_CHECKING:
    from src.entities.user import User
    from src.ui.gui        import GUI


def delete_meal(gui: 'GUI', user: 'User') -> None:
    """Render the `Delete Meal` menu."""
    title = 'Delete Meal'

    list_of_todays_meals = user.get_todays_meals()

    if not list_of_todays_meals:
        show_message(gui, title, "No meals recorded for today.")
        return

    while True:
        menu    = GUIMenu(gui, title)
        buttons = {f'{meal.name} ({meal.eat_time})': (Button(menu, closes_menu=True), meal)
                   for meal in list_of_todays_meals}

        return_bt = Button(menu, closes_menu=True)

        menu.menu.add.label('Select meal to delete')
        menu.menu.add.label('\n')

        for name, button_meal_tup in buttons.items():
            menu.menu.add.button(name, action=button_meal_tup[0].set_pressed)

        menu.menu.add.label('\n', font_size=5)
        menu.menu.add.button('Return', action=return_bt.set_pressed)
        menu.start()

        for name, button_meal_tup in buttons.items():
            button = button_meal_tup[0]
            meal   = button_meal_tup[1]
            if button.pressed:
                if get_yes(gui, title, f'Confirm deletion of {name}', 'No'):
                    user.delete_meal(meal)
                list_of_todays_meals = user.get_todays_meals()
                if not list_of_todays_meals:
                    return

                continue

        if return_bt.pressed:
            return
