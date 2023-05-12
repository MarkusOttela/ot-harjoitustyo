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

import os
import unittest

from src.common.exceptions import ignored
from src.common.utils      import ensure_dir


class TestEnsureDir(unittest.TestCase):

    def tearDown(self) -> None:
        """Post-test actions."""
        with ignored(OSError):
            os.rmdir('test_dir/')

    def test_ensure_dir(self) -> None:
        self.assertIsNone(ensure_dir('test_dir/'))
        self.assertIsNone(ensure_dir('test_dir/'))
        self.assertTrue(os.path.isdir('test_dir/'))
