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

import pygame

from src.common.exceptions import EscPressed, KeyPress

from src.common.enums    import CalContent
from src.common.formulae import calculate_nv_goal

from src.entities.nutritional_values import NutritionalValues
from src.entities.user               import User

from src.ui.gui import GUI

if typing.TYPE_CHECKING:
    from src.database.unencrypted_database import RecipeDatabase


def align_float(float_list: list) -> list:
    """Align floats so that the decimal points are above each other."""
    float_strings  = [f"{f:.1f}"  for f in float_list]
    decimal_points = [s.find('.') for s in float_strings]

    return [' ' * (max(decimal_points) - d) + s
            for s, d in zip(float_strings, decimal_points)]


def get_meal_lines(user      : 'User',
                   recipe_db : 'RecipeDatabase'
                   ) -> tuple:
    """Get meal lines."""
    total_consumed_kcal      = 0.0
    total_consumed_carbs_g   = 0.0
    total_consumed_protein_g = 0.0
    total_consumed_fat_g     = 0.0

    lines     = [42 * ' ' + 'Daily Overview', 'Meals:']
    meal_list = user.get_todays_meals()

    # Columns
    c1, c2, c3, c4, c5, c6, c7, c8 = ([] for _ in range(8))

    if not meal_list:
        lines.append("    <n/a>")
    else:
        for meal in meal_list:
            c1.append(len(meal.eat_time) * ' ')
            c2.append(meal.eat_time)
            c3.append(meal.name)
            c4.append(meal.total_weight)
            c5.append(meal.meal_nv.protein_g)
            c6.append(meal.meal_nv.kcal)
            c7.append(meal.meal_nv.carbohydrates_g)
            c8.append(meal.meal_nv.fat_g)

            total_consumed_kcal      += meal.meal_nv.kcal
            total_consumed_carbs_g   += meal.meal_nv.carbohydrates_g
            total_consumed_protein_g += meal.meal_nv.protein_g
            total_consumed_fat_g     += meal.meal_nv.fat_g

        c4s = align_float(c4)
        c5s = align_float(c5)
        c6s = align_float(c6)
        c7s = align_float(c7)
        c8s = align_float(c8)

        c1.insert(0, '        ')
        c2.insert(0, 'Time')
        c3.insert(0, 'Meal')
        c4s.insert(0, 'Serving (g)')
        c5s.insert(0, 'Protein (g)')
        c6s.insert(0, 'Energy (kcal)')
        c7s.insert(0, 'Carbs (g)')
        c8s.insert(0, 'Fat (g)')

        # Determine column widths
        c1w, c2w, c3w, c4w, c5w, c6w, c7w, c8w \
            = [max(len(v) for v in column) for column in [c1, c2, c3, c4s, c5s, c6s, c7s, c8s]]

        recipe_names = [r[:17] for r in recipe_db.get_list_of_recipe_names()]

        c3w = max(c3w, len(max(recipe_names, key=len)))

        lines.extend([f'{f1:<{c1w}}  {f2:<{c2w}}  {f3:<{c3w}}  {f4:>{c4w}}  '
                      f'{f5:>{c5w}}  {f6:>{c6w}}  {f7:>{c7w}}  {f8:>{c8w}}'
                      for f1, f2, f3, f4, f5, f6, f7, f8 in zip(c1, c2, c3, c4s, c5s, c6s, c7s, c8s)])

    return lines, total_consumed_kcal, total_consumed_carbs_g


def get_daily_macro_lines(user                 : 'User',
                          total_burned_carbs_g : float
                          ) -> list:
    """Get daily macro lines."""
    nv_goals = calculate_nv_goal(user)

    diet_kcal_goal   = nv_goals.kcal
    diet_carb_g_goal = nv_goals.carbohydrates_g
    diet_prot_g_goal = nv_goals.protein_g
    diet_fat_g_goal  = nv_goals.fat_g

    todays_consumed_nv = NutritionalValues()
    for meal in user.get_todays_meals():
        todays_consumed_nv += meal.meal_nv

    todays_consumed_nv.apply_tef_multipliers()

    total_consumed_kcal      = todays_consumed_nv.kcal
    total_consumed_protein_g = todays_consumed_nv.protein_g
    total_consumed_carbs_g   = todays_consumed_nv.carbohydrates_g
    total_consumed_fat_g     = todays_consumed_nv.fat_g

    # Burned fat is ignored in the macro balance as the point of diet is to generally reduce fat.
    total_burned_carbs_kcal  = total_burned_carbs_g   * CalContent.KCAL_PER_GRAM_CARB.value
    kcal_goal                = diet_kcal_goal         + total_burned_carbs_kcal
    carb_goal_g              = diet_carb_g_goal       + total_burned_carbs_g

    # Columns
    c1 = ['Energy:', 'Carbs:', 'Protein:', 'Fat:']

    c2 = align_float([total_consumed_kcal,
                      total_consumed_carbs_g,
                      total_consumed_protein_g,
                      total_consumed_fat_g])

    c3 = align_float([kcal_goal,
                      carb_goal_g,
                      diet_prot_g_goal,
                      diet_fat_g_goal])

    c4 = ['kcal', 'g', 'g', 'g', 'g']

    c5 = align_float([(consumed / goal * 100.0) for consumed,
                      goal in [(total_consumed_kcal,      kcal_goal       ),
                               (total_consumed_carbs_g,   carb_goal_g     ),
                               (total_consumed_protein_g, diet_prot_g_goal),
                               (total_consumed_fat_g,     diet_fat_g_goal )] ])

    # Column widths
    c1w, c2w, c3w, c4w = [max(len(v) for v in column) for column in [c1, c2, c3, c4]]

    lines = [f'          {f1:{c1w}} {f2:{c2w}} / {f3:{c3w}} {f4:{c4w}} ({f5}% of daily goal) '
             f'{"!" if float(f5) > 100.0 else ""}'
             for f1, f2, f3, f4, f5 in zip(c1, c2, c3, c4, c5)]

    return ['', 'Macros:'] + lines


