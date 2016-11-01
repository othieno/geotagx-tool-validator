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

    def test_valid_iso_3166_1_alpha_2_codes(self):
        self.assertTrue(helper.is_iso_3166_1_alpha_2_code("CH"), "Switzerland")
        self.assertTrue(helper.is_iso_3166_1_alpha_2_code("GB"), "United Kingdom")
        self.assertTrue(helper.is_iso_3166_1_alpha_2_code("US"), "United States")
        self.assertTrue(helper.is_iso_3166_1_alpha_2_code("UG"), "Uganda")

    def test_illegal_iso_3166_1_alpha_2_codes(self):
        self.assertFalse(helper.is_iso_3166_1_alpha_2_code(None), "No code")
        self.assertFalse(helper.is_iso_3166_1_alpha_2_code(""), "Empty string")
        self.assertFalse(helper.is_iso_3166_1_alpha_2_code({}), "Non-string value (dictionary)")
        self.assertFalse(helper.is_iso_3166_1_alpha_2_code(42), "Non-string value (number)")
        self.assertFalse(helper.is_iso_3166_1_alpha_2_code("42"), "String containing non-alphabet characters")
        self.assertFalse(helper.is_iso_3166_1_alpha_2_code("A4"), "Two-character string containing a numeric character")
        self.assertFalse(helper.is_iso_3166_1_alpha_2_code("ch"), "Lowercase ISO code")
        self.assertFalse(helper.is_iso_3166_1_alpha_2_code("   CH"), "Valid ISO code with leading whitespace.")
        self.assertFalse(helper.is_iso_3166_1_alpha_2_code("CH   "), "Valid ISO code with trailing whitespace.")

    def test_valid_iso_15924_codes(self):
        self.assertTrue(helper.is_iso_15924_code("Latn"), "Latin")
        self.assertTrue(helper.is_iso_15924_code("Cyrl"), "Cyrillic")
        self.assertTrue(helper.is_iso_15924_code("Hans"), "Han (Simplified)")
        self.assertTrue(helper.is_iso_15924_code("Zzzz"), "Uncoded script")

    def test_illegal_iso_15924_codes(self):
        self.assertFalse(helper.is_iso_15924_code(None), "No code")
        self.assertFalse(helper.is_iso_15924_code(""), "Empty string")
        self.assertFalse(helper.is_iso_15924_code({}), "Non-string value (dictionary)")
        self.assertFalse(helper.is_iso_15924_code(42), "Non-string value (number)")
        self.assertFalse(helper.is_iso_15924_code("42"), "String containing non-alphabet characters")
        self.assertFalse(helper.is_iso_15924_code("A444"), "Four-character string containing numeric characters")
        self.assertFalse(helper.is_iso_15924_code("latn"), "Non-capitalized code")
        self.assertFalse(helper.is_iso_15924_code("Latin"), "Five-letter code")
        self.assertFalse(helper.is_iso_15924_code("    Latn"), "Valid ISO code with leading whitespace")
        self.assertFalse(helper.is_iso_15924_code("Latn    "), "Valid ISO code with trailing whitespace")

    def test_valid_language_codes(self):
        self.assertTrue(helper.is_language_code("en"), "English")
        self.assertTrue(helper.is_language_code("fr"), "French")
        self.assertTrue(helper.is_language_code("de"), "German")
        self.assertTrue(helper.is_language_code("it"), "Italian")
        self.assertTrue(helper.is_language_code("haw"), "Hawaiian")
        self.assertTrue(helper.is_language_code("en-US"), "English (American)")
        self.assertTrue(helper.is_language_code("pt-BR"), "Portuguese (Brazilian)")
        self.assertTrue(helper.is_language_code("zh-Hans"), "Chinese (Simplified)")
        self.assertTrue(helper.is_language_code("zh-Hant"), "Chinese (Traditional)")
        self.assertTrue(helper.is_language_code("az-Arab"), "Azerbaijani (Arabic script)")
        self.assertTrue(helper.is_language_code("az-Cyrl"), "Azerbaijani (Cyrillic script)")
        self.assertTrue(helper.is_language_code("bs-Latn"), "Bosnian (Latin script)")

    def test_illegal_language_codes(self):
        self.assertFalse(helper.is_language_code(None), "No code")
        self.assertFalse(helper.is_language_code(""), "Empty string")
        self.assertFalse(helper.is_language_code({}), "Non-string value (dictionary)")
        self.assertFalse(helper.is_language_code(42), "Non-string value (number)")
        self.assertFalse(helper.is_language_code("42"), "String containing non-alphabet characters")
        self.assertFalse(helper.is_language_code("FR"), "Uppercase string")
        self.assertFalse(helper.is_language_code("e"), "Single-character string")
        self.assertFalse(helper.is_language_code("en    "), "String containing trailing whitespace")
        self.assertFalse(helper.is_language_code("    en"), "String containing leading whitespace")
        self.assertFalse(helper.is_language_code("en fr"), "Missing hyphen separator")
        self.assertFalse(helper.is_language_code("en_GB"), "Underscore used as separator")
        self.assertFalse(helper.is_language_code("en- GB"), "Whitespace after hyphen separator")
        self.assertFalse(helper.is_language_code("en   -GB"), "Whitespace before hyphen separator")
        self.assertFalse(helper.is_language_code("-en-GB"), "Leading hyphen")
        self.assertFalse(helper.is_language_code("az-Latin"), "Invalid script name (longer than 4 letters)")
        self.assertFalse(helper.is_language_code("az-latn"), "Invalid script name (not capitalized)")
