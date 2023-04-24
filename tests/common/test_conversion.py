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

import unittest

from src.common.conversion import str_to_float, str_to_int
from src.common.exceptions import ConversionError


class TestConversion(unittest.TestCase):

    def test_str_to_float(self) -> None:

        # Test valid conversion
        for b in [True, False]:
            self.assertEqual(str_to_float('test', '1.05', negative_allowed=b), 1.05)

        self.assertEqual(str_to_float('test', '-1.05', negative_allowed=True), -1.05)
        self.assertEqual(str_to_float('test', '-1',    negative_allowed=True), -1.0)

        # Test invalid conversion raises ConversionError

        # Negative when not allowed
        with self.assertRaises(ConversionError):
            str_to_float('test', '-1.05', negative_allowed=False)

        # Invalid values
        for b in [True, False]:
            for v in ['string', '1.1.1', '']:
                with self.assertRaises(ConversionError):
                    str_to_float('test', v, negative_allowed=b)

    def test_str_to_int(self) -> None:

        # Test valid conversion
        for b in [True, False]:
            self.assertEqual(str_to_int('test', '1', negative_allowed=b), 1)

        self.assertEqual(str_to_int('test', '-1', negative_allowed=True), -1)

        # Test invalid conversion raises ConversionError

        # Negative when not allowed
        with self.assertRaises(ConversionError):
            str_to_int('test', '-1', negative_allowed=False)

        # Invalid values
        for b in [True, False]:
            for v in ['string', '1.0', '']:
                with self.assertRaises(ConversionError):
                    str_to_int('test', v, negative_allowed=b)
