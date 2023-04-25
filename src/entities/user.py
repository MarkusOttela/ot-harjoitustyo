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

from enum import Enum, unique

from src.common.security.user_credentials import UserCredentials
from src.database.encrypted_database      import EncryptedDatabase

from src.common.statics import Gender
from src.diet.enums     import PhysicalActivityLevel


@unique
class DBKeys(Enum):
    """JSON Database keys."""
    NAME           = 'name'
    BIRTHDAY       = 'birthday'
    GENDER         = 'gender'
    HEIGHT_CM      = 'height_cm'
    INIT_WEIGHT_KG = 'init_weight_kg'
    PAL            = 'pal'


class User:
    """UserCredentials object manages all information about the user."""

    def __init__(self, credentials: UserCredentials) -> None:
        self.credentials = credentials
        self._name       = credentials.get_username()

        self._birthday = ''
        self._gender   = Gender.MALE

        self._height_cm      = 0
        self._init_weight_kg = 0

        self._pal = PhysicalActivityLevel.LightlyActive

        self.database = EncryptedDatabase(self.credentials)

    def __repr__(self) -> str:
        """Format User attributes."""
        return (f"<User-object {id(self)}>\n"
                f"  Name:        {self._name}\n"
                f"  Birthday:    {self._birthday}\n"
                f"  Gender:      {self._gender.value}\n"
                f"  Height:      {self._height_cm}\n"
                f"  Init Weight: {self._init_weight_kg}\n"
                f"  PAL:         {self._pal.value}\n")

    # Databases
    def serialize(self) -> bytes:
        """Serialize user's attributes into a bytestring."""
        return json.dumps({DBKeys.NAME.value           : self._name,
                           DBKeys.BIRTHDAY.value       : self._birthday,
                           DBKeys.GENDER.value         : self._gender.value,
                           DBKeys.HEIGHT_CM.value      : self._height_cm,
                           DBKeys.INIT_WEIGHT_KG.value : self._init_weight_kg,
                           DBKeys.PAL.value            : self._pal.value,
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

    # Setters
    def set_birthday(self, birthday: str) -> None:
        """Set the birthday of the user."""
        self._birthday = birthday
        self.store_db()

    def set_gender(self, gender: 'Gender') -> None:
        """Set gender for the user."""
        self._gender = gender
        self.store_db()

    # Setters
    def set_height(self, height: float) -> None:
        """Set the height of the user."""
        self._height_cm = height
        self.store_db()

    # Setters
    def set_init_weight(self, weight: float) -> None:
        """Set the initial weight of the user."""
        self._init_weight_kg = weight
        self.store_db()

    def set_pal(self, pal: 'PhysicalActivityLevel') -> None:
        """Set the Physical Activity Level (PAL) for the user."""
        self._pal = pal
        self.store_db()

    # Getters
    def get_gender(self) -> 'Gender':
        """Get the user's gender."""
        return self._gender

    def get_birthday(self) -> str:
        """Get the user's birthday."""
        return self._birthday

    def get_height(self) -> float:
        """Get the user's height in centimeters."""
        return self._height_cm

    def get_initial_weight(self) -> float:
        """Get the user's initial weight in kilograms."""
        return self._init_weight_kg

    def get_pal(self) -> 'PhysicalActivityLevel':
        """Get the user's Physical Activity Level (PAL)."""
        return self._pal
