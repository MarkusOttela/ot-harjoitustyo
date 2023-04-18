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

import multiprocessing
import os

from typing import Optional

import argon2

from enum import Enum


class CryptoLiterals(Enum):
    """Cryptographic variables."""
    SYMMETRIC_KEY_LENGTH = 32
    BLAKE2_DIGEST_LENGTH = 64
    SALT_LENGTH          = 32


def derive_database_key(password: str, salt: Optional[bytes] = None) -> tuple:
    """Derive encryption key from password and salt."""
    if salt is None:
        salt = os.getrandom(CryptoLiterals.SALT_LENGTH.value, flags=0)

    key = argon2.low_level.hash_secret_raw(secret=password.encode(),
                                           salt=salt,
                                           time_cost=20,
                                           memory_cost=1000,  # TODO REPLACE WITH 512*1024,
                                           parallelism=multiprocessing.cpu_count(),
                                           hash_len=CryptoLiterals.SYMMETRIC_KEY_LENGTH.value,
                                           type=argon2.Type.ID)  # type: bytes
    return salt, key
