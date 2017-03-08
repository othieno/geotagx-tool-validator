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
    def test_valid_questions(self):
        self.assertTrue(validator.is_question({
            "key": "ready",
            "title": "Are you ready?",
            "input": {
                "type": "polar"
            },
        })[0], "Simple question configuration")

    def test_illegal_questions(self):
        self.assertRaises(TypeError, validator.is_question, None)
        self.assertRaises(TypeError, validator.is_question, 42)
        self.assertRaises(TypeError, validator.is_question, [])
        self.assertRaises(TypeError, validator.is_question, "")
        self.assertFalse(validator.is_question({})[0], "Empty dictionary")
        self.assertFalse(validator.is_question({
            "key": "ready",
            "title": "Are you ready?",
            "input": {
                "type": "polar"
            },
            "hintr": "This field's key has a typo!",
        })[0], "Unrecognized field")
        self.assertFalse(validator.is_question({
            "title": "Are you ready?",
            "input": {
                "type": "polar"
            },
        })[0], "Missing key field")
        self.assertFalse(validator.is_question({
            "key": "ready",
            "input": {
                "type": "polar"
            },
        })[0], "Missing title field")
        self.assertFalse(validator.is_question({
            "key": "ready",
            "title": "Are you ready?",
        })[0], "Missing input field")

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
        self.assertTrue(validator.is_reserved_key("__")[0], "Underscores only")
        self.assertTrue(validator.is_reserved_key("__--")[0], "Underscores and hyphens only")
        self.assertTrue(validator.is_reserved_key("__key")[0], "Leading underscores")
        self.assertTrue(validator.is_reserved_key("_now-y0u_4re-pushing-1t")[0], "Mixed characters")

    def test_illegal_reserved_keys(self):
        self.assertRaises(TypeError, validator.is_reserved_key, None)
        self.assertRaises(TypeError, validator.is_reserved_key, 42)
        self.assertRaises(TypeError, validator.is_reserved_key, [])
        self.assertRaises(TypeError, validator.is_reserved_key, {})
        self.assertFalse(validator.is_reserved_key("")[0], "Empty string")
        self.assertFalse(validator.is_reserved_key("   ")[0], "Whitespace only")
        self.assertFalse(validator.is_reserved_key("  key")[0], "Leading whitespace")
        self.assertFalse(validator.is_reserved_key("__  key")[0], "Whitespace in between characters")
        self.assertFalse(validator.is_reserved_key("end")[0], "No leading underscore")
        self.assertFalse(validator.is_reserved_key("_end\t")[0], "Traling tabulation")
        self.assertFalse(validator.is_reserved_key("*$/\\")[0], "Unaccepted characters")
        self.assertFalse(validator.is_reserved_key("\n")[0], "Illegal escape character")

    def test_valid_question_titles(self):
        self.assertTrue(validator.is_question_title("Is this a question title?")[0], "Simple title")
        self.assertTrue(validator.is_question_title({"en":"Is this a normalized title?"})[0], "Normalized title")
        self.assertTrue(validator.is_question_title({
            "en":"Is this a normalized title?",
            "fr":"Est-ce un titre normalisé?",
        })[0], "Normalized title with translation")

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

    def test_valid_question_help(self):
        self.assertTrue(validator.is_question_help("This is not a helpful question hint.")[0], "Simple hint")
        self.assertTrue(validator.is_question_help({"en":"Is this a normalized hint?"})[0], "Normalized hint")

    def test_illegal_question_help(self):
        self.assertRaises(TypeError, validator.is_question_help, None)
        self.assertRaises(TypeError, validator.is_question_help, 42)
        self.assertRaises(TypeError, validator.is_question_help, [])
        self.assertRaises(TypeError, validator.is_question_help, {"la":"Et tu, Brute?"}, 42)
        self.assertRaises(TypeError, validator.is_question_help, {"la":"Et tu, Brute?"}, {})
        self.assertFalse(validator.is_question_help({"en":None})[0], "No normalized hint")
        self.assertFalse(validator.is_question_help({"en":""})[0], "Empty normalized hint")
        self.assertFalse(validator.is_question_help({"en":"     "})[0], "Whitespace only")
        self.assertFalse(validator.is_question_help({42:"This is an invalid hint."})[0], "Normalized hint with illegal language code")
        self.assertFalse(validator.is_question_help({"fr-Latin":"Ceci est un rappel."})[0], "Normalized hint with illegal language code")

    def test_valid_question_branches(self):
        self.assertTrue(validator.is_question_branch("start")[0], "Question key")
        self.assertTrue(validator.is_question_branch("_stop")[0], "Reserved question key")
        self.assertTrue(validator.is_question_branch({
            "no":"start",
            "yes":"stop",
            "okay":"_on",
        })[0], "Multiple branch nodes")

    def test_illegal_question_branches(self):
        self.assertRaises(TypeError, validator.is_question_branch, None)
        self.assertRaises(TypeError, validator.is_question_branch, 42)
        self.assertRaises(TypeError, validator.is_question_branch, [])
        self.assertFalse(validator.is_question_branch("")[0], "Empty string")
        self.assertFalse(validator.is_question_branch({})[0], "Empty dictionary")

    def test_valid_question_input(self):
        pass

    def test_illegal_question_input(self):
        self.assertRaises(TypeError, validator.is_question_input, None)
        self.assertRaises(TypeError, validator.is_question_input, 42)
        self.assertRaises(TypeError, validator.is_question_input, "")
        self.assertRaises(TypeError, validator.is_question_input, [])
        self.assertRaises(TypeError, validator.is_question_input, {}, 42)
        self.assertRaises(TypeError, validator.is_question_input, {}, "")
        self.assertRaises(TypeError, validator.is_question_input, {}, {})
        self.assertRaises(TypeError, validator.is_question_input, {"type": 42})
        self.assertRaises(TypeError, validator.is_question_input, {"type": []})
        self.assertRaises(TypeError, validator.is_question_input, {"type": {}})
        self.assertFalse(validator.is_question_input({})[0], "Empty dictionary")
        self.assertFalse(validator.is_question_input({"type": None})[0], "Undefined input type")
        self.assertFalse(validator.is_question_input({"type": ""})[0], "Empty input type")
        self.assertFalse(validator.is_question_input({"type": "xyz"})[0], "Unrecognized input type")

    def test_valid_question_input_types(self):
        self.assertTrue(validator.is_question_input_type("polar"), "Polar (Yes/No) input")
        self.assertTrue(validator.is_question_input_type("dropdown-list"), "Dropdown list input")
        self.assertTrue(validator.is_question_input_type("multiple-choice"), "Multiple-choice input")
        self.assertTrue(validator.is_question_input_type("text"), "Text input")
        self.assertTrue(validator.is_question_input_type("number"), "Number input")
        self.assertTrue(validator.is_question_input_type("datetime"), "Date and time input")
        self.assertTrue(validator.is_question_input_type("url"), "URL input")
        self.assertTrue(validator.is_question_input_type("geotagging"), "Geotagging input")

    def test_illegal_question_input_types(self):
        self.assertRaises(TypeError, validator.is_question_input_type, None)
        self.assertRaises(TypeError, validator.is_question_input_type, 42)
        self.assertRaises(TypeError, validator.is_question_input_type, [])
        self.assertRaises(TypeError, validator.is_question_input_type, {})
        self.assertFalse(validator.is_question_input_type("")[0], "Empty string")
        self.assertFalse(validator.is_question_input_type("audio")[0], "Unrecognized type")
        self.assertFalse(validator.is_question_input_type("dattetime")[0], "Typo for the date/time input")

    def test_valid_polar_inputs(self):
        self.assertTrue(validator.is_question_input({"type": "polar"})[0], "Polar input")

    def test_valid_dropdown_list_inputs(self):
        self.assertRaises(NotImplementedError, validator.is_question_input, {"type": "dropdown-list"})

    def test_illegal_dropdown_list_inputs(self):
        pass

    def test_valid_multiple_choice_inputs(self):
        self.assertRaises(NotImplementedError, validator.is_question_input, {"type": "multiple-choice"})

    def test_illegal_multiple_choice_inputs(self):
        pass

    def test_valid_text_inputs(self):
        self.assertRaises(NotImplementedError, validator.is_question_input, {"type": "text"})

    def test_illegal_text_inputs(self):
        pass

    def test_valid_number_inputs(self):
        self.assertRaises(NotImplementedError, validator.is_question_input, {"type": "number"})

    def test_illegal_number_inputs(self):
        pass

    def test_valid_datetime_inputs(self):
        self.assertRaises(NotImplementedError, validator.is_question_input, {"type": "datetime"})

    def test_illegal_datetime_inputs(self):
        pass

    def test_valid_url_inputs(self):
        self.assertRaises(NotImplementedError, validator.is_question_input, {"type": "url"})

    def test_illegal_url_inputs(self):
        pass

    def test_valid_geotagging_inputs(self):
        self.assertTrue(validator.is_question_input({"type": "geotagging"})[0], "Geotagging input")
        self.assertTrue(validator.is_question_input({
            "type": "geotagging",
            "location": None
        })[0], "Geotagging input with explicitly unspecified location")
        self.assertTrue(validator.is_question_input({
            "type": "geotagging",
            "location": "Geneva"
        })[0], "Geotagging input with location")

    def test_illegal_geotagging_inputs(self):
        self.assertFalse(validator.is_question_input({
            "type": "geotagging",
            "location": ""
        })[0], "Geotagging input with empty location value")
        self.assertFalse(validator.is_question_input({
            "type": "geotagging",
            "location": 42
        })[0], "Geotagging input with invalid location value type (numerical value)")
        self.assertFalse(validator.is_question_input({
            "type": "geotagging",
            "location": ["Geneva"]
        })[0], "Geotagging input with invalid location value type (list)")
        self.assertFalse(validator.is_question_input({
            "type": "geotagging",
            "location": {}
        })[0], "Geotagging input with invalid location value type (dictionary)")
