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

from typing import Optional

from src.common.enums      import ColorScheme, FontSize
from src.common.exceptions import AbortMenuOperation

from src.entities.recipe import Recipe
from src.entities.user   import User

from src.ui.gui_menu         import GUIMenu
from src.ui.callback_classes import Button, StringInput, MultiSelection

from src.ui.screens.get_yes      import get_yes
from src.ui.screens.show_message import show_message

if typing.TYPE_CHECKING:
    from src.database.unencrypted_database import IngredientDatabase, RecipeDatabase
    from src.ui.gui import GUI


def add_mealprep_recipe(gui           : 'GUI',
                        user          : Optional['User'],
                        recipe_db     : 'RecipeDatabase',
                        ingredient_db : 'IngredientDatabase'
                        ) -> None:
    """Render the `Add Mealprep Recipe` menu."""
    title         = 'Add Mealprep Recipe'
    error_message = ''

    available_ingredients = [(ingredient.name, ingredient)
                             for ingredient in ingredient_db.get_list_of_ingredients()]

    name   = StringInput()
    author = StringInput()

    selected_ingredients    = MultiSelection()
    selected_accompaniments = MultiSelection()

    selected_ingredients.sel_list    = []
    selected_accompaniments.sel_list = []

    if user is not None:
        author.set_value(user.name)

    while True:

        try:
            # Find indexes of previously selected ingredients
            selected_ingredient_indexes = []
            for i, tuple_ in enumerate(available_ingredients):
                ing_name, ingredient = tuple_
                if ingredient in selected_ingredients.sel_list:
                    selected_ingredient_indexes.append(i)

            # Find indexes of previously selected accompaniments
            selected_accompaniment_indexes = []
            for i, tuple_ in enumerate(available_ingredients):
                ing_name, ingredient = tuple_
                if ingredient in selected_accompaniments.sel_list:
                    selected_accompaniment_indexes.append(i)

            menu          = GUIMenu(gui, title)
            return_button = Button(menu, closes_menu=True)
            done_button   = Button(menu, closes_menu=True)

            menu.menu.add.text_input(f'Name: ',
                                     onchange=name.set_value,
                                     default=name.value,
                                     maxchar=19,
                                     font_color=ColorScheme.FONT_COLOR.value)

            menu.menu.add.text_input(f'Author: ',
                                     onchange=author.set_value,
                                     default=author.value,
                                     maxchar=19,
                                     font_color=ColorScheme.FONT_COLOR.value)

            menu.menu.add.dropselect_multiple(f'Select ingredients: ',
                                              onchange=selected_ingredients.set_value,
                                              onreturn=selected_ingredients.set_value,
                                              items=available_ingredients,  # type: ignore
                                              default=selected_ingredient_indexes,
                                              selection_box_height=len(available_ingredients),
                                              selection_option_font_size=FontSize.FONT_SIZE_XSMALL.value,
                                              **gui.drop_multi_selection_theme
                                              )

            menu.menu.add.dropselect_multiple(f'Select accompaniments: ',
                                              onchange=selected_accompaniments.set_value,
                                              onreturn=selected_accompaniments.set_value,
                                              items=available_ingredients,  # type: ignore
                                              default=selected_accompaniment_indexes,
                                              selection_box_height=len(available_ingredients),
                                              selection_option_font_size=FontSize.FONT_SIZE_XSMALL.value,
                                              **gui.drop_multi_selection_theme
                                              )

            menu.menu.add.label('\n', font_size=5)
            menu.menu.add.button('Done',   action=done_button.set_pressed)
            menu.menu.add.button('Return', action=return_button.set_pressed)

            menu.show_error_message(error_message)
            menu.start()

            if return_button.pressed:
                return

            if done_button.pressed:

                if name.value == '':
                    raise ValueError("Please enter a name for the recipe")

                if not selected_ingredients.values:
                    raise ValueError("Please select at least one mealprep ingredient")

                new_recipe = Recipe(name.value, author.value,
                                    selected_ingredients.values,
                                    selected_accompaniments.values,
                                    is_mealprep=True)

                if not recipe_db.has_recipe(new_recipe):
                    recipe_db.insert_recipe(new_recipe)
                    show_message(gui, title, 'Recipe has been added.')
                    raise AbortMenuOperation("Recipe added.")

                if get_yes(gui, title,
                           f'Recipe {str(new_recipe)} already exists. Overwrite(?)',
                           default_str='No'):
                    recipe_db.replace_recipe(new_recipe)
                    show_message(gui, title, 'Recipe has been replaced')
                    raise AbortMenuOperation("Recipe replaced.")

        except ValueError as e:
            error_message = e.args[0]
            continue
