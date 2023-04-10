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

from src.common.statics               import Program
from src.database.ingredient_database import IngredientDatabase
from src.gui.gui                      import GUI
from src.gui.screens.main_menu        import main_menu


def main() -> None:
    """Calorinator - Diet tracker

    The program supports the user in maintaining their diet by
        1. Tracking their meals, and by counting the nutritional values of each meal
        2. Informing them about the daily consumption in relation to their goal values
        3. Creating statistics about food and nutrient consumption, and progress of the diet
    """
    print(f'{Program.NAME.value} {Program.VERSION.value}\n')

    gui           = GUI()
    ingredient_db = IngredientDatabase()

    main_menu(gui, ingredient_db)


if __name__ == '__main__':
    main()
