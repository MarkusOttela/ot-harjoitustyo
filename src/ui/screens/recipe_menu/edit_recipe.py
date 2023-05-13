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

from src.common.enums      import Color, ColorScheme, FontSize
from src.common.validation import strings

from src.entities.recipe import Recipe

from src.ui.gui_menu         import GUIMenu
from src.ui.callback_classes import Button, MultiSelection, StringInput

from src.ui.screens.get_yes      import get_yes
from src.ui.screens.show_message import show_message

if typing.TYPE_CHECKING:
    from src.database.unencrypted_database import IngredientDatabase, RecipeDatabase
    from src.ui.gui import GUI


def edit_recipe(gui           : 'GUI',
                orig_recipe   : Recipe,
                recipe_db     : 'RecipeDatabase',
                ingredient_db : 'IngredientDatabase',
                ) -> None:
    """Render the `Edit Recipe` menu."""
    title         = 'Edit Recipe'
    error_message = ''

    available_ingredients = [(ingredient.name, ingredient)
                             for ingredient in ingredient_db.get_list_of_ingredients()]

    name = StringInput()
    name.set_value(orig_recipe.name)

    author = StringInput()
    author.set_value(orig_recipe.author)

    selected_ingredients    = MultiSelection()
    selected_accompaniments = MultiSelection()

    selected_ingredients.sel_list    = orig_recipe.ingredient_names
    selected_accompaniments.sel_list = orig_recipe.accompaniment_names

    # Find indexes of previously selected ingredients
    if not orig_recipe.ingredient_names:
        selected_ingredient_indexes = None
    else:
        selected_ingredient_indexes = []

        for i, tuple_ in enumerate(available_ingredients):
            ing_name, ingredient = tuple_
            if ing_name in selected_ingredients.sel_list:
                selected_ingredient_indexes.append(i)

    # Find indexes of previously selected accompaniments
    if not orig_recipe.accompaniment_names:
        selected_accompaniment_indexes = None
    else:
        selected_accompaniment_indexes = []

        for i, tuple_ in enumerate(available_ingredients):
            ing_name, ingredient = tuple_
            if ing_name in selected_accompaniments.sel_list:
                selected_accompaniment_indexes.append(i)

    while True:
        try:
            menu = GUIMenu(gui, title)

            done_bt   = Button(menu, closes_menu=True)
            delete_bt = Button(menu, closes_menu=True)
            return_bt = Button(menu, closes_menu=True)

            menu.menu.add.text_input(f'Name: ',
                                     onchange=name.set_value,
                                     default=name.value,
                                     valid_chars=strings,
                                     maxchar=19,
                                     font_color=ColorScheme.FONT_COLOR.value)

            menu.menu.add.text_input(f'Author: ',
                                     onchange=author.set_value,
                                     default=author.value,
                                     valid_chars=strings,
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

            if orig_recipe.is_mealprep:
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
            menu.menu.add.button('Done', action=done_bt.set_pressed)

            menu.menu.add.button('Delete',
                                 action=delete_bt.set_pressed,
                                 font_color=Color.RED.value)

            menu.menu.add.button('Return', action=return_bt.set_pressed)

            menu.show_error_message(error_message)
            menu.start()

            if return_bt.pressed:
                return

            if delete_bt.pressed:
                if get_yes(gui, title, f"Delete {str(orig_recipe)}?", 'No'):
                    recipe_db.remove_recipe(orig_recipe)
                    show_message(gui, title, 'Recipe has been deleted.')
                    return

            if done_bt.pressed:
                if name.value == '':
                    raise ValueError(f'Please a name for the recipe')

                new_recipe = Recipe(name.value, author.value,
                                    selected_ingredients.values,
                                    selected_accompaniments.values,
                                    orig_recipe.is_mealprep)

                recipe_id_changed = new_recipe != orig_recipe

                if not recipe_id_changed:
                    recipe_db.replace_recipe(new_recipe)
                    show_message(gui, title, 'Recipe has been updated.')
                    return

                if not recipe_db.has_recipe(new_recipe):
                    recipe_db.remove_recipe(orig_recipe)
                    recipe_db.insert_recipe(new_recipe)
                    show_message(gui, title, 'Recipe has been renamed and updated.')
                    return

                if get_yes(gui, title,
                           f'Another recipe {str(new_recipe)} already exists. Overwrite(?)',
                           default_str='No'):
                    recipe_db.remove_recipe(orig_recipe)
                    recipe_db.replace_recipe(new_recipe)
                    show_message(gui, title, 'Recipe has been replaced.')
                    return

        except ValueError as e:
            error_message = e.args[0]
            continue
