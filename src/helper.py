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


def is_language_code(code):
    """Validates the specified language code.

    A language code is a non-empty string containing two or three lowercase letters. It may
    be extended with one of the following variety codes:
    - an ISO 3166-1 alpha-2 code to denote the region in which the language is spoken,
    - an ISO 15924 code which represents the name of the language's writing system (script).

    A variety code must always be preceded by a hyphen (-) e.g. en-GB, zh-Hans, az-Latn or fr-CH.

    Args:
        code (str): A language code to validate.

    Returns:
        bool: True if the specified code is a valid language code, False otherwise.
    """
    try:
        if is_empty_string(code):
            return False
        elif code in is_language_code.KNOWN_LANGUAGE_CODES:
            return True
        else:
            from re import match
            matches = match(r"([a-z]{2,3})(-[a-zA-Z]{2,4})?", code)
            if matches and matches.group() == code:
                valid = True
                variety = matches.group(2)
                if variety:
                    variety = variety[1:] # Skip the hyphen separator.
                    valid = is_iso_3166_1_alpha_2_code(variety) or is_iso_15924_code(variety)

                if valid:
                    is_language_code.KNOWN_LANGUAGE_CODES.add(code)

                return valid
            else:
                return False
    except TypeError:
        # The is_empty_string function will raise a TypeError if the code argument is not a
        # string. So if the argument is not a string, it stands to reason that it's not a
        # valid ISO code.
        return False

is_language_code.KNOWN_LANGUAGE_CODES = set()
"""A cache used by the is_language_code function to store and quickly retrieve verified language codes."""


def is_normalized_string(normalized_string, language_codes=None):
    """Checks if the specified string is normalized.

    A normalized string is not a true string but rather a non-empty dictionary where each key is a
    language code that is mapped to a non-empty string.

    Args:
        normalized_string (dict): A normalized string to validate.
        language_codes (list): A list of language codes that the normalized string dictionary must contain.
            If unspecified, the function only verifies that the dictionary keys are indeed valid language codes.

    Returns:
        bool: True if the specified string is normalized, False otherwise.

    Raises:
        TypeError: If the normalized_string argument is not a dictionary or if the language_codes argument is
            not a list or a NoneType.
    """
    if not isinstance(normalized_string, dict):
        raise TypeError("Invalid argument type: is_normalized_string expects 'dict' for normalized_string argument but got '%s'.".format(type(normalized_string).__name__))

    if language_codes is not None and not isinstance(language_codes, list):
        raise TypeError("Invalid argument type: is_normalized_string expects 'list' for language_codes argument but got '%s'.".format(type(language_codes).__name__))

    try:
        return normalized_string and \
               (True if language_codes is None else all(l in normalized_string for l in language_codes)) and \
               all(is_language_code(k) and not is_empty_string(v) for k, v in normalized_string.iteritems())
    except TypeError:
        # The is_empty_string function will raise a TypeError if the code argument is not a
        # string. So if the argument is not a string, it stands to reason that it's not a
        # valid ISO code.
        return False
