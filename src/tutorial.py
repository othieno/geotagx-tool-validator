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
from helper import check_arg_type, is_empty_string, is_configuration_string, find_unexpected_keys

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
    check_arg_type(is_tutorial_configuration, "tutorial_configuration", tutorial_configuration, dict)
    check_arg_type(is_tutorial_configuration, "task_presenter_configuration", task_presenter_configuration, dict)
    check_arg_type(is_tutorial_configuration, "enable_logging", enable_logging, bool)
    check_arg_type(is_tutorial_configuration, "validate_task_presenter_configuration", validate_task_presenter_configuration, bool)

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
        "subjects": partial(__is_tutorial_subjects, languages=available_languages),
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
    check_arg_type(is_tutorial_default_message, "default_message", default_message, dict)
    check_arg_type(is_tutorial_default_message, "languages", languages, (list, type(None)))

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


def __is_tutorial_subjects(tutorial_subjects, languages=None):
    """Validates the specified list of tutorial subjects.

    Args:
        tutorial_subjects (list): A list of tutorial subjects to validate.
        languages (list): A list of available languages.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified list
            is valid, False otherwise; and an error message in case the list is invalid.

    Raises:
        TypeError: If the tutorial_subjects argument is not a list, or the languages
            argument is not a list or NoneType.
    """
    check_arg_type(__is_tutorial_subjects, "tutorial_subjects", tutorial_subjects, list)
    check_arg_type(__is_tutorial_subjects, "languages", languages, (list, type(None)))

    if not tutorial_subjects:
        return (False, "A project tutorial must contain one or more subjects.")

    for s in tutorial_subjects:
        valid, message = is_tutorial_subject(s, languages)
        if not valid:
            return (False, message)

    return (True, None)


def is_tutorial_subject(tutorial_subject, languages=None):
    """Validates the specified tutorial subject.

    Args:
        tutorial_subject (dict): A tutorial subject to validate.
        languages (list): A list of available languages.

    Returns:
        <bool, str|NoneType>: A pair containing the value True if the specified subject
            is valid, False otherwise; and an error message in case the subject is invalid.

    Raises:
        TypeError: If the tutorial_subject argument is not a dictionary, or the languages
            argument is not a list or NoneType.
    """
    check_arg_type(is_tutorial_subject, "tutorial_subject", tutorial_subject, dict)
    check_arg_type(is_tutorial_subject, "languages", languages, (list, type(None)))

    missing = [k for k in is_tutorial_subject.REQUIRED_FIELDS if k not in tutorial_subject]
    if missing:
        message = "A tutorial's subject configuration is missing the following fields: '{}'."
        return (False, message.format("', '".join(missing)))

    from functools import partial
    validators = {
        "source": is_tutorial_subject_source,
        "page": is_tutorial_subject_page,
        "assertions": partial(__is_tutorial_subject_assertions, languages=languages),
    }

    for key, field in tutorial_subject.iteritems():
        validator = validators.get(key)
        if not validator:
            return (False, "The field '{}' is not a recognized tutorial subject field.".format(key))

        valid, message = validator(field)
        if not valid:
            return (False, message)

    return (True, None)


is_tutorial_subject.REQUIRED_FIELDS = frozenset([
    "source",
    "page",
    "assertions",
])
"""A collection of required tutorial subject fields."""


def is_tutorial_subject_source(tutorial_subject_source):
    """Validates the specified tutorial subject source.

    Args:
        tutorial_subject_source (basestring): A source to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified source
            is valid, False otherwise; and an error message in case the source is invalid.

    Raises:
        TypeError: If the tutorial_subject_source argument is not a string.
    """
    message = "A tutorial subject's 'source' field must be a non-empty string."
    return (False, message) if is_empty_string(tutorial_subject_source) else (True, None)


def is_tutorial_subject_page(tutorial_subject_page):
    """Validates the specified tutorial subject page.

    Args:
        tutorial_subject_page (basestring): A page to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified page
            is valid, False otherwise; and an error message in case the page is invalid.

    Raises:
        TypeError: If the tutorial_subject_page argument is not a string.
    """
    message = "A tutorial subject's 'page' field must be a non-empty string."
    return (False, message) if is_empty_string(tutorial_subject_page) else (True, None)


def __is_tutorial_subject_assertions(tutorial_subject_assertions, languages=None):
    """Validates the specified set of tutorial subject assertions.

    Args:
        tutorial_subject_assertions (dict): A set of assertions to validate.
        languages (list): A list of available languages.

    Returns:
        <bool, str|NoneType>: A pair containing the value True if the specified set of
            assertions is valid, False otherwise; and an error message in case validation failed.

    Raises:
        TypeError: If the tutorial_subject_assertions argument is not a dictionary, or
            the languages argument is not a list or NoneType.
    """
    check_arg_type(__is_tutorial_subject_assertions, "tutorial_subject_assertions", tutorial_subject_assertions, dict)
    check_arg_type(__is_tutorial_subject_assertions, "languages", languages, (list, type(None)))

    from question import is_question_key
    for key, assertion in tutorial_subject_assertions.iteritems():
        valid, message = is_question_key(key)
        if not valid:
            return (False, message)

        valid, message = is_tutorial_subject_assertion(assertion, languages)
        if not valid:
            return (False, message)

    return (True, None)


def is_tutorial_subject_assertion(tutorial_subject_assertion, languages=None):
    """Validates the specified tutorial subject assertion.

    Args:
        tutorial_subject_assertion (dict): A subject assertion to validate.
        languages (list): A list of available languages.

    Returns:
        <bool, str|NoneType>: A pair containing the value True if the specified assertion
            is valid, False otherwise; and an error message in case validation failed.

    Raises:
        TypeError: If the tutorial_subject_assertion argument is not a dictionary, or
            the languages argument is not a list or NoneType.
    """
    check_arg_type(is_tutorial_subject_assertion, "tutorial_subject_assertion", tutorial_subject_assertion, dict)
    check_arg_type(is_tutorial_subject_assertion, "languages", languages, (list, type(None)))

    raise NotImplementedError

    return (True, None)
