#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

"""
Calorinator - Diet tracker
Copyright (C) Markus Ottela

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
import datetime
import os
import unittest

from src.common.enums      import Directories
from src.common.exceptions import ignored

from src.common.utils      import (ensure_dir, write_bytes, get_list_of_user_account_names,
                                   separate_header, get_today_str)

from tests.utils import cd_unit_test, cleanup


class TestEnsureDir(unittest.TestCase):

    def tearDown(self):
        """Post-test actions."""
        with ignored(OSError):
            os.rmdir('test_dir/')

    def test_ensure_dir(self):
        self.assertIsNone(ensure_dir('test_dir/'))
        self.assertIsNone(ensure_dir('test_dir/'))
        self.assertTrue(os.path.isdir('test_dir/'))


class TestWriteBytes(unittest.TestCase):

    def setUp(self) :
        self.unit_test_dir = cd_unit_test()

    def tearDown(self) :
        cleanup(self.unit_test_dir)

    def test_function_writes_bytes_to_file(self):
        bytestring = os.getrandom(32)

        write_bytes('test_file', bytestring)

        self.assertTrue(os.path.isfile('test_file'))

        with open('test_file', 'rb') as f_ptr:
            data = f_ptr.read()

        self.assertEqual(data, bytestring)


class TestGetListOfUserAccountNames(unittest.TestCase):

    def setUp(self) :
        self.unit_test_dir = cd_unit_test()

    def tearDown(self) :
        cleanup(self.unit_test_dir)

    def test_empty_directory(self):
        lst = get_list_of_user_account_names()
        self.assertIsInstance(lst, list)
        self.assertEqual(len(lst), 0)

    def test_single_username(self):
        ensure_dir(Directories.USER_DATA.value)
        os.mkdir(f'{Directories.USER_DATA.value}/test')

        lst = get_list_of_user_account_names()
        self.assertIsInstance(lst, list)
        self.assertEqual(len(lst), 1)

    def test_multiple_usernames(self):
        ensure_dir(Directories.USER_DATA.value)
        os.mkdir(f'{Directories.USER_DATA.value}/test')
        os.mkdir(f'{Directories.USER_DATA.value}/test2')
        os.mkdir(f'{Directories.USER_DATA.value}/test3')

        lst = get_list_of_user_account_names()
        self.assertIsInstance(lst, list)
        self.assertEqual(len(lst), 3)


class TestSeparateHeader(unittest.TestCase):

    def test_separate_header(self) :
        tup = separate_header(b"teststring", header_length=len(b"test"))
        self.assertEqual(tup, (b"test", b"string"))


class TestGetTodayStr(unittest.TestCase):

    def test_get_today_str(self):
        purp_string      = get_today_str()
        day, month, year = purp_string.split('/')
        self.assertEqual(int(day), datetime.datetime.today().day)
        self.assertEqual(int(month), datetime.datetime.today().month)
        self.assertEqual(int(year), datetime.datetime.today().year)
