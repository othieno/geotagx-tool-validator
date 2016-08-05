# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project sanitizer tool.
# It contains validators for various components of a question sub-configuration.
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
from helper import is_empty_string

def is_question(question): # pragma: no cover
    raise NotImplementedError()


def is_question_key(question_key):
    """Validates the specified question key.

    A key is a non-empty string that is strictly composed of alphanumeric
    characters (a-Z, A-Z, 0-9), hyphens (-) or underscores (_). It must also
    not begin with an underscore as those are keys reserved for internal use.

    Args:
        question_key (str): A question key to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified question key
            is valid, False otherwise; as well as an error message in case validation fails.
    """
    try:
        ERROR_MESSAGE = "A question key must be a non-empty string strictly composed of alphanumeric characters (a-z, A-Z, 0-9), hyphens (-) or underscores (_). It must never begin with an underscore."
        if is_empty_string(question_key):
            return (False, ERROR_MESSAGE)
        else:
            from re import match
            matches = match("(?!_)[a-zA-Z0-9-_]+", question_key)
            valid = matches and matches.group() == question_key
            return (True, None) if valid else (False, ERROR_MESSAGE)
    except TypeError:
        return (False, "The 'question_key' argument must be a non-empty string.")


def is_question_title(question_title): # pragma: no cover
    raise NotImplementedError()


def is_question_help(question_help): # pragma: no cover
    raise NotImplementedError()


def is_question_input(question_input): # pragma: no cover
    raise NotImplementedError()


def is_question_branch(question_branch): # pragma: no cover
    raise NotImplementedError()
