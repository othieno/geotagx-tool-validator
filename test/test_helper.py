# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project sanitizer tool.
# It contains unit tests for helper module.
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
import unittest, helper

class TestHelperFunctions(unittest.TestCase):
    def test_empty_strings(self):
        self.assertTrue(helper.is_empty_string(""), "Empty string.")
        self.assertTrue(helper.is_empty_string("   "), "Empty string (whitespace only).")
        self.assertTrue(helper.is_empty_string("\r\n\t"), "Empty string (escape sequences).")

    def test_nonempty_strings(self):
        self.assertRaises(TypeError, helper.is_empty_string, None)
        self.assertRaises(TypeError, helper.is_empty_string, {})
        self.assertRaises(TypeError, helper.is_empty_string, 42)
        self.assertRaises(TypeError, helper.is_empty_string, [])
        self.assertFalse(helper.is_empty_string("Hello, World"), "Non-empty string.")
        self.assertFalse(helper.is_empty_string("   *"), "String with leading whitespace and asterisk.")
        self.assertFalse(helper.is_empty_string("trailblazer   "), "String with trailing whitespace.")
        self.assertFalse(helper.is_empty_string("    Hello, World    "), "String with leading and trailing whitespace.")
        self.assertFalse(helper.is_empty_string("\r\n\t\\"), "Escape sequences with backslash character.")


if __name__ == "__main__":
    unittest.main()
