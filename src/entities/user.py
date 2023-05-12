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

from src.common.conversion import Conversion
from src.common.enums      import Gender, Format, PhysicalActivityLevel, DietStage, DBKeys
from src.common.utils      import get_today_str

from src.database.encrypted_database import EncryptedDatabase
from src.entities.user_credentials   import UserCredentials

from src.entities.meal import Meal


class User:  # pylint: disable=too-many-instance-attributes, too-many-public-methods
    """UserCredentials object manages all information about the user.

    Note: The `pylint: disable=` suppressions here are because User is more
          or less a data-class that holds all data for the user.
    """

    def __init__(self,
                 credentials : UserCredentials,
                 dob         : str,
                 gender      : 'Gender',
                 init_weight : float,
                 height      : float,
                 pal         : 'PhysicalActivityLevel',
                 diet_stage  : 'DietStage'
                 ) -> None:
        self.credentials = credentials
        self.name        = credentials.get_username()

        self.birthday = dob
        self.gender   = gender

        self.height_cm      = height
        self.init_weight_kg = init_weight

        self.pal        = pal
        self.diet_stage = diet_stage
        self.bmr        = 0.0

        self.daily_macro_goals : dict = {}
        self.weight_log        : dict = {}
        self.meal_log          : dict = {}

        self.database = EncryptedDatabase(self.credentials)

    def __repr__(self) -> str:
        """Format User attributes."""
        string = (f"<User-object {id(self)}>\n"
                  f"  Name:         {self.name}\n"
                  f"  Birthday:     {self.birthday}\n"
                  f"  Gender:       {self.gender.value}\n"
                  f"  Height:       {self.height_cm}\n"
                  f"  Init Weight:  {self.init_weight_kg}\n"
                  f"  Curr. Weight: {self.get_todays_weight()}\n"
                  f"  PAL:          {self.pal.value}\n"
                  f"  Daily goals:\n")
        for key, value in self.daily_macro_goals.items():
            string += f'    {key:8}: {value:.1f}'
            string += 'kcal\n' if key == 'Energy' else 'g\n'
        return string

    # Databases
    def serialize(self) -> bytes:
        """Serialize user's attributes into a bytestring."""
        return json.dumps({DBKeys.NAME.value:           self.name,
                           DBKeys.BIRTHDAY.value:       self.birthday,
                           DBKeys.GENDER.value:         self.gender.value,
                           DBKeys.HEIGHT_CM.value:      self.height_cm,
                           DBKeys.INIT_WEIGHT_KG.value: self.init_weight_kg,
                           DBKeys.PAL.value:            self.pal.value,
                           DBKeys.DIET_STAGE.value:     self.diet_stage.value,
                           DBKeys.WEIGHT_LOG.value:     json.dumps(self.weight_log),
                           DBKeys.MEAL_LOG.value:       json.dumps(self.meal_log),
                           }).encode()

    def store_db(self) -> None:
        """Store the user's data into the database."""
        self.database.store_db(self.serialize())

    @classmethod
    def from_database(cls, credentials: UserCredentials) -> 'User':
        """Load user's private data from their encrypted database."""
        serialized_data = EncryptedDatabase(credentials).load_db()
        json_db         = json.loads(serialized_data)

        name        = json_db[DBKeys.NAME.value]
        dob         = json_db[DBKeys.BIRTHDAY.value]
        height      = json_db[DBKeys.HEIGHT_CM.value]
        init_weight = json_db[DBKeys.INIT_WEIGHT_KG.value]

        gender     = Gender(json_db[DBKeys.GENDER.value])
        pal        = PhysicalActivityLevel(json_db[DBKeys.PAL.value])
        diet_stage = DietStage(json_db[DBKeys.DIET_STAGE.value])
        weight_log = json.loads(json_db[DBKeys.WEIGHT_LOG.value])
        meal_log   = json.loads(json_db[DBKeys.MEAL_LOG.value])

        user = User(credentials,
                    dob,
                    gender,
                    init_weight,
                    height,
                    pal,
                    diet_stage)

        user.name       = name
        user.weight_log = weight_log
        user.meal_log   = meal_log

        return user

    # Setters
    # -------

    def set_morning_weight(self, weight_kg: float) -> None:
        """Set the morning weight for the day."""
        self.weight_log[get_today_str()] = weight_kg
        self.store_db()

    def add_meal(self, meal: 'Meal') -> None:
        """Add meal to the meal log."""
        if not get_today_str() in self.meal_log.keys():
            self.meal_log[get_today_str()] = []
        self.meal_log[get_today_str()].append(meal.serialize())
        self.store_db()

    def delete_meal(self, meal_to_delete: 'Meal') -> None:
        """Delete meal from the meal log."""
        if not get_today_str() in self.meal_log.keys():
            return
        self.meal_log[get_today_str()].remove(meal_to_delete.serialize())
        self.store_db()

    # Getters
    # -------

    def get_todays_meals(self) -> list:
        """Return the list of meals for the day."""
        try:
            return [Meal.from_serialized_string(s) for s in self.meal_log[get_today_str()]]
        except KeyError:
            return []

    def get_todays_weight(self) -> float:
        """Get today's weight."""
        return self.weight_log[get_today_str()]

    def get_age(self) -> float:
        """Return the current age of the user in years."""
        dt_birthday  = datetime.strptime(self.birthday, Format.DATETIME_DATE.value)
        age_in_years = (datetime.today() - dt_birthday).days / Conversion.DAYS_PER_YEAR.value
        return age_in_years

    def get_weight_log(self) -> dict:
        """Get the user's weight log."""
        return self.weight_log

    # Has'ers
    # -------
    def has_weight_entry_for_the_day(self) -> bool:
        """Return True if the daily weight entry has been recorded."""
        return get_today_str() in self.weight_log.keys()
