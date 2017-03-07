# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project validator tool.
# It contains validators for various components of a question configuration.
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
from helper import is_empty_string, is_normalized_string

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

    Raises:
        TypeError: If the question argument is not a dictionary or available_languages is
        not a list or NoneType.
    """
    if not isinstance(question, dict):
        raise TypeError("Invalid argument type: is_question expects 'dict' for the question argument but got '{}'.".format(type(question).__name__))
    elif available_languages is not None and not isinstance(available_languages, list):
        raise TypeError("Invalid argument type: is_question expects 'list' for the available_languages argument but got '{}'.".format(type(available_languages).__name__))

    missing = [k for k in is_question.REQUIRED_FIELDS if k not in question or question[k] is None]
    if missing:
        message = "The question configuration is missing the following fields: '{}'."
        return (False, message.format("', '".join(missing)))

    from functools import partial
    validators = {
        "key": is_question_key,
        "title": partial(is_question_title, languages=available_languages),
        "hint": partial(is_question_help, languages=available_languages),
        "help": partial(is_question_help, languages=available_languages),
        "input": partial(is_question_input, languages=available_languages),
        "branch": is_question_branch,
    }
    for key, configuration in question.iteritems():
        validator = validators.get(key)
        if not validator:
            return (False, "The question configuration key '{}' is not recognized.".format(key))

        valid, message = validator(configuration)
        if not valid:
            return (False, message)

    return (True, None)


is_question.REQUIRED_FIELDS = frozenset([
    "key",
    "title",
    "input"
])
"""A set of required question fields."""


def is_question_key(key):
    """Validates the specified question key.

    A key is a non-empty string that is strictly composed of alphanumeric
    characters (a-Z, A-Z, 0-9), hyphens (-) or underscores (_). It must also
    not begin with an underscore as those are keys reserved for internal use.

    Args:
        key (str): A question key to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified question key
            is valid, False otherwise; as well as an error message in case validation fails.

    Raises:
        TypeError: If the key argument is not a string.
    """
    message = "A question key must be a non-empty string strictly composed of alphanumeric characters (a-z, A-Z, 0-9), hyphens (-) or underscores (_). It must never begin with an underscore."
    if is_empty_string(key):
        return (False, message)
    else:
        from re import match
        matches = match("(?!_)[a-zA-Z0-9-_]+", key)
        valid = matches and matches.group() == key
        return (True, None) if valid else (False, message)


def is_reserved_question_key(key):
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

    Raises:
        TypeError: If the key argument is not a string.
    """
    message = "A reserved key must be a non-empty string strictly composed of alphanumeric characters (a-z, A-Z, 0-9), hyphens (-) or underscores (_). It must always begin with an underscore."
    if is_empty_string(key):
        return (False, message)
    else:
        from re import match
        matches = match("_+[a-zA-Z0-9-_]+", key)
        valid = matches and matches.group() == key
        return (True, None) if valid else (False, message)


def is_question_title(question_title, languages=None):
    """Validates the specified question title.

    A title is a non-empty or normalized string.

    Args:
        title (str|dict): A title to validate.
        languages (list): A list of languages that the normalized string dictionary must contain, where each item of the
            list is a language code. Note that this parameter is used if and only if the title is a normalized string.

    Returns:
        <bool, str|None>: A pair containing the value True if the title is valid,
            False otherwise; as well as an error message in case it is invalid.

    Raises:
        TypeError: If the question_title argument is not a string or dictionary, or if
            languages is not a list or NoneType.
    """
    if isinstance(question_title, basestring):
        message = "A question title must be a non-empty string."
        return (False, message) if is_empty_string(question_title) else (True, None)
    elif isinstance(question_title, dict):
        if languages is not None and not isinstance(languages, list):
            raise TypeError("Invalid argument type: is_question_title expects 'list' or 'NoneType' for the languages argument but got '{}'.".format(type(languages).__name__))

        message = "The question title is not a valid normalized string."
        return (True, None) if is_normalized_string(question_title, languages) else (False, message)
    else:
        raise TypeError("Invalid argument type: is_question_title expects 'basestring' or 'dict' for the question_title argument but got '{}'.".format(type(question_title).__name__))


