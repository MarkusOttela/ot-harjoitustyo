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
import typing
import unittest

from unittest import mock

from src.common.crypto import derive_database_key
from src.common.enums  import Directories, DatabaseFileName

from src.database.encrypted_database import EncryptedDatabase
from src.entities.user_credentials   import UserCredentials

from tests.utils import cd_unit_test, cleanup

if typing.TYPE_CHECKING:
    pass


class TestEncryptedDatabase(unittest.TestCase):

    def setUp(self) :
        self.unit_test_dir = cd_unit_test()
        self.test_password = 'password'
        self.test_salt     = 8*b'salt'
        with mock.patch('multiprocessing.cpu_count', return_value=1):
            _, self.test_key = derive_database_key(self.test_password, self.test_salt)
        self.uc = UserCredentials('test', self.test_salt, self.test_key)

    def tearDown(self) :
        cleanup(self.unit_test_dir)

    def test_storing_database_creates_the_database(self):
        db = EncryptedDatabase(self.uc)
        db.store_db(b'test_data')

        self.assertTrue(os.path.isdir(f'{Directories.USER_DATA.value}/test/'))
        self.assertTrue(os.path.isfile(f'{Directories.USER_DATA.value}/test/{DatabaseFileName.USER_DATABASE.value}.db'))

    def test_loading_data_works(self):
        test_data = b'test_data'
        db = EncryptedDatabase(self.uc)
        db.store_db(test_data)

        purp_data = db.load_db()
        self.assertEqual(purp_data, test_data)
