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

from src.common.conversion import str_to_float, str_to_int, convert_input_fields
from src.common.exceptions import ConversionError
from src.ui.callback_classes import StringInput


class TestConversion(unittest.TestCase):

    def test_str_to_float(self) :

        # Test valid conversion
        for bool_ in [True, False]:
            self.assertEqual(str_to_float('test', '1.05', negative_allowed=bool_), 1.05)

        self.assertEqual(str_to_float('test', '-1.05', negative_allowed=True), -1.05)
        self.assertEqual(str_to_float('test', '-1',    negative_allowed=True), -1.0)

        # Test invalid conversion raises ConversionError

        # Negative when not allowed
        with self.assertRaises(ConversionError):
            str_to_float('test', '-1.05', negative_allowed=False)

        # Invalid values
        for bool_ in [True, False]:
            for value in ['string', '1.1.1', '']:
                with self.assertRaises(ConversionError):
                    str_to_float('test', value, negative_allowed=bool_)

    def test_str_to_int(self) :

        # Test valid conversion
        for bool_ in [True, False]:
            self.assertEqual(str_to_int('test', '1', negative_allowed=bool_), 1)

        self.assertEqual(str_to_int('test', '-1', negative_allowed=True), -1)

        # Test invalid conversion raises ConversionError

        # Negative when not allowed
        with self.assertRaises(ConversionError):
            str_to_int('test', '-1', negative_allowed=False)

        # Invalid values
        for bool_ in [True, False]:
            for value in ['string', '1.0', '']:
                with self.assertRaises(ConversionError):
                    str_to_int('test', value, negative_allowed=bool_)


class TestCovertInputFields(unittest.TestCase):

    def test_successful_conversions(self) :
        metadata = {
            'integer': ('integer', int   ),
            'float':   ('float',   float ),
            'string':  ('string',  str   ),
        }

        string_inputs = {'integer': StringInput(),
                         'float':   StringInput(),
                         'string':  StringInput()}

        string_inputs['integer'].set_value('1')
        string_inputs['float'].set_value('1.0')
        string_inputs['string'].set_value('test')

        success, value_dict = convert_input_fields(string_inputs, metadata)

        self.assertTrue(success)
        self.assertIsInstance(value_dict['integer'], int)
        self.assertIsInstance(value_dict['float'], float)
        self.assertIsInstance(value_dict['string'], str)

    def test_unsuccessful_conversions(self) :
        metadata = {
            'integer': ('integer', int   ),
            'float':   ('float',   float ),
            'string':  ('string',  str   ),
        }

        string_inputs = {'integer': StringInput(),
                         'float':   StringInput(),
                         'string':  StringInput()}

        string_inputs['integer'].set_value('a')
        string_inputs['float'].set_value('b')

        success, failed_conversions = convert_input_fields(string_inputs, metadata)

        self.assertFalse(success)
        self.assertIsNone(failed_conversions['integer'])
        self.assertIsNone(failed_conversions['float'])

    def test_unknown_type_raise_value_error(self) :
        metadata = {
            'integer' : ('integer',   int   ),
            'float'   :   ('float',   float ),
            'Nonetype':  ('Nonetype', None  ),
        }

        string_inputs = {'integer':  StringInput(),
                         'float':    StringInput(),
                         'Nonetype': StringInput()}

        string_inputs['integer'].set_value('a')
        string_inputs['float'].set_value('b')

        with self.assertRaises(ValueError):
            convert_input_fields(string_inputs, metadata)
