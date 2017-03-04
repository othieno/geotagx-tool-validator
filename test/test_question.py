# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project sanitizer tool.
# It contains unit tests for the question module.
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
        self.assertTrue(validator.is_question_key("A")[0], "Single-character")
        self.assertTrue(validator.is_question_key("key")[0], "String")
        self.assertTrue(validator.is_question_key("42")[0], "String with numeric characters only")
        self.assertTrue(validator.is_question_key("now-y0u_4re-pushing-1t")[0], "Mixed characters")
        self.assertTrue(validator.is_question_key("--")[0], "Hyphens only")
        self.assertTrue(validator.is_question_key("--__")[0], "Hyphens and underscores only")
        self.assertTrue(validator.is_question_key("--key")[0], "Leading hyphens")

    def test_illegal_question_keys(self):
        self.assertRaises(TypeError, validator.is_question_key, None)
        self.assertRaises(TypeError, validator.is_question_key, 42)
        self.assertRaises(TypeError, validator.is_question_key, [])
        self.assertRaises(TypeError, validator.is_question_key, {})
        self.assertFalse(validator.is_question_key("")[0], "Empty string")
        self.assertFalse(validator.is_question_key("   ")[0], "Whitespace only")
        self.assertFalse(validator.is_question_key("  key")[0], "Leading whitespace")
        self.assertFalse(validator.is_question_key("end\t")[0], "Traling tabulation")
        self.assertFalse(validator.is_question_key("*$/\\")[0], "Unaccepted characters")
        self.assertFalse(validator.is_question_key("\n")[0], "Illegal escape character")
        self.assertFalse(validator.is_question_key("_end")[0], "Leading underscore (reserved key)")
        self.assertFalse(validator.is_question_key("__--")[0], "Multiple leading underscores (reserved key)")

    def test_valid_reserved_keys(self):
        self.assertTrue(validator.is_reserved_question_key("__")[0], "Underscores only")
        self.assertTrue(validator.is_reserved_question_key("__--")[0], "Underscores and hyphens only")
        self.assertTrue(validator.is_reserved_question_key("__key")[0], "Leading underscores")
        self.assertTrue(validator.is_reserved_question_key("_now-y0u_4re-pushing-1t")[0], "Mixed characters")

    def test_illegal_reserved_keys(self):
        self.assertRaises(TypeError, validator.is_reserved_question_key, None)
        self.assertRaises(TypeError, validator.is_reserved_question_key, 42)
        self.assertRaises(TypeError, validator.is_reserved_question_key, [])
        self.assertRaises(TypeError, validator.is_reserved_question_key, {})
        self.assertFalse(validator.is_reserved_question_key("")[0], "Empty string")
        self.assertFalse(validator.is_reserved_question_key("   ")[0], "Whitespace only")
        self.assertFalse(validator.is_reserved_question_key("  key")[0], "Leading whitespace")
        self.assertFalse(validator.is_reserved_question_key("__  key")[0], "Whitespace in between characters")
        self.assertFalse(validator.is_reserved_question_key("end")[0], "No leading underscore")
        self.assertFalse(validator.is_reserved_question_key("_end\t")[0], "Traling tabulation")
        self.assertFalse(validator.is_reserved_question_key("*$/\\")[0], "Unaccepted characters")
        self.assertFalse(validator.is_reserved_question_key("\n")[0], "Illegal escape character")

    def test_valid_question_titles(self):
        self.assertTrue(validator.is_question_title("Is this a question title?")[0], "Simple title")
        self.assertTrue(validator.is_question_title({"en":"Is this a normalized title?"})[0], "Normalized title")

    def test_illegal_question_titles(self):
        self.assertRaises(TypeError, validator.is_question_title, None)
        self.assertRaises(TypeError, validator.is_question_title, 42)
        self.assertRaises(TypeError, validator.is_question_title, [])
        self.assertRaises(TypeError, validator.is_question_title, {"la":"Et tu, Brute?"}, 42)
        self.assertRaises(TypeError, validator.is_question_title, {"la":"Et tu, Brute?"}, {})
        self.assertFalse(validator.is_question_title({"en":None})[0], "No normalized title")
        self.assertFalse(validator.is_question_title({"en":""})[0], "Empty normalized title")
        self.assertFalse(validator.is_question_title({"en":"     "})[0], "Whitespace only")
        self.assertFalse(validator.is_question_title({42:"This is an invalid title."})[0], "Normalized title with illegal language code")
        self.assertFalse(validator.is_question_title({"fr-Latin":"Ceci est un rappel."})[0], "Normalized title with illegal language code")

    def test_valid_questions(self):
        pass

    def test_illegal_questions(self):
        self.assertRaises(TypeError, validator.is_question, None)
        self.assertRaises(TypeError, validator.is_question, "")
        self.assertRaises(TypeError, validator.is_question, 42)
        self.assertFalse(validator.is_question({})[0], "Empty dict")
