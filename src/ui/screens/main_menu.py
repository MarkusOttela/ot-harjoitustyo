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

import sys
import typing

from src.common.exceptions           import AbortMenuOperation
from src.common.statics              import Program
from src.common.utils                import get_list_of_user_account_names
from src.ui.gui_menu                 import GUIMenu
from src.ui.screens.callback_classes import Button

from src.ui.screens.ingredient_menu.manage_ingredients import manage_ingredients_menu
from src.ui.screens.login.create_new_user              import create_new_user
from src.ui.screens.login.login_existing_user          import login_existing_user

if typing.TYPE_CHECKING:
    from src.ui.gui                       import GUI
    from src.database.ingredient_database import IngredientDatabase


def main_menu(gui           : 'GUI',
              ingredient_db : 'IngredientDatabase'
              ) -> None:
    """Render the Main Menu."""
    while True:
        try:
            menu = GUIMenu(gui, Program.NAME.value)

            create_user_bt     = Button(menu, closes_menu=True)
            login_bt           = Button(menu, closes_menu=True)
            ingredient_menu_bt = Button(menu, closes_menu=True)
            exit_bt            = Button(menu, closes_menu=True)

            menu.menu.add.button('Create New User', action=create_user_bt.set_pressed)
            if get_list_of_user_account_names():
                menu.menu.add.button('Login Existing User', action=login_bt.set_pressed)
            menu.menu.add.button('Manage Ingredients', action=ingredient_menu_bt.set_pressed)
            menu.menu.add.button('Exit',               action=exit_bt.set_pressed)

            menu.start()

            if ingredient_menu_bt.pressed:
                manage_ingredients_menu(gui, ingredient_db)
                continue

            if create_user_bt.pressed:
                user = create_new_user(gui)
                print(f"Created {repr(user)}")

            if login_bt.pressed:
                user = login_existing_user(gui)
                print(f"Logged in {repr(user)}")

            if exit_bt.pressed:
                sys.exit()

        except AbortMenuOperation:
            continue
