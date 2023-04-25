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

import json

from datetime import datetime
from enum     import Enum, unique

from src.common.conversion                import Conversion
from src.common.security.user_credentials import UserCredentials
from src.common.utils                     import get_today_str

from src.database.encrypted_database import EncryptedDatabase

from src.common.statics import Gender, Format

from src.diet.bmr   import calculate_bmr
from src.diet.enums import PhysicalActivityLevel, DietStage, CalContent
from src.diet.coef  import get_pal_multiplier, get_calorie_deficit_multiplier


@unique
class DBKeys(Enum):
    """JSON Database keys."""
    NAME           = 'name'
    BIRTHDAY       = 'birthday'
    GENDER         = 'gender'
    HEIGHT_CM      = 'height_cm'
    INIT_WEIGHT_KG = 'init_weight_kg'
    PAL            = 'pal'
    WEIGHT_LOG     = 'weight_log'


class User:
    """UserCredentials object manages all information about the user."""

    def __init__(self, credentials: UserCredentials) -> None:
        self.credentials = credentials
        self._name       = credentials.get_username()

        self._birthday = ''
        self._gender   = Gender.MALE

        self._height_cm      = 0
        self._init_weight_kg = 0

        self._pal        = PhysicalActivityLevel.LightlyActive
        self._diet_stage = DietStage.Diet
        self._bmr        = 0.0

        self.daily_macro_goals = dict()
        self._weight_log       = dict()

        self.database = EncryptedDatabase(self.credentials)

    def __repr__(self) -> str:
        """Format User attributes."""
        string = (f"<User-object {id(self)}>\n"
                  f"  Name:        {self._name}\n"
                  f"  Birthday:    {self._birthday}\n"
                  f"  Gender:      {self._gender.value}\n"
                  f"  Height:      {self._height_cm}\n"
                  f"  Init Weight: {self._init_weight_kg}\n"
                  f"  PAL:         {self._pal.value}\n"
                  f"  Daily goals:\n")
        for key, value in self.daily_macro_goals.items():
            string += f'    {key:8}: {value:.1f}'
            string += 'kcal\n' if key == 'Energy' else 'g\n'
        return string

    # Databases
    def serialize(self) -> bytes:
        """Serialize user's attributes into a bytestring."""
        return json.dumps({DBKeys.NAME.value           : self._name,
                           DBKeys.BIRTHDAY.value       : self._birthday,
                           DBKeys.GENDER.value         : self._gender.value,
                           DBKeys.HEIGHT_CM.value      : self._height_cm,
                           DBKeys.INIT_WEIGHT_KG.value : self._init_weight_kg,
                           DBKeys.PAL.value            : self._pal.value,
                           DBKeys.WEIGHT_LOG.value     : json.dumps(self._weight_log),
                           }).encode()

    def store_db(self) -> None:
        """Store the user's data into the database."""
        self.database.store_db(self.serialize())

    def load_db(self) -> None:
        """Load user's data"""
        serialized_data = self.database.load_db()
        json_db         = json.loads(serialized_data)

        self._name           = json_db[DBKeys.NAME.value]
        self._birthday       = json_db[DBKeys.BIRTHDAY.value]
        self._height_cm      = json_db[DBKeys.HEIGHT_CM.value]
        self._init_weight_kg = json_db[DBKeys.INIT_WEIGHT_KG.value]
        self._gender         = Gender(               json_db[DBKeys.GENDER.value])
        self._pal            = PhysicalActivityLevel(json_db[DBKeys.PAL.value])
        self._weight_log     = json.loads(json_db[DBKeys.WEIGHT_LOG.value])

    # Setters
    # -------
    def set_birthday(self, birthday: str) -> None:
        """Set the birthday of the user."""
        self._birthday = birthday
        self.store_db()

    def set_gender(self, gender: 'Gender') -> None:
        """Set gender for the user."""
        self._gender = gender
        self.store_db()

    def set_height(self, height: float) -> None:
        """Set the height of the user."""
        self._height_cm = height
        self.store_db()

    def set_init_weight(self, weight: float) -> None:
        """Set the initial weight of the user."""
        self._init_weight_kg = weight
        self.store_db()

    def set_pal(self, pal: 'PhysicalActivityLevel') -> None:
        """Set the Physical Activity Level (PAL) for the user."""
        self._pal = pal
        self.store_db()

    def set_diet_stage(self, diet_stage: 'DietStage') -> None:
        """Set the Physical Activity Level (PAL) for the user."""
        self._diet_stage = diet_stage
        self.store_db()

    def set_todays_weight(self, weight_kg: float) -> None:
        """Set the day's weight."""
        self._weight_log[get_today_str()] = weight_kg
        self.store_db()

    # Dynamically generated values
    def calculate_bmr(self, weight_kg: float) -> None:
        """Calculate the user's basal metabolic rate."""
        self._bmr = calculate_bmr(self._gender, weight_kg, self._height_cm, self.get_age())

    def calculate_daily_macros(self) -> None:
        """Calculate the daily macro goals for the user.

        Protein goal: avg. form https://youtu.be/l7jIU_73ZaM?t=403
        """
        self.calculate_bmr(self.get_todays_weight())

        theoretical_maintenance_kcal = get_pal_multiplier(self._pal) * self._bmr
        calorie_deficit_multiplier   = get_calorie_deficit_multiplier(self._diet_stage)

        kcal_goal = calorie_deficit_multiplier * theoretical_maintenance_kcal

        protein_goal_g    = 1.9  * self.get_todays_weight()
        protein_goal_kcal = protein_goal_g * CalContent.KCAL_PER_GRAM_PROTEIN.value
        fat_goal_kcal     = 0.25 * kcal_goal
        fat_goal_g        = fat_goal_kcal / CalContent.KCAL_PER_GRAM_FAT.value
        carbs_goal_kcal   = (kcal_goal - protein_goal_kcal - fat_goal_kcal)
        carbs_goal_g      = carbs_goal_kcal / CalContent.KCAL_PER_GRAM_CARB.value

        self.daily_macro_goals = {'Energy'  : kcal_goal,
                                  'Carbs'   : carbs_goal_g,
                                  'Fat'     : fat_goal_g,
                                  'Protein' : protein_goal_g}

    # Getters
    # -------
    def get_gender(self) -> 'Gender':
        """Get the user's gender."""
        return self._gender

    def get_birthday(self) -> str:
        """Get the user's birthday."""
        return self._birthday

    def get_age(self) -> float:
        """Return the current age of the user in years."""
        dt_birthday = datetime.strptime(self._birthday, Format.DATETIME_DATE.value)
        age_in_years = ((datetime.today() - dt_birthday).days / Conversion.DAYS_PER_YEAR.value)
        return age_in_years

    def get_height(self) -> float:
        """Get the user's height in centimeters."""
        return self._height_cm

    def get_todays_weight(self) -> float:
        """Get today's weight."""
        return self._weight_log[get_today_str()]

    def get_initial_weight(self) -> float:
        """Get the user's initial weight in kilograms."""
        return self._init_weight_kg

    def get_pal(self) -> 'PhysicalActivityLevel':
        """Get the user's Physical Activity Level (PAL)."""
        return self._pal

    def get_bmr(self) -> float:
        """Get the user's Basal Metabolic Rate (kcal/day)."""
        return self._bmr

    # Has'ers
    # -------
    def has_weight_entry_for_the_day(self) -> bool:
        """Return True if the daily weight entry has been recorded."""
        return get_today_str() in self._weight_log.keys()
