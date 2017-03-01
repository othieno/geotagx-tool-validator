# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project validator tool.
# It contains validators for various components of a task presenter configuration.
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
def is_task_presenter_configuration(configuration, enable_logging=False):
    """Validates the specified task presenter configuration.

    Args:
        configuration (dict): A task presenter configuration to validate.
        enable_logging (bool): If set to True, the function will log the operations it performs.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified configuration
            is valid, False otherwise; and an error message in case the name is invalid.

    Raises:
        TypeError: If the configuration argument is not a dictionary or enable_logging is not a boolean.
    """
    if not isinstance(configuration, dict):
        raise TypeError("Invalid argument type: is_task_presenter_configuration expects 'dict' for the configuration argument but got '{}'.".format(type(configuration).__name__))
    elif not isinstance(enable_logging, bool):
        raise TypeError("Invalid argument type: is_task_presenter_configuration expects 'bool' for the enable_logging argument but got '{}'.".format(type(enable_logging).__name__))

    missing = [k for k in ["questionnaire"] if k not in configuration]
    if missing:
        return (False, "The task presenter configuration is missing the following fields: '{}'.".format("', '".join(missing)))

    validators = {
        "language": is_task_presenter_language,
        "subject": is_task_presenter_subject,
        "questionnaire": is_task_presenter_questionnaire,
    }
    for key, configuration in configuration.iteritems():
        validator = validators.get(key)
        if not validator:
            return (False, "The task presenter configuration key '{}' is not recognized.".format(key))

        valid, message = validator(configuration)
        if not valid:
            return (False, message)

    return (True, None)


def is_task_presenter_language(language):
    """Validates the specified language configuration.

    A valid language configuration is comprised of the following fields:
    - available: a list of available languages where each language is identified by a code,
    - default: a task presenter's default language, also identified by a unique code. The
      default language must also be a member of the list of available languages.

    Args:
        language (dict): A task presenter language configuration to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified configuration
            valid, False otherwise; as well as an error message in case it is invalid.
    """
    raise NotImplementedError()


def is_task_presenter_subject(subject):
    """Validates the specified subject configuration.

    A valid subject configuration is comprised of the following fields:
    - type: a string denoting the subject type.

    Args:
        subject (dict): A task presenter subject configuration to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified configuration
            is valid, False otherwise; as well as an error message in case it is invalid.
    """
    raise NotImplementedError()


def is_task_presenter_questionnaire(questionnaire, available_languages=None):
    """Validates the specified questionnaire configuration.

    A valid questionnanire configuration is comprised of the following fields:
    - questions: a list of question configurations.

    Args:
        questionnanire (dict): A task presenter questionnanire configuration to validate.
        available_languages (list): A list of available languages.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified configuration
            is valid, False otherwise; as well as an error message in case it is invalid.

    Raises:
        TypeError: If the 'available_languages' argument is not a list.
    """
    raise NotImplementedError()
