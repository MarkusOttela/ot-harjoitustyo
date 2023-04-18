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

from src.common.statics import Directories
from src.common.utils import ensure_dir, write_bytes


class User:
    """User object stores all information about the user."""

    def __init__(self, name: str, salt: bytes, database_key: bytes) -> None:
        """Create new User object."""
        self.__name         : str   = name
        self.__salt         : bytes = salt
        self.__database_key : bytes = database_key
        self.__userdata_dir : str   = f'{Directories.USERDATA.value}/{self.__name}'

        self.store_credentials()

    def __repr__(self) -> str:
        """Represent user object's data."""
        return f"Username:    {self.__name}\n" \
               f"Salt:        {self.__salt.hex()}\n" \
               f"DB key hash: {self.get_key_hash().hex()}"

    def get_key_hash(self) -> bytes:
        """Get key hash."""
        return hashlib.blake2b(self.__database_key).digest()

    def store_credentials(self) -> None:
        """Store credentials into a database."""
        data_to_store = self.__salt + self.get_key_hash()
        ensure_dir(self.__userdata_dir)
        write_bytes(f'{self.__userdata_dir}/credentials.db', data_to_store)
