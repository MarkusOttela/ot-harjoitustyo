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
from src.common.statics                   import Gender, Format
from src.common.utils                     import get_today_str

from src.database.encrypted_database import EncryptedDatabase

from src.diet.enums import PhysicalActivityLevel, DietStage
from src.diet.meal  import Meal


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
    MEAL_LOG       = 'meal_log'


class User:  # pylint: disable=too-many-instance-attributes, too-many-public-methods
    """UserCredentials object manages all information about the user.

    Note: The `pylint: disable=` suppressions here are because User is more
          or less a data-class that holds all data for the user.
    """

    def __init__(self, credentials: UserCredentials) -> None:
        self.credentials = credentials
        self._name       = credentials.get_username()

        self._birthday = ''
        self._gender   = Gender.MALE

        self._height_cm      = 0.0
        self._init_weight_kg = 0.0

        self._pal        = PhysicalActivityLevel.LIGHTLY_ACTIVE
        self._diet_stage = DietStage.DIET
        self._bmr        = 0.0

        self.daily_macro_goals : dict = {}
        self._weight_log       : dict = {}
        self._meal_log         : dict = {}

        self.database = EncryptedDatabase(self.credentials)

    def __repr__(self) -> str:
        """Format User attributes."""
        string = (f"<User-object {id(self)}>\n"
                  f"  Name:         {self._name}\n"
                  f"  Birthday:     {self._birthday}\n"
                  f"  Gender:       {self._gender.value}\n"
                  f"  Height:       {self._height_cm}\n"
                  f"  Init Weight:  {self._init_weight_kg}\n"
                  f"  Curr. Weight: {self.get_todays_weight()}\n"
                  f"  PAL:          {self._pal.value}\n"
                  f"  Daily goals:\n")
        for key, value in self.daily_macro_goals.items():
            string += f'    {key:8}: {value:.1f}'
            string += 'kcal\n' if key == 'Energy' else 'g\n'
        return string

    # Databases
    def serialize(self) -> bytes:
        """Serialize user's attributes into a bytestring."""
        return json.dumps({DBKeys.NAME.value:           self._name,
                           DBKeys.BIRTHDAY.value:       self._birthday,
                           DBKeys.GENDER.value:         self._gender.value,
                           DBKeys.HEIGHT_CM.value:      self._height_cm,
                           DBKeys.INIT_WEIGHT_KG.value: self._init_weight_kg,
                           DBKeys.PAL.value:            self._pal.value,
                           DBKeys.WEIGHT_LOG.value:     json.dumps(self._weight_log),
                           DBKeys.MEAL_LOG.value:       json.dumps(self._meal_log),
                           }).encode()

    def store_db(self) -> None:
        """Store the user's data into the database."""
        self.database.store_db(self.serialize())

    def load_db(self) -> None:
        """Load user's private data from their encrypted database."""
        serialized_data = self.database.load_db()
        json_db         = json.loads(serialized_data)

        self._name           = json_db[DBKeys.NAME.value]
        self._birthday       = json_db[DBKeys.BIRTHDAY.value]
        self._height_cm      = json_db[DBKeys.HEIGHT_CM.value]
        self._init_weight_kg = json_db[DBKeys.INIT_WEIGHT_KG.value]

        self._gender         = Gender(json_db[DBKeys.GENDER.value])
        self._pal            = PhysicalActivityLevel(json_db[DBKeys.PAL.value])
        self._weight_log     = json.loads(json_db[DBKeys.WEIGHT_LOG.value])
        self._meal_log       = json.loads(json_db[DBKeys.MEAL_LOG.value])

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

    def set_morning_weight(self, weight_kg: float) -> None:
        """Set the morning weight for the day."""
        self._weight_log[get_today_str()] = weight_kg
        self.store_db()

    def add_meal(self, meal: 'Meal') -> None:
        """Add meal to the meal log."""
        if not get_today_str() in self._meal_log.keys():
            self._meal_log[get_today_str()] = []
        self._meal_log[get_today_str()].append(meal.serialize())
        self.store_db()

    def delete_meal(self, meal_to_delete: 'Meal') -> None:
        """Delete meal from the meal log."""
        if not get_today_str() in self._meal_log.keys():
            return
        self._meal_log[get_today_str()].remove(meal_to_delete.serialize())
        self.store_db()

    # Getters
    # -------

    def get_todays_meals(self) -> list:
        """Return the list of meals for the day."""
        try:
            return [Meal.from_serialized_string(s) for s in self._meal_log[get_today_str()]]
        except KeyError:
            return []

    def get_todays_weight(self) -> float:
        """Get today's weight."""
        return self._weight_log[get_today_str()]

    def get_username(self) -> str:
        """Get the user's username."""
        return self.credentials.get_username()

    def get_gender(self) -> 'Gender':
        """Get the user's gender."""
        return self._gender

    def get_birthday(self) -> str:
        """Get the user's birthday."""
        return self._birthday

    def get_age(self) -> float:
        """Return the current age of the user in years."""
        dt_birthday  = datetime.strptime(self._birthday, Format.DATETIME_DATE.value)
        age_in_years = (datetime.today() - dt_birthday).days / Conversion.DAYS_PER_YEAR.value
        return age_in_years

    def get_height(self) -> float:
        """Get the user's height in centimeters."""
        return self._height_cm

    def get_initial_weight(self) -> float:
        """Get the user's initial weight in kilograms."""
        return self._init_weight_kg

    def get_diet_stage(self) -> 'DietStage':
        """Get the diet stage of the user."""
        return self._diet_stage

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
