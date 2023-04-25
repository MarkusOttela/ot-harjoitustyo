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
import os
import typing
import unittest

from src.common.security.crypto           import derive_database_key
from src.common.security.user_credentials import UserCredentials
from src.common.statics                   import Directories

from tests.utils import cd_unit_test, cleanup

if typing.TYPE_CHECKING:
    pass


class TestUserCredentials(unittest.TestCase):

    def setUp(self) -> None:
        self.unit_test_dir = cd_unit_test()
        self.test_password = 'password'
        self.test_salt     = 8*b'salt'
        _, self.test_key   = derive_database_key(self.test_password, self.test_salt)
        self.uc            = UserCredentials('test', self.test_salt, self.test_key)

    def tearDown(self) -> None:
        cleanup(self.unit_test_dir)

    def test_repr(self):
        self.assertEqual(repr(self.uc), """\
Username:    test
Salt:        73616c7473616c7473616c7473616c7473616c7473616c7473616c7473616c74
DB key hash: c51faf44405620badf5b7a785f6b672582ad07fe840b64bfdddbecdf6d32b22ef2302c9e147bd06f9fa58cfb18e1ddc3e10c7628d5527cee36a1c2122b959671""")

    def test_get_username_returns_username(self):
        self.assertEqual(self.uc.get_username(), 'test')

    def test_get_key_hash_returns_hash_of_key(self):
        self.assertEqual(self.uc.get_key_hash(), hashlib.blake2b(self.test_key).digest())

    def test_store_credentials_creates_file(self):
        self.uc.store_credentials()
        self.assertTrue(os.path.isdir(f'{Directories.USERDATA.value}/test'))
        self.assertTrue(os.path.isfile(f'{Directories.USERDATA.value}/test/credentials.db'))

    def test_loading_credentials_with_password(self):
        self.uc.store_credentials()
        self.assertTrue(os.path.isfile(f'{Directories.USERDATA.value}/test/credentials.db'))
        uc = UserCredentials.from_password('test', self.test_password)
        self.assertEqual(self.uc.get_key_hash(), uc.get_key_hash())

    def test_encrypting_and_decrypting_is_bijective(self):
        pt1 = b'plaintext'
        ct  = self.uc.encrypt(pt1)
        pt2 = self.uc.decrypt(ct)
        self.assertEqual(pt1, pt2)


if __name__ == '__main__':
    unittest.main(exit=False)
