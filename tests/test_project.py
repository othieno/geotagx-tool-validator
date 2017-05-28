# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project sanitizer tool.
# It contains unit tests for the project module.
#
# Author: Jeremy Othieno (j.othieno@gmail.com)
#
# Copyright (c) 2016-2017 UNITAR/UNOSAT
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
import project as validator

class TestProjectValidator(unittest.TestCase):
    def test_valid_project_configurations(self):
        self.assertTrue(validator.is_project_configuration({
            "name": "Demo",
            "short_name": "demo",
            "description": "A demo."
        })[0], "Simple project")

    def test_illegal_project_configurations(self):
        self.assertRaises(TypeError, validator.is_project_configuration, None)
        self.assertRaises(TypeError, validator.is_project_configuration, 42)
        self.assertRaises(TypeError, validator.is_project_configuration, "")
        self.assertRaises(TypeError, validator.is_project_configuration, [])
        self.assertFalse(validator.is_project_configuration({})[0], "Empty dictionary")
        self.assertFalse(validator.is_project_configuration({"name": "Demo"})[0], "Missing keys")
        self.assertFalse(validator.is_project_configuration({
            "name": "Demo",
            "short_name": 42,
            "description": "A demo."
        })[0], "Illegal short name")
        self.assertFalse(validator.is_project_configuration({
            "name": "Demo",
            "short_name": "demo",
            "description": "A demo.",
            "unknown_key": 42
        })[0], "Unknown key")

    def test_valid_project_names(self):
        self.assertTrue(validator.is_project_name("hello")[0], "Valid name")
        self.assertTrue(validator.is_project_name("hello   ")[0], "Valid name with trailing whitespace")
        self.assertTrue(validator.is_project_name("   hello")[0], "Valid name with leading whitespace")
        self.assertTrue(validator.is_project_name("   hello   ")[0], "Valid name with leading and trailing whitespace")

    def test_illegal_project_names(self):
        self.assertFalse(validator.is_project_name(None)[0], "NoneType object used as name")
        self.assertFalse(validator.is_project_name(42)[0], "Project name is a numerical value (not a string)")
        self.assertFalse(validator.is_project_name("")[0], "Empty string")
        self.assertFalse(validator.is_project_name([])[0], "Empty list used as a name")
        self.assertFalse(validator.is_project_name({})[0], "Empty dictionary used as a name")
        self.assertFalse(validator.is_project_name("   ")[0], "Whitespace only")

    def test_valid_project_short_names(self):
        self.assertTrue(validator.is_project_short_name("hello")[0], "Alphabet characters")
        self.assertTrue(validator.is_project_short_name("hello32")[0], "Alphanumeric characters")
        self.assertTrue(validator.is_project_short_name("hello-world")[0], "Hyphen-separated characters")
        self.assertTrue(validator.is_project_short_name("hello_world")[0], "Underscore-separated characters")
        self.assertTrue(validator.is_project_short_name("h")[0], "Single letter project name")
        self.assertTrue(validator.is_project_short_name("1")[0], "Single digit project name")

    def test_illegal_project_short_names(self):
        self.assertFalse(validator.is_project_short_name(None)[0], "NoneType object used as short name")
        self.assertFalse(validator.is_project_short_name(42)[0], "Numerical value used as a short name")
        self.assertFalse(validator.is_project_short_name("")[0], "Empty string")
        self.assertFalse(validator.is_project_short_name("   ")[0], "Whitespace only")
        self.assertFalse(validator.is_project_short_name("   hello")[0], "Valid short name but leading whitespace")
        self.assertFalse(validator.is_project_short_name("hello   ")[0], "Valid short name but trailing whitespace")
        self.assertFalse(validator.is_project_short_name("   hello   ")[0], "Valid short name but leading and trailing whitespace")
        self.assertFalse(validator.is_project_short_name("hello*world")[0], "Invalid character (star)")
        self.assertFalse(validator.is_project_short_name("#hello-world")[0], "Invalid character (hash)")
        self.assertFalse(validator.is_project_short_name([])[0], "Empty list used as a short name")
        self.assertFalse(validator.is_project_short_name({})[0], "Empty dictionary used as a short name")

    def test_valid_project_descriptions(self):
        self.assertTrue(validator.is_project_description("?")[0], "Description is a non-empty string")
        self.assertTrue(validator.is_project_description("   hello")[0], "Valid description with leading whitespace")
        self.assertTrue(validator.is_project_description("hello   ")[0], "Valid description with trailing whitespace")
        self.assertTrue(validator.is_project_description("   hello   ")[0], "Valid description with leading and trailing whitespace")

    def test_illegal_project_descriptions(self):
        self.assertFalse(validator.is_project_description(None)[0], "NoneType object used as description")
        self.assertFalse(validator.is_project_description(42)[0], "Project description is a numerical value")
        self.assertFalse(validator.is_project_description("")[0], "Empty string")
        self.assertFalse(validator.is_project_description("   ")[0], "Whitespace only")
        self.assertFalse(validator.is_project_description([])[0], "Project description is a list")
        self.assertFalse(validator.is_project_description({})[0], "Project description is a dictionary")

    def test_valid_project_repositories(self):
        self.assertTrue(validator.is_project_repository("https://github.com/geotagx/geotagx-project-demo.git")[0], "Github repository")

    def test_illegal_project_repositories(self):
        self.assertFalse(validator.is_project_repository(None)[0], "No value")
        self.assertFalse(validator.is_project_repository(42)[0], "Repository is a numerical value")
        self.assertFalse(validator.is_project_repository([])[0], "Repository is a list")
        self.assertFalse(validator.is_project_repository({})[0], "Repository is a dictionary")
        self.assertFalse(validator.is_project_repository("42")[0], "Repository is a not a URL")
        self.assertFalse(validator.is_project_repository("github.com/geotagx/geotagx-project-demo.git")[0], "Missing URL protocol")

    def test_valid_project_tracking(self):
        self.assertTrue(validator.is_project_do_not_track(True)[0], "Tracking disabled")
        self.assertTrue(validator.is_project_do_not_track(False)[0], "Tracking enabled")

    def test_illegal_project_tracking(self):
        self.assertFalse(validator.is_project_do_not_track(None)[0], "No value")
        self.assertFalse(validator.is_project_do_not_track(42)[0], "Tracking boolean is a numerical value")
        self.assertFalse(validator.is_project_do_not_track("")[0], "Tracking boolean is a string")
        self.assertFalse(validator.is_project_do_not_track([])[0], "Tracking boolean is a list")
        self.assertFalse(validator.is_project_do_not_track({})[0], "Tracking boolean is a dictionary")


if __name__ == "__main__":
    unittest.main()
