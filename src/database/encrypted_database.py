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

from src.common.statics import DatabaseFileName, Directories
from src.common.utils   import write_bytes

if typing.TYPE_CHECKING:
    from src.common.security.user_credentials import UserCredentials


class EncryptedDatabase:
    """EncryptedDatabase contains JSON-format data, that is transparently encrypted."""

    def __init__(self, credentials: 'UserCredentials') -> None:
        """Create new EncryptedDatabase object."""
        self.credentials = credentials
        self.path_to_db  = (f'{Directories.USERDATA.value}'
                            f'/{self.credentials.get_username()}'
                            f'/{DatabaseFileName.USER_DATABASE.value}.db')

    def store_db(self, data: bytes) -> None:
        """Store the data into encrypted database"""
        ciphertext = self.credentials.encrypt(data)
        write_bytes(self.path_to_db, ciphertext)

    def load_db(self) -> bytes:
        """Authenticate, decrypt and return database plaintext bytes."""
        with open(self.path_to_db, 'rb') as f_ptr:
            database_ct = f_ptr.read()
        return self.credentials.decrypt(database_ct)
