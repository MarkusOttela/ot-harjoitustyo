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

from src.common.exceptions import ValidationError
from src.common.validation import (validate_bool, validate_float, validate_int, validate_str,
                                   validate_type, validate_positive_float)


class TestValidation(unittest.TestCase):

    def test_validate_type(self) -> None:

        # Valid types
        for value, type_ in [('string', str),
                             (1,        int),
                             (0.1,      float),
                             (True,     bool)]:
            self.assertIsNone(validate_type('test', value, type_))

        # Invalid types
        for value, type_ in [('string', bool),
                             (1,        float),
                             (0.1,      int),
                             (True,     str)]:
            with self.assertRaises(ValidationError):
                validate_type('test', value, type_)

    def test_validate_str(self) -> None:
        # Valid values
        for bool_ in [True, False]:
            self.assertIsNone(validate_str('test', 'valid', empty_allowed=bool_))

        # Invalid values
        for bool_ in [True, False]:
            for value in [1, 1.0, True]:
                with self.assertRaises(ValidationError):
                    validate_str('test', value, empty_allowed=bool_)

        with self.assertRaises(ValidationError):
            validate_str('test', '', empty_allowed=False)

    def test_validate_int(self) -> None:
        # Valid values
        self.assertIsNone(validate_int('test',  5, negative_allowed=False))
        self.assertIsNone(validate_int('test', -5, negative_allowed=True))

        # Invalid values
        for bool_ in [True, False]:
            for value in ['string', 1.0]:
                with self.assertRaises(ValidationError):
                    validate_int('test', value, negative_allowed=bool_)

        with self.assertRaises(ValidationError):
            validate_int('test', -1, negative_allowed=False)

    def test_validate_float(self) -> None:
        # Valid values
        self.assertIsNone(validate_float('test',  5.0, negative_allowed=False))
        self.assertIsNone(validate_float('test', -5.0, negative_allowed=True))

        # Invalid values
        for bool_ in [True, False]:
            for value in ['string', 1, True]:
                with self.assertRaises(ValidationError):
                    validate_float('test', value, negative_allowed=bool_)

        with self.assertRaises(ValidationError):
            validate_float('test', -1.0, negative_allowed=False)

    def test_validate_bool(self) -> None:
        # Valid values
        self.assertIsNone(validate_bool('test', False))
        self.assertIsNone(validate_bool('test', True))

        for value in [1, 0, 1.0, -1.0, 'test', '']:
            # Invalid values
            with self.assertRaises(ValidationError):
                validate_bool('test', value)

    def test_validate_positive_float(self):
        # Valid values
        self.assertEqual(5.0,  validate_positive_float(' 5.0', 'test',))
        self.assertEqual(10.0, validate_positive_float(' 10.0', 'test', upper_limit=10.0))

        # Invalid values
        for bool_ in [None, 5]:
            for string in [None, '', '-1', 'string']:
                with self.assertRaises(ValueError):
                    validate_positive_float(string, 'test', upper_limit=bool_)

        # Upper limit exceeded
        with self.assertRaises(ValueError):
            validate_positive_float('10.1', 'test', upper_limit=10)
