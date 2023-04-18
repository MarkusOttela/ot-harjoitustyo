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

import hashlib
import secrets

from src.common.exceptions      import IncorrectPassword
from src.common.security.crypto import CryptoLiterals, derive_database_key
from src.common.statics         import Directories
from src.common.utils           import ensure_dir, write_bytes


class UserCredentials:
    """UserCredentials object manages the user's login information."""

    def __init__(self,
                 name         : str,
                 salt         : bytes,
                 database_key : bytes
                 ) -> None:
        """Create new UserCredentials object."""
        self.__name           : str   = name
        self.__salt           : bytes = salt
        self.__database_key   : bytes = database_key
        self.__userdata_dir   : str   = f'{Directories.USERDATA.value}/{self.__name}'
        self.__credentials_db : str   = f'{self.__userdata_dir}/credentials.db'

        self.store_credentials()

    def __repr__(self) -> str:
        """Represent user object's data."""
        return f"Username:    {self.__name}\n" \
               f"Salt:        {self.__salt.hex()}\n" \
               f"DB key hash: {self.get_key_hash().hex()}"

    def get_username(self) -> str:
        """Get the username."""
        return self.__name

    def get_key_hash(self) -> bytes:
        """Get key hash."""
        return hashlib.blake2b(self.__database_key).digest()

    def store_credentials(self) -> None:
        """Store credentials into a database."""
        ensure_dir(self.__userdata_dir)

        data_to_store = self.__salt + self.get_key_hash()
        write_bytes(self.__credentials_db, data_to_store)

    @staticmethod
    def from_password(name: str, password: str) -> 'UserCredentials':
        """Initialize User from name and password."""
        userdata_dir   = f'{Directories.USERDATA.value}/{name}'
        credentials_db = f'{userdata_dir}/credentials.db'

        with open(credentials_db, 'rb') as f:
            data = f.read()

        salt   = data[:CryptoLiterals.SALT_LENGTH.value]
        digest = data[CryptoLiterals.SALT_LENGTH.value:]

        _, purp_key = derive_database_key(password, salt)
        prup_digest = hashlib.blake2b(purp_key).digest()

        if secrets.compare_digest(digest, prup_digest):
            return UserCredentials(name, salt, purp_key)
        else:
            raise IncorrectPassword("Incorrect password")
