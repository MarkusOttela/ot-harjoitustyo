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

from src.ui.callback_classes import Button
from src.ui.gui_menu         import GUIMenu

from src.ui.screens.mealprep_menu.edit_mealprep import edit_mealprep
from src.ui.screens.show_message                import show_message

if typing.TYPE_CHECKING:
    from src.database.unencrypted_database import MealprepDatabase, IngredientDatabase
    from src.ui.gui import GUI


def select_mealprep_to_edit(gui           : 'GUI',
                            mealprep_db   : 'MealprepDatabase',
                            ingredient_db : 'IngredientDatabase'
                            ) -> None:
    """Render the `Select Mealprep to Edit` menu."""
    title = 'Select Mealprep to Edit'

    while True:
        menu = GUIMenu(gui, title)

        list_of_mealpreps = mealprep_db.get_list_of_mealpreps()

        if not list_of_mealpreps:
            show_message(gui, title, 'No mealpreps yet in database.')
            return

        buttons = {mealprep.recipe_name: Button(menu, closes_menu=True)
                   for mealprep in list_of_mealpreps}

        cancel_bt = Button(menu, closes_menu=True)

        for mealprep in list_of_mealpreps:
            menu.menu.add.button(f'{str(mealprep)}',
                                 action=buttons[mealprep.recipe_name].set_pressed)
        menu.menu.add.button('Cancel', action=cancel_bt.set_pressed)

        menu.start()

        if cancel_bt.pressed:
            return

        for name, button in buttons.items():
            if button.pressed:
                edit_mealprep(gui, mealprep_db, ingredient_db, mealprep_db.get_mealprep(name))

                # If edit_mealprep deletes the last mealprep edit menu is no longer needed.
                if not mealprep_db.get_list_of_mealpreps():
                    return
