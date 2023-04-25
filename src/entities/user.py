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

from src.common.security.user_credentials import UserCredentials
from src.database.encrypted_database      import EncryptedDatabase

from src.common.statics import Gender


class User:
    """UserCredentials object manages all information about the user."""

    def __init__(self, credentials: UserCredentials) -> None:
        self.credentials = credentials
        self._name       = credentials.get_username()
        self._birthday   = ''
        self._gender     = None
        self._birthday   = ''
        self.database    = EncryptedDatabase(self.credentials)

    def __repr__(self) -> str:
        """Format User attributes."""
        return f"<User-object {id(self)}> (Username: {self._name})"

    # Databases
    def serialize(self) -> bytes:
        """Serialize user's attributes into a bytestring."""
        return json.dumps({'name'     : self._name,
                           'birthday' : self._birthday,
                           'gender'   : self.get_gender().value}).encode()

    def store_db(self) -> None:
        """Store the user's data into the database."""
        self.database.store_db(self.serialize())

    def load_db(self) -> None:
        """Load user's data"""
        serialized_data = self.database.load_db()
        json_db         = json.loads(serialized_data)

        self._name     = json_db['name']
        self._birthday = json_db['birthday']
        self._gender   = Gender.MALE if json_db['name'] == 'male' else Gender.FEMALE

    # Setters
    def set_birthday(self, birthday: str) -> None:
        """Set the birthday of the user."""
        self._birthday = birthday
        self.store_db()

    def set_gender(self, gender: 'Gender') -> None:
        """Set gender for the user."""
        self._gender = gender
        self.store_db()

    # Getters
    def get_gender(self) -> 'Gender':
        """Get the user's gender."""
        return self._gender

    def get_birthday(self) -> str:
        """Get the user's birthday."""
        return self._birthday
