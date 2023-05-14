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
import unittest

from unittest import mock

from src.common.crypto     import derive_database_key
from src.common.enums      import Directories
from src.common.exceptions import IncorrectPassword

from src.entities.user_credentials import UserCredentials

from tests.utils import cd_unit_test, cleanup


class TestUserCredentials(unittest.TestCase):

    def setUp(self) :
        self.unit_test_dir = cd_unit_test()
        self.test_password = 'password'
        self.test_salt     = 8*b'Salt'
        with mock.patch('multiprocessing.cpu_count', return_value=1):
            _, self.test_key = derive_database_key(self.test_password, self.test_salt)
        self.user_credentials = UserCredentials('test', self.test_salt, self.test_key)

    def tearDown(self) :
        cleanup(self.unit_test_dir)

    def test_repr(self):
        expected_digest = ('d41f0a313abeeed965710d58e7ab111873624ff9f54e5567754e3b2fb2f90623'
                           '346b9abd8c8ca667e7562e4708130891f457afe9174a6524e89d5f02119e8291')
        self.assertEqual(repr(self.user_credentials), f"""\
<UserCredentials-object {id(self.user_credentials)}>
  User Name:   test
  Salt:        53616c7453616c7453616c7453616c7453616c7453616c7453616c7453616c74
  DB key hash: {expected_digest}""")

    def test_get_username_returns_username(self):
        self.assertEqual(self.user_credentials.get_username(), 'test')

    def test_get_key_hash_returns_hash_of_key(self):
        self.assertEqual(self.user_credentials.get_key_hash(),
                         hashlib.blake2b(self.test_key).digest())

    def test_store_credentials_creates_file(self):
        self.user_credentials.store_credentials()
        self.assertTrue(os.path.isdir(f'{Directories.USER_DATA.value}/test'))
        self.assertTrue(os.path.isfile(f'{Directories.USER_DATA.value}/test/credentials.db'))

    def test_loading_credentials_with_incorrect_password_raises_incorrect_password(self):
        self.user_credentials.store_credentials()
        self.assertTrue(os.path.isfile(f'{Directories.USER_DATA.value}/test/credentials.db'))
        with mock.patch('multiprocessing.cpu_count', return_value=1):
            with self.assertRaises(IncorrectPassword):
                UserCredentials.from_password('test', 'incorrect')

    def test_loading_credentials_with_password(self):
        self.user_credentials.store_credentials()
        self.assertTrue(os.path.isfile(f'{Directories.USER_DATA.value}/test/credentials.db'))
        with mock.patch('multiprocessing.cpu_count', return_value=1):
            user_credentials = UserCredentials.from_password('test', self.test_password)
        self.assertEqual(self.user_credentials.get_key_hash(), user_credentials.get_key_hash())

    def test_encrypting_and_decrypting_is_bijective(self):
        plaintext1 = b'plaintext'
        ciphertext  = self.user_credentials.encrypt(plaintext1)
        plaintext2 = self.user_credentials.decrypt(ciphertext)
        self.assertEqual(plaintext1, plaintext2)


if __name__ == '__main__':
    unittest.main(exit=False)
