#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

"""
Calorienator - Diet tracker
Copyright (C) Markus Ottela

This file is part of Calorienator.
Calorienator is free software: you can redistribute it and/or modify it under the 
terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version. Calorienator is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
details. You should have received a copy of the GNU General Public License
along with Calorienator. If not, see <https://www.gnu.org/licenses/>.
"""

import unittest

from src.common.exceptions import ignored


class TestIgnored(unittest.TestCase):

    @staticmethod
    def func() -> None:
        """Mock function that raises exception."""
        raise KeyboardInterrupt

    def test_ignored_contextmanager(self) -> None:
        raised = False
        try:
            with ignored(KeyboardInterrupt):
                TestIgnored.func()
        except KeyboardInterrupt:
            raised = True
        self.assertFalse(raised)
