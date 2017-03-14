# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project validator tool.
# It contains validators for various components of a tutorial configuration.
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
from helper import is_configuration_string, find_unexpected_keys

def is_tutorial_configuration(
    tutorial_configuration,
    task_presenter_configuration,
    enable_logging=False,
    validate_task_presenter_configuration=True
):
    """Validates the specified tutorial configuration.

    Args:
        tutorial_configuration (dict): A tutorial configuration to validate.
        task_presenter_configuration (dict): The task presenter configuration complemented by the tutorial configuration.
        enable_logging (bool): If set to True, the function will log the operations it performs.
        validate_task_presenter_configuration (bool): If set to True, the specified task presenter configuration is validated too.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified configuration
            is valid, False otherwise; and an error message in case the configuration is invalid.

    Raises:
        TypeError: If either of the configuration arguments is not a dictionary, or the
            remaining arguments are not booleans.
    """
    if not isinstance(tutorial_configuration, dict):
        raise TypeError("Invalid argument type: is_tutorial_configuration expects 'dict' for the tutorial_configuration argument but got '{}'.".format(type(tutorial_configuration).__name__))
    elif not isinstance(task_presenter_configuration, dict):
        raise TypeError("Invalid argument type: is_tutorial_configuration expects 'dict' for the task_presenter_configuration argument but got '{}'.".format(type(task_presenter_configuration).__name__))
    elif not isinstance(enable_logging, bool):
        raise TypeError("Invalid argument type: is_tutorial_configuration expects 'bool' for the enable_logging argument but got '{}'.".format(type(enable_logging).__name__))
    elif not isinstance(validate_task_presenter_configuration, bool):
        raise TypeError("Invalid argument type: is_tutorial_configuration expects 'bool' for the validate_task_presenter_configuration argument but got '{}'.".format(type(validate_task_presenter_configuration).__name__))

    if validate_task_presenter_configuration:
        from task_presenter import is_task_presenter_configuration
        valid, message = is_task_presenter_configuration(task_presenter_configuration)
        if not valid:
            return (False, message)

    missing = [k for k in is_tutorial_configuration.REQUIRED_FIELDS if k not in tutorial_configuration]
    if missing:
        return (False, "The tutorial configuration is missing the following fields: '{}'.".format("', '".join(missing)))

    available_languages = task_presenter_configuration["language"]["available"] if "language" in task_presenter_configuration else None

    from functools import partial
    validators = {
        "enable-random-order": is_tutorial_enable_random_order,
        "default-message": partial(is_tutorial_default_message, languages=available_languages),
        "subjects": is_tutorial_subjects,
    }
    for key, configuration in tutorial_configuration.iteritems():
        validator = validators.get(key)
        if not validator:
            return (False, "The tutorial configuration key '{}' is not recognized.".format(key))

        valid, message = validator(configuration)
        if not valid:
            return (False, message)

    return (True, None)


is_tutorial_configuration.REQUIRED_FIELDS = frozenset([
    "subjects",
])
"""A set of required tutorial configuration fields."""


def is_tutorial_enable_random_order(enable_random_order):
    """Validates the specified 'Enable random order' flag.

    Args:
        enable_random_order (bool): A flag to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified flag
            is valid, False otherwise; and an error message in case the flag is invalid.
    """
    error_message = "The 'enable-random-order' argument must be a boolean."
    return (True, None) if isinstance(enable_random_order, bool) else (False, error_message)


def is_tutorial_default_message(default_message, languages=None):
    """Validates the specified set of default messages.

    Args:
        default_message (dict): A set of default messages.
        languages (list): A list of available languages.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified message set
            is valid, False otherwise; and an error message in case the set is invalid.
    Raises:
        TypeError: If the default_message argument is not a dictionary, or if the
            languages argument is not a list or NoneType.
    """
    if not isinstance(default_message, dict):
        raise TypeError("Invalid argument type: is_tutorial_default_message expects 'dict' for the default_message argument but got '{}'.".format(type(default_message).__name__))
    elif languages is not None and not isinstance(languages, list):
        raise TypeError("Invalid argument type: is_tutorial_default_message expects 'list' for the languages argument but got '{}'.".format(type(languages).__name__))

    unexpected_keys = find_unexpected_keys(default_message, is_tutorial_configuration.DEFAULT_MESSAGE_FIELDS)
    if unexpected_keys:
        message = "The tutorial's 'default-message' contains the following unrecognized fields: '{}'."
        return (False, message.format("', '".join(unexpected_keys)))

    for key, message in default_message.iteritems():
        if not is_configuration_string(message, languages):
            return (False, "The tutorial's default message field '{}' is invalid. A message must be a non-empty or normalized string.".format(key))

    return (True, None)


is_tutorial_configuration.DEFAULT_MESSAGE_FIELDS = frozenset([
    "on-wrong-answer",
    "on-correct-answer",
])
"""A set of default message fields."""


def is_tutorial_subjects(tutorial_subjects):
    raise NotImplementedError
