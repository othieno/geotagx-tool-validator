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

def is_key(key):
    """Validates the specified question key.

    A key is a non-empty string that is strictly composed of alphanumeric
    characters (a-Z, A-Z, 0-9), hyphens (-) or underscores (_). It must also
    not begin with an underscore as those are keys reserved for internal use.

    Args:
        key (str): A question key to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified question key
            is valid, False otherwise; as well as an error message in case validation fails.
    """
    try:
        ERROR_MESSAGE = "A question key must be a non-empty string strictly composed of alphanumeric characters (a-z, A-Z, 0-9), hyphens (-) or underscores (_). It must never begin with an underscore."
        if is_empty_string(key):
            return (False, ERROR_MESSAGE)
        else:
            from re import match
            matches = match("(?!_)[a-zA-Z0-9-_]+", key)
            valid = matches and matches.group() == key
            return (True, None) if valid else (False, ERROR_MESSAGE)
    except TypeError:
        return (False, "The key argument must be a non-empty string.")


def is_reserved_key(key):
    """Validates the specified reserved question key.

    A key is a non-empty string that is strictly composed of alphanumeric
    characters (a-Z, A-Z, 0-9), hyphens (-) or underscores (_). A reserved key
    is almost identical to a regular question key with one slight difference: it
    must always begin with an underscore.

    Args:
        key (str): A reserved key to validate.

    Returns:
        bool: True if the specified key is valid and reserved for internal use,
        False otherwise.
    """
    try:
        ERROR_MESSAGE = "A reserved key must be a non-empty string strictly composed of alphanumeric characters (a-z, A-Z, 0-9), hyphens (-) or underscores (_). It must always begin with an underscore."
        if is_empty_string(key):
            return (False, ERROR_MESSAGE)
        else:
            from re import match
            matches = match("_+[a-zA-Z0-9-_]+", key)
            valid = matches and matches.group() == key
            return (True, None) if valid else (False, ERROR_MESSAGE)
    except TypeError:
        return (False, "The key argument must be a non-empty string.")


def is_title(question_title, available_languages=None): # pragma: no cover
    raise NotImplementedError()


def is_help(question_help, available_languages=None): # pragma: no cover
    raise NotImplementedError()


def is_input(question_input, available_languages=None): # pragma: no cover
    raise NotImplementedError()


def is_control_flow(question_branch): # pragma: no cover
    raise NotImplementedError()


def is_question(question, available_languages=None):
    """Validates the specified question configuration.

    A valid question configuration is comprised of the following fields:
    - key: the question's unique identifier,
    - title: the question's title,
    - hint (optional): a short hint that may help clarify the question,
    - help (optional): a longer, more elaborate explanation of the question,
    - input: a configuration for the question's input,
    - branch (optional): a configuration that determines the next question depending on
      the answer to the this question.

    Args:
        question (dict): A question configuration to validate.
        available_languages (list): A list of available languages.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified configuration
            is valid, False otherwise; as well as an error message in case it is invalid.
    """
    if not isinstance(question, dict) or not question:
        return (False, "The question argument must be a non-empty dictionary.")

    from functools import partial
    VALIDATORS = {
        "key": is_key,
        "title": partial(is_title, available_languages=available_languages),
        "hint": partial(is_help, available_languages=available_languages),
        "help": partial(is_help, available_languages=available_languages),
        "input": partial(is_input, available_languages=available_languages),
        "branch": is_control_flow,
    }

    for key in VALIDATORS.keys():
        field = question.get(key)
        if field is None and key in is_question.REQUIRED_FIELD_KEYS:
            return (False, "The question configuration must contain the '{}' field.".format(key))
        elif field:
            validator = VALIDATORS[key]
            valid, message = validator(field)
            if not valid:
                return (False, message)

    return (True, None)


is_question.REQUIRED_FIELD_KEYS = frozenset(["key", "title", "input"])
"""A set of required question fields."""
