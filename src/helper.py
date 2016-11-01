# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project validator tool.
# It contains miscellaneous helper functions.
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
def is_empty_string(empty_string):
    """Checks if the specified string is empty.

    A string is considered empty if it does not contain characters other than
    whitespace or escape sequences.

    Args:
        empty_string (basestring): An empty string to check.

    Returns:
        bool: True if the specified string is empty, False otherwise.

    Raises:
        TypeError: If the empty_string argument is not a string.
    """
    if not isinstance(empty_string, basestring):
        raise TypeError("Invalid argument type: is_empty_string expects 'basestring' but got '{}'.".format(type(empty_string).__name__))

    return not empty_string or empty_string.isspace()


def is_iso_3166_1_alpha_2_code(code):
    """Validates the specified ISO 3166-1 alpha-2 code.

    An ISO 3166-1 alpha-2 code is a two-letter uppercase string assigned to a region,
    e.g. GB (United Kingdom), US (United States) or CH (Switzerland).

    Args:
        code (str): An ISO 3166-1 alpha-2 code to validate.

    Returns:
        bool: True if the specified code is a valid ISO 3166-1 alpha-2 code, False otherwise.
    """
    try:
        if is_empty_string(code):
            return False
        else:
            # TODO Optimize this: Regular expressions are a bit of an overkill.
            from re import match
            matches = match("[A-Z]{2}", code)
            return matches and matches.group() == code
    except TypeError:
        # The is_empty_string function will raise a TypeError if the code argument is not a
        # string. So if the argument is not a string, it stands to reason that it's not a
        # valid ISO code.
        return False


def is_iso_15924_code(code):
    """Validates the specified ISO 15924 code.

    An ISO 15924 code is a four-letter capitalized string assigned to a language's writing system,
    for instance Latn (Latin), Cyrl (Cyrillic), or Arab (Arabic).

    Args:
        code (str): An ISO 15924 code to validate.

    Returns:
        bool: True if the specified code is a valid ISO 15924 code, False otherwise.
    """
    try:
        if is_empty_string(code):
            return False
        else:
            from re import match
            matches = match("[A-Z]{1}[a-z]{3}", code)
            return matches and matches.group() == code
    except TypeError:
        # The is_empty_string function will raise a TypeError if the code argument is not a
        # string. So if the argument is not a string, it stands to reason that it's not a
        # valid ISO code.
        return False
