# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project validator tool.
# It contains validators for various components of a question configuration.
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
from helper import check_arg_type, is_empty_string, is_configuration_string

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
    check_arg_type(is_question, "question", question, dict)
    check_arg_type(is_question, "available_languages", available_languages, (list, type(None)))

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


def __is_key(key):
    """Validates the specified key.

    A key is a non-empty string that is strictly composed of alphanumeric
    characters (a-Z, A-Z, 0-9), hyphens (-) or underscores (_).

    Args:
        key (str): A key to validate.

    Returns:
        bool: True if the specified key is valid, False otherwise.

    Raises:
        TypeError: If the key argument is not a string.
    """
    if is_empty_string(key):
        return False
    else:
        from re import match
        matches = match("[a-zA-Z0-9-_]+", key)
        return matches and matches.group() == key


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
    if not __is_key(key) or key[0] == '_':
        return (False, "A question key must be a non-empty string strictly composed of alphanumeric characters (a-z, A-Z, 0-9), hyphens (-) or underscores (_). It must never begin with an underscore.")

    return (True, None)


def is_reserved_key(key):
    """Validates the specified reserved question key.

    A key is a non-empty string that is strictly composed of alphanumeric
    characters (a-Z, A-Z, 0-9), hyphens (-) or underscores (_). A key reserved for
    internal use is almost identical to a regular question key with one slight
    difference: it must always begin with an underscore.

    Args:
        key (str): A reserved key to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified key is valid,
            False otherwise; as well as an error message in case validation fails.

    Raises:
        TypeError: If the key argument is not a string.
    """
    if not __is_key(key) or key[0] != '_':
        return (False, "A reserved key must be a non-empty string strictly composed of alphanumeric characters (a-z, A-Z, 0-9), hyphens (-) or underscores (_). It must always begin with an underscore.")

    return (True, None)


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
    if not is_configuration_string(question_title, languages):
        return (False, "A question title must be a non-empty or normalized string.")

    return (True, None)


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
    if not is_configuration_string(question_help, languages):
        return (False, "A question help field must be a non-empty or normalized string.")

    return (True, None)


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
    check_arg_type(is_question_branch, "question_branch", question_branch, (basestring, dict))

    if isinstance(question_branch, basestring):
        if not __is_key(question_branch):
            return (False, "A question branch string must be a valid key, reserved or otherwise.")
    elif isinstance(question_branch, dict):
        if question_branch:
            if any(not __is_key(key) for key in question_branch.itervalues()):
                return (False, "A question branch string must be a valid key, reserved or otherwise.")
        else:
            return (False, "A question branch dictionary must contain at least one answer-key pair.")

    return (True, None)


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
    "multiple-option",
    "text",
    "number",
    "datetime",
    "url",
    "geotagging",
])
"""A collection of question input types."""


def __is_polar_input(question_input, _):
    """Validates the specified polar input configuration.

    A polar input configuration is a non-empty dictionary that contains the 'type' field.
    Since the type field is validated prior to this function being called (see
    is_question_input), this function always returns <True, None>.

    Args:
        question_input (dict): An input configuration to validate.

    Returns:
        <True, None>: A pair containing the value True, and no error message.
    """
    return (True, None)


__is_polar_input.FIELDS = frozenset([
    "type",
])
"""A collection of polar input configuration fields."""


def __is_dropdown_list_input(question_input, languages=None):
    raise NotImplementedError()


def __is_multiple_option_input(question_input, languages=None):
    for key in ["enable-multiple-choices", "enable-other-option", "enable-illustrations"]:
        field = question_input.get(key)
        if field is not None and not isinstance(field, bool):
            return (False, "The '{}' field must be a boolean value.".format(key))

    options = question_input.get("options")
    if options is not None:
        enable_illustrations = question_input.get("enable-illustrations", False)
        if not isinstance(options, list) or len(options) < 1:
            return (False, "The 'options' field must be a non-empty list.")
        else:
            for option in options:
                label = option.get("label")
                error = (False, "An option label must be a non-empty or normalized string.")
                try:
                    if label is None or not is_configuration_string(label, languages):
                        return error
                except TypeError:
                    return error

                value = option.get("value")
                if value is None or not isinstance(value, basestring):
                    return (False, "An option value must be a string.")

                # If the 'enable-illustrations' flag is set to True, validate illustrations.
                illustration = option.get("illustration") if enable_illustrations else None
                if illustration is not None:
                    missing = [k for k in illustration.keys() if k not in __is_multiple_option_input.ILLUSTRATION_FIELDS or illustration[k] is None]
                    if missing:
                        missing = "', '".join(missing)
                        return (False, "The illustration is missing the following fields: '{}'.".format(missing))

                    for key in __is_multiple_option_input.ILLUSTRATION_FIELDS:
                        try:
                            field = illustration.get(key)
                            if is_empty_string(field):
                                return (False, "An illustration's '{}' field must be a non-empty string.".format(key))
                        except:
                            return (False, "An illustration's '{}' field must be a string.".format(key))
    else:
        return (False, "The 'options' field must be a non-empty list.")

    return (True, None)


__is_multiple_option_input.FIELDS = frozenset([
    "type",
    "enable-multiple-choices",
    "enable-other-option",
    "enable-illustrations",
    "options",
])
"""A collection of multiple-option input configuration fields."""


