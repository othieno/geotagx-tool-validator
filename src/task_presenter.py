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
from helper import check_arg_type, is_language_code, is_empty_string

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
    check_arg_type(is_task_presenter_configuration, "configuration", configuration, dict)
    check_arg_type(is_task_presenter_configuration, "enable_logging", enable_logging, bool)

    missing = [k for k in is_task_presenter_configuration.REQUIRED_FIELDS if k not in configuration]
    if missing:
        message = "The task presenter configuration is missing the following fields: '{}'."
        return (False, message.format("', '".join(missing)))

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


is_task_presenter_configuration.REQUIRED_FIELDS = frozenset([
    "questionnaire"
])
"""A set of required task presenter configuration fields."""


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

    Raises:
        TypeError: If the 'language' argument is not a dictionary.
    """
    check_arg_type(is_task_presenter_language, "language", language, dict)

    missing = [k for k in is_task_presenter_language.REQUIRED_FIELDS if k not in language]
    if missing:
        message = "The task presenter's language configuration is missing the following fields: '{}'."
        return (False, message.format("', '".join(missing)))

    available_languages = language["available"]
    if not isinstance(available_languages, list) or len(available_languages) < 1:
        return (False, "The list of available languages must be a non-empty list of language codes.")

    invalid_language_codes = [l for l in available_languages if not is_language_code(l)]
    if invalid_language_codes:
        message = "The task presenter's list of available languages contains the following invalid codes: '{}'."
        return (False, message.format("', '".join(invalid_language_codes)))

    default_language = language["default"]
    if default_language not in available_languages:
        message = "The task presenter's default language '{}' is not listed as an available language."
        return (False, message.format(default_language))

    return (True, None)


is_task_presenter_language.REQUIRED_FIELDS = frozenset([
    "default",
    "available",
])
"""A set of required language configuration fields."""


def is_task_presenter_subject(subject):
    """Validates the specified subject configuration.

    A valid subject configuration is comprised of the following fields:
    - type: a string denoting the subject type.

    Args:
        subject (dict): A task presenter subject configuration to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified configuration
            is valid, False otherwise; as well as an error message in case it is invalid.

    Raises:
        TypeError: If the 'subject' argument is not a dictionary.
    """
    check_arg_type(is_task_presenter_subject, "subject", subject, dict)

    missing = [k for k in is_task_presenter_subject.REQUIRED_FIELDS if k not in subject]
    if missing:
        message = "The task presenter's subject configuration is missing the following fields: '{}'."
        return (False, message.format("', '".join(missing)))

    validators = {
        "type": is_subject_type,
    }
    for key, configuration in subject.iteritems():
        validator = validators.get(key)
        if not validator:
            return (False, "The task presenter subject configuration key '{}' is not recognized.".format(key))

        valid, message = validator(configuration)
        if not valid:
            return (False, message)

    return (True, None)


is_task_presenter_subject.REQUIRED_FIELDS = frozenset([
    "type",
])
"""A set of required subject configuration fields."""


def is_task_presenter_questionnaire(questionnaire, languages=None):
    """Validates the specified questionnaire configuration.

    A valid questionnanire configuration is comprised of the following fields:
    - questions: a list of question configurations.

    Args:
        questionnanire (dict): A task presenter questionnanire configuration to validate.
        languages (list): A list of available languages.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified configuration
            is valid, False otherwise; as well as an error message in case it is invalid.

    Raises:
        TypeError: If the questionnaire argument is not a dictionary or languages
        is not a list or NoneType.
    """
    check_arg_type(is_task_presenter_questionnaire, "questionnaire", questionnaire, dict)
    check_arg_type(is_task_presenter_questionnaire, "languages", languages, (list, type(None)))

    missing = [k for k in ["questions"] if k not in questionnaire]
    if missing:
        message = "The task presenter's questionnaire configuration is missing the following fields: '{}'."
        return (False, message.format("', '".join(missing)))

    questions = questionnaire["questions"]
    if not isinstance(questions, list) or len(questions) < 1:
        return (False, "A questionnaire must have a non-empty list of questions.")
    else:
        from question import is_question
        for q in questions:
            valid, message = is_question(q, languages)
            if not valid:
                return (False, message)

    return (True, None)


def is_subject_type(subject_type):
    """Validates the specified subject type.

    Args:
        subject_type (str): A subject type to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified subject type
            is valid, False otherwise; as well as an error message in case it is invalid.

    Raises:
        TypeError: If the 'subject_type' argument is not a string.
    """
    if is_empty_string(subject_type):
        return (False, "A subject type must be a non-empty string.")
    elif subject_type not in is_subject_type.SUPPORTED_TYPES:
        return (False, "The subject type '{}' is not recognized.".format(subject_type))

    return (True, None)


is_subject_type.SUPPORTED_TYPES = frozenset([
    "image",
    "pdf",
])
"""A collection of supported subject types."""
