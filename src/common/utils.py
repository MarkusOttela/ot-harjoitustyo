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

import os

from datetime import datetime

from src.common.exceptions import ignored
from src.common.statics    import Directories, Format


def ensure_dir(directory: str) -> None:
    """Ensure directory exists."""
    if not directory.endswith('/'):
        directory += '/'

    name = os.path.dirname(directory)
    if not os.path.exists(name):
        with ignored(FileExistsError):
            os.makedirs(name)


def write_bytes(path_to_file: str, data: bytes) -> None:
    """Ensure bytestring is written to the disc."""
    with open(path_to_file, 'wb') as f_ptr:
        f_ptr.write(data)
        f_ptr.flush()
        os.fsync(f_ptr)


def get_list_of_user_account_names() -> list:
    """Get list of user account names."""
    return next(os.walk(Directories.USERDATA.value))[1]


def separate_header(bytestring    : bytes,     # Bytestring to slice
                    header_length : int        # Number of header bytes to separate
                    ) -> tuple:                # Header and payload
    """Separate `header_length` first bytes from a bytestring."""
    return bytestring[:header_length], bytestring[header_length:]


def get_today_str() -> str:
    """Get today's date in string format."""
    return datetime.today().strftime(Format.DATETIME_DATE.value)