def get_calorie_balance(user: 'User') -> list:
    """Get daily calorie balance."""
    nv_goals = calculate_nv_goal(user)

    todays_consumed_nv = NutritionalValues()
    for meal in user.get_todays_meals():
        todays_consumed_nv += meal.meal_nv

    todays_consumed_nv.apply_tef_multipliers()
    consumed_kcal    = todays_consumed_nv.kcal
    consumed_carbs_g = todays_consumed_nv.carbohydrates_g
    consumed_fats_g  = todays_consumed_nv.fat_g

    bmr_kcal    = nv_goals.kcal
    bmr_carbs_g = nv_goals.carbohydrates_g
    bmr_fat_g   = nv_goals.fat_g
    bmr_total_g = bmr_carbs_g + bmr_fat_g

    total_burned_g   = bmr_total_g
    total_consumed_g = consumed_carbs_g + consumed_fats_g
    weight_change_g  = total_consumed_g - total_burned_g
    weight_change_kg = weight_change_g / 1000

    kcal_change     = consumed_kcal - bmr_kcal
    current_weight  = user.get_todays_weight()
    weight_tomorrow = current_weight + weight_change_kg

    consumed_kcal_aligned, bmd_kcal_aligned, kcal_change_aligned \
        = align_float([consumed_kcal, bmr_kcal, kcal_change])

    bmr_warning = f'! Below BMR' if consumed_kcal < bmr_kcal else ''

    consumed_carbs_g_aligned, bmr_carbs_g_aligned = align_float([consumed_carbs_g, bmr_carbs_g])
    consumed_fat_g_aligned,   bmr_fat_g_aligned   = align_float([consumed_fats_g,  bmr_fat_g  ])
    consumed_total_g_aligned, bmr_total_g_aligned = align_float([total_consumed_g, bmr_total_g])

    carb_total_change_g = consumed_carbs_g - bmr_carbs_g
    fat_total_change_g  = consumed_fats_g  - bmr_fat_g

    weight_change_dir = '+' if weight_change_g     >= 0 else ''
    carb_change_dir   = '-' if carb_total_change_g  < 0 else '+'
    fat_change_dir    = '-' if fat_total_change_g   < 0 else '+'

    # Columns
    c0 = ['', '', '']
    c1 = ['Food-TEF', 'BMR']
    c2 = ['+', '-', '-']
    c3 = [consumed_kcal_aligned, bmd_kcal_aligned]
    c4 = ['C +', 'C -', 'C -']
    c5 = [consumed_carbs_g_aligned, bmr_carbs_g_aligned]
    c6 = ['g', 'g', 'g']
    c7 = ['F +', 'F -', 'F -']
    c8 = [consumed_fat_g_aligned, bmr_fat_g_aligned]
    c9 = ['g', 'g', 'g']
    c10 = [bmr_warning, '', '']
    c11 = [consumed_total_g_aligned, bmr_total_g_aligned]

    # Column widths
    c0w, c1w, c2w, c3w, c4w, c5w, c6w, c7w, c8w, c9w \
        = [max(len(v) for v in column) for column in [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9]]

    lines = ['', 'Daily calorie balance:']

    lines += [
        f'         {f0} {f1:{c1w}} {f2:{c2w}} {f3:{c3w}} kcal'
        f'           {f2}  {f11:4}g  ({f4:{c4w}} {f5:{c5w}}{f6:{c6w}}  {f7:{c7w}} {f8:{c8w}}{f9:{c9w}}) {f10}'
        for f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11 in zip(c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11)]

    lines += [f'{19 * " " + 14 * "─" + 2 * " " + 18 * "─" + 2 * " " + 11 * "─" + 2 * " " + 11 * "─"}',
              f'                   = {kcal_change_aligned} kcal  D weight = {weight_change_dir}{weight_change_g:.1f}g'
              f'  (C {carb_change_dir} {abs(carb_total_change_g):.1f}g  F {fat_change_dir} '
              f'{abs(fat_total_change_g):.1f}g) ({current_weight}kg -> {weight_tomorrow:.1f}kg)']

    return lines


def show_daily_overview(gui       : 'GUI',
                        user      : 'User',
                        recipe_db : 'RecipeDatabase'
                        ) -> None:
    """Show the daily calorie balance overview."""
    meal_lines, total_kcal, total_carbohydrates_g = get_meal_lines(user, recipe_db)

    macro_lines   = get_daily_macro_lines(user, total_carbohydrates_g)
    cal_bal_lines = get_calorie_balance(user)

    lines = meal_lines + macro_lines + cal_bal_lines

    font_size = 13
    gui.clear_screen()

    for i, line in enumerate(lines):
        font   = pygame.font.SysFont('monospace', font_size)
        sprite = font.render(line, True, gui.color.FONT_COLOR.value)
        gui.display.blit(sprite, (0, i * 1.5 * font_size))

    gui.draw_screen()

    while True:
        try:
            gui.check_events()
            gui.tick()
        except EscPressed:
            return
        except KeyPress:
            pass
