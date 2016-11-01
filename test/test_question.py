# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project sanitizer tool.
# It contains unit tests for question module.
#
# Author: Jeremy Othieno (j.othieno@gmail.com)
#
# Copyright (c) 2016 UNITAR/UNOSAT
#
# The MIT License (MIT)
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
import unittest
import question as validator

class TestQuestionValidators(unittest.TestCase):
    def test_valid_question_keys(self):
        self.assertTrue(validator.is_key("A")[0], "Single-character")
        self.assertTrue(validator.is_key("key")[0], "String")
        self.assertTrue(validator.is_key("42")[0], "String with numeric characters only")
        self.assertTrue(validator.is_key("now-y0u_4re-pushing-1t")[0], "Mixed characters")
        self.assertTrue(validator.is_key("--")[0], "Hyphens only")
        self.assertTrue(validator.is_key("--__")[0], "Hyphens and underscores only")
        self.assertTrue(validator.is_key("--key")[0], "Leading hyphens")

    def test_illegal_question_keys(self):
        self.assertFalse(validator.is_key(None)[0], "No value")
        self.assertFalse(validator.is_key("")[0], "Empty string")
        self.assertFalse(validator.is_key("   ")[0], "Whitespace only")
        self.assertFalse(validator.is_key("  key")[0], "Leading whitespace")
        self.assertFalse(validator.is_key("end\t")[0], "Traling tabulation")
        self.assertFalse(validator.is_key("*$/\\")[0], "Unaccepted characters")
        self.assertFalse(validator.is_key("\n")[0], "Illegal escape character")
        self.assertFalse(validator.is_key("_end")[0], "Leading underscore (reserved key)")
        self.assertFalse(validator.is_key("__--")[0], "Multiple leading underscores")
        self.assertFalse(validator.is_key(42)[0], "Not a string (number)")
        self.assertFalse(validator.is_key([])[0], "Not a string (list)")
        self.assertFalse(validator.is_key({})[0], "Not a string (dictionary)")
