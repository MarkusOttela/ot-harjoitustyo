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

from src.common.exceptions import AbortMenuOperation
from src.common.statics    import Program
from src.common.utils      import get_list_of_user_account_names

from src.ui.gui_menu         import GUIMenu
from src.ui.callback_classes import Button

from src.ui.screens.get_morning_weight                   import get_morning_weight
from src.ui.screens.ingredient_menu.manage_ingredients   import manage_ingredients_menu
from src.ui.screens.initial_survey.get_body_measurements import get_body_measurements
from src.ui.screens.initial_survey.initial_survey        import get_dob_and_gender
from src.ui.screens.initial_survey.start_diet_survey     import start_diet_survey
from src.ui.screens.log_meal.select_meal_to_log          import select_meal_to_log
from src.ui.screens.login.create_new_user                import create_new_user
from src.ui.screens.login.login_existing_user            import login_existing_user
from src.ui.screens.meal_menu.delete_meal                import delete_meal
from src.ui.screens.mealprep_menu.manage_mealpreps       import manage_mealpreps_menu
from src.ui.screens.recipe_menu.manage_recipes           import manage_recipes_menu
from src.ui.screens.statistics.daily_overview            import show_daily_overview

if typing.TYPE_CHECKING:
    from src.database.unencrypted_database import IngredientDatabase, MealprepDatabase, RecipeDatabase
    from src.ui.gui import GUI


def main_menu(gui           : 'GUI',
              ingredient_db : 'IngredientDatabase',
              recipe_db     : 'RecipeDatabase',
              mealprep_db   : 'MealprepDatabase'
              ) -> None:
    """Render the Main Menu."""
    user = None

    while True:
        try:
            menu = GUIMenu(gui, Program.NAME.value)

            create_user_bt     = Button(menu, closes_menu=True)
            login_bt           = Button(menu, closes_menu=True)

            log_meal_bt        = Button(menu, closes_menu=True)
            daily_overview_bt  = Button(menu, closes_menu=True)

            delete_meals       = Button(menu, closes_menu=True)
            mealprep_menu_bt   = Button(menu, closes_menu=True)
            recipe_menu_bt     = Button(menu, closes_menu=True)
            ingredient_menu_bt = Button(menu, closes_menu=True)

            logout_bt          = Button(menu, closes_menu=True)
            exit_bt            = Button(menu, closes_menu=True)

            if user is None:
                if get_list_of_user_account_names():
                    menu.menu.add.button('Login Existing User', action=login_bt.set_pressed)
                menu.menu.add.button('Create New User',         action=create_user_bt.set_pressed)

            if user is not None:
                menu.menu.add.label('\n')
                menu.menu.add.label(f'Welcome back {user.get_username()}')
                menu.menu.add.label('\n')
                menu.menu.add.button('Log Meal',       action=log_meal_bt.set_pressed)
                menu.menu.add.button('Daily Overview', action=daily_overview_bt.set_pressed)

            menu.menu.add.label('')
            if user is not None:
                menu.menu.add.button('Delete Meal(s)', action=delete_meals.set_pressed)
            menu.menu.add.button('Manage Mealpreps',   action=mealprep_menu_bt.set_pressed)
            menu.menu.add.button('Manage Recipes',     action=recipe_menu_bt.set_pressed)
            menu.menu.add.button('Manage Ingredients', action=ingredient_menu_bt.set_pressed)
            menu.menu.add.label('')

            if user is not None:
                menu.menu.add.button('Logout', action=logout_bt.set_pressed)

            menu.menu.add.button('Exit', action=exit_bt.set_pressed)

            menu.start()

            # ---

            if create_user_bt.pressed:
                user = create_new_user(gui)
                get_dob_and_gender(gui, user)
                get_body_measurements(gui, user)
                start_diet_survey(gui, user)
                user.calculate_daily_macros()

            if login_bt.pressed:
                user = login_existing_user(gui)
                user.load_db()

                if not user.has_weight_entry_for_the_day():
                    get_morning_weight(gui, user)
                user.calculate_daily_macros()

            # ---

            if log_meal_bt.pressed and user is not None:
                select_meal_to_log(gui, user, mealprep_db, recipe_db, ingredient_db)

            if daily_overview_bt.pressed and user is not None:
                show_daily_overview(gui, user, recipe_db)

            # ---

            if delete_meals.pressed and user is not None:
                delete_meal(gui, user)
                continue

            if mealprep_menu_bt.pressed:
                manage_mealpreps_menu(gui, mealprep_db, recipe_db, ingredient_db)
                continue

            if recipe_menu_bt.pressed:
                manage_recipes_menu(gui, user, recipe_db, ingredient_db)
                continue

            if ingredient_menu_bt.pressed:
                manage_ingredients_menu(gui, ingredient_db)
                continue

            # ---

            if logout_bt.pressed:
                user = None
                continue

            if exit_bt.pressed:
                sys.exit()

        except AbortMenuOperation:
            continue