def is_question_help(question_help, languages=None):
    """Validates the specified question help.

    A help is a non-empty or normalized string.

    Args:
        help (str|dict): The help to validate.
        languages (list): A list of languages that the normalized string dictionary must contain, where each item of the
            list is a language code. Note that this parameter is used if and only if the help is a normalized string.

    Returns:
        <bool, str|None>: A pair containing the value True if the help is valid,
            False otherwise; as well as an error message in case it is invalid.

    Raises:
        TypeError: If the question_help argument is not a string or dictionary, or if
            languages is not a list or NoneType.
    """
    if isinstance(question_help, basestring):
        message = "A question help must be a non-empty string."
        return (False, message) if is_empty_string(question_help) else (True, None)
    elif isinstance(question_help, dict):
        if languages is not None and not isinstance(languages, list):
            raise TypeError("Invalid argument type: is_question_help expects 'list' or 'NoneType' for the languages argument but got '{}'.".format(type(languages).__name__))

        message = "The question help is not a valid normalized string."
        return (True, None) if is_normalized_string(question_help, languages) else (False, message)
    else:
        raise TypeError("Invalid argument type: is_question_help expects 'basestring' or 'dict' for the question_help argument but got '{}'.".format(type(question_help).__name__))


def is_question_branch(question_branch):
    """Validates the specified question branch.

    A branch is either a non-empty string which is a valid question or reserved key,
    or a dictionary where each possible question answer is mapped to a key.

    Args:
        question_branch (str|dict): A branch to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the branch is valid,
            False otherwise; as well as an error message in case it is invalid.

    Raises:
        TypeError: If the question_branch argument is not a string or dictionary.
    """
    raise NotImplementedError()


def is_question_input(question_input, languages=None):
    """Validates the specified input configuration.

    A question's input configuration is a non-empty dictionary comprised of different fields
    that define a question's input parameters.

    Args:
        question_input (dict): An input configuration to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified configuration
            is valid, False otherwise; as well as an error message in case it is invalid.

    Raises:
        TypeError: If the question_input argument is not a dictionary, or if languages
            is not a list or NoneType.
    """
    if not isinstance(question_input, dict):
        raise TypeError("Invalid argument type: is_question_input expects 'dict' for the question_input argument but got '{}'.".format(type(question_input).__name__))
    elif languages is not None and not isinstance(languages, list):
        raise TypeError("Invalid argument type: is_question_input expects 'list' or 'NoneType' for the languages argument but got '{}'.".format(type(languages).__name__))

    missing = [k for k in is_question_input.REQUIRED_FIELDS if k not in question_input or question_input[k] is None]
    if missing:
        message = "The question input configuration is missing the following fields: '{}'."
        return (False, message.format("', '".join(missing)))

    input_type = question_input["type"]
    valid, message = is_question_input_type(input_type)
    if not valid:
        return (False, message)

    # Note: the VALIDATORS dictionary is defined at the end of this module.
    validator = is_question_input.VALIDATORS.get(input_type)
    if not validator:
        return (False, "The question input type '{}' is not recognized.".format(input_type))

    return validator(question_input, languages)


is_question_input.REQUIRED_FIELDS = frozenset([
    "type",
])
"""A collection of required question input fields."""


def is_question_input_type(input_type):
    """Validates the specified question input type.

    Args:
        input_type (str): An input type to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified input type
            is valid, False otherwise; as well as an error message in case it is invalid.

    Raises:
        TypeError: If the input_type argument is not a string.
    """
    if is_empty_string(input_type):
        return (False, "An input type must be a non-empty string.")
    elif input_type not in is_question_input_type.INPUT_TYPES:
        return (False, "The input type '{}' is not recognized.".format(input_type))

    return (True, None)


is_question_input_type.INPUT_TYPES = frozenset([
    "polar",
    "dropdown-list",
    "multiple-choice",
    "text",
    "number",
    "datetime",
    "url",
    "geotagging",
])
"""A collection of question input types."""


def __is_polar_input(question_input, unused=None): # pragma: no cover
    """Validates the specified polar input configuration.

    A polar input configuration is a non-empty dictionary that contains the 'type' field.
    Since the type field is validated prior to this function being called (see
    is_question_input), this function always returns True.

    Args:
        question_input (dict): A polar input configuration to validate.

    Returns:
        <True, None>: A pair containing the value True, and no error message.
    """
    return (True, None)


is_question_input.VALIDATORS = {
    "polar": __is_polar_input,
    "dropdown-list": lambda x, y: (True, None),
    "multiple-choice": lambda x, y: (True, None),
    "text": lambda x, y: (True, None),
    "number": lambda x, y: (True, None),
    "datetime": lambda x, y: (True, None),
    "url": lambda x, y: (True, None),
    "geotagging": lambda x, y: (True, None),
}
"""A collection of question input validators."""