__is_multiple_option_input.ILLUSTRATION_FIELDS = frozenset([
    "image",
    "page",
    "attribution",
])
"""A collection of a multiple-option input configuration's illustration subfields."""


def __is_text_input(question_input, languages=None):
    """Validates the specified text input configuration.

    Args:
        question_input (dict): An input configuration to validate.
        languages (list): A list of languages that the normalized string dictionary must contain,
            where each item of the list is a language code.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified configuration
            is valid, False otherwise; as well as an error message in case it is invalid.
    """
    placeholder = question_input.get("placeholder")
    if placeholder is not None:
        error = (False, "A placeholder must be a non-empty or normalized string.")
        try:
            if not is_configuration_string(placeholder, languages):
                return error
        except TypeError:
            return error

    enable_long_text = question_input.get("enable-long-text")
    if enable_long_text is not None and not isinstance(enable_long_text, bool):
        return (False, "The 'enable-long-text' field must be a boolean value.")

    min_length = question_input.get("min-length")
    if min_length is not None:
        if not isinstance(min_length, int):
            return (False, "The 'min-length' field must be an integer value.")
        elif min_length < 0:
            return (False, "The 'min-length' must be a positive integer.")

    max_length = question_input.get("max-length")
    if max_length is not None:
        if not isinstance(max_length, int):
            return (False, "The 'max-length' field must be an integer value.")
        elif max_length < 0:
            return (False, "The 'min-length' must be a positive integer.")
        elif min_length is not None and max_length < min_length:
            return (False, "The 'max-length' must be greater than or equal to the 'min-length'.")

    return (True, None)


__is_text_input.FIELDS = frozenset([
    "type",
    "placeholder",
    "enable-long-text",
    "min-length",
    "max-length",
])
"""A collection of text input configuration fields."""


def __is_number_input(question_input, languages=None):
    raise NotImplementedError()


def __is_datetime_input(question_input, languages=None):
    raise NotImplementedError()


def __is_url_input(question_input, languages=None):
    raise NotImplementedError()


def __is_geotagging_input(question_input, _):
    """Validates the specified geotagging input configuration.

    A geotagging input configuration contains the following optional fields:
    - location: a string that specifies the input's initial location.

    Args:
        question_input (dict): An input configuration to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified configuration
            is valid, False otherwise; as well as an error message in case it is invalid.
    """
    location = question_input.get("location")
    if location is not None:
        message = "A geotagging input's 'location' field must be a non-empty string."
        try:
            if is_empty_string(location):
                return (False, message)
        except TypeError:
            return (False, message)

    return (True, None)


__is_geotagging_input.FIELDS = frozenset([
    "type",
    "location",
])
"""A collection of geotagging input configuration fields."""


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
    check_arg_type(is_question_input, "question_input", question_input, dict)
    check_arg_type(is_question_input, "languages", languages, (list, type(None)))

    missing_fields = [k for k in is_question_input.REQUIRED_FIELDS if k not in question_input or question_input[k] is None]
    if missing_fields:
        message = "The question input configuration is missing the following fields: '{}'."
        return (False, message.format("', '".join(missing_fields)))

    input_type = question_input["type"]
    valid, message = is_question_input_type(input_type)
    if not valid:
        return (False, message)

    fields = set(question_input.keys()) - is_question_input.REQUIRED_FIELDS
    expected_fields = is_question_input.EXPECTED_FIELDS.get(input_type)
    unexpected_fields = fields - expected_fields
    if unexpected_fields:
        message = "A {} configuration contains the following unexpected fields: '{}'."
        return (False, message.format(input_type, "', '".join(unexpected_fields)))

    validator = is_question_input.VALIDATORS.get(input_type)
    if not validator:
        return (False, "The question input type '{}' is not recognized.".format(input_type))

    return validator(question_input, languages)


is_question_input.REQUIRED_FIELDS = frozenset([
    "type",
])
"""A collection of required question input fields."""


is_question_input.EXPECTED_FIELDS = {
    "polar": frozenset(["type"]),
    "dropdown-list": frozenset([
        "options",
        "prompt",
        "size",
    ]),
    "multiple-option": frozenset([
        "options",
        "enable-multiple-choices",
        "enable-other-option",
        "enable-illustrations",
        "size",
    ]),
    "text": frozenset([
        "enable-long-text",
        "min-length",
        "max-length",
        "placeholder",
    ]),
    "number": frozenset([
        "min-value",
        "max-value",
        "placeholder",
    ]),
    "datetime": frozenset([
        "date-format",
        "time-format",
        "from",
        "to",
        "disable-date",
        "disable-time",
    ]),
    "url": frozenset([
        "max-length",
        "domain",
        "placeholder",
    ]),
    "geotagging": frozenset([
        "location",
    ]),
}
"""A collection of expected fields for each question input."""


is_question_input.VALIDATORS = {
    "polar": __is_polar_input,
    "dropdown-list": __is_dropdown_list_input,
    "multiple-option": __is_multiple_option_input,
    "text": __is_text_input,
    "number": __is_number_input,
    "datetime": __is_datetime_input,
    "url": __is_url_input,
    "geotagging": __is_geotagging_input,
}
"""A collection of question input validators."""
