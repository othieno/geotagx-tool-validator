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
from helper import check_arg_type, is_configuration, is_empty_string, is_configuration_string

def is_tutorial_configuration(
    configuration,
    task_presenter_configuration,
    enable_logging=False,
    validate_task_presenter_configuration=True
):
    """Validates the specified tutorial configuration.

    Args:
        configuration (dict): A tutorial configuration to validate.
        task_presenter_configuration (dict): The task presenter configuration complemented by the tutorial configuration.
        validate_task_presenter_configuration (bool): If set to True, the specified task presenter configuration is validated too.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified configuration
            is valid, False otherwise; and an error message in case the configuration is invalid.

    Raises:
        TypeError: If either of the configuration arguments is not a dictionary, or the
            remaining arguments are not booleans.
    """
    check_arg_type(is_tutorial_configuration, "task_presenter_configuration", task_presenter_configuration, dict)
    check_arg_type(is_tutorial_configuration, "validate_task_presenter_configuration", validate_task_presenter_configuration, bool)

    if validate_task_presenter_configuration:
        from task_presenter import is_task_presenter_configuration
        valid, message = is_task_presenter_configuration(task_presenter_configuration)
        if not valid:
            return (False, message)

    def is_default_message(message):
        return is_tutorial_default_message(message, task_presenter_configuration["language"]["available"])

    def are_subjects(subjects):
        check_arg_type(are_subjects, "subjects", subjects, list)
        if not subjects:
            return (False, "A project tutorial must contain at least one subject.")
        for subject in subjects:
            valid, message = is_tutorial_subject(subject, task_presenter_configuration["language"]["available"])
            if not valid:
                return (False, message)
        return (True, None)

    return is_configuration(
        configuration,
        required_fields=frozenset(["subjects"]),
        field_validators={
            "enable-random-order": is_tutorial_enable_random_order,
            "default-message": is_default_message,
            "subjects": are_subjects,
        },
        missing_field_message="The tutorial configuration is missing the following field(s): '{}'.",
        unexpected_field_message="The tutorial configuration key '{}' is not recognized."
    )


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

    unexpected_fields = set(default_message.keys()) - is_tutorial_configuration.DEFAULT_MESSAGE_FIELDS
    if unexpected_fields:
        message = "The tutorial's 'default-message' contains the following unexpected fields: '{}'."
        return (False, message.format("', '".join(unexpected_fields)))

    for key, message in default_message.iteritems():
        if not is_configuration_string(message, languages):
            return (False, "The tutorial's default message field '{}' is invalid. A message must be a non-empty or normalized string.".format(key))

    return (True, None)


is_tutorial_configuration.DEFAULT_MESSAGE_FIELDS = frozenset([
    "on-wrong-answer",
    "on-correct-answer",
])
"""A set of default message fields."""


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
    check_arg_type(is_tutorial_subject, "languages", languages, (list, type(None)))

    def is_source(subject_source):
        message = "A tutorial subject's 'source' field must be a non-empty string."
        return (False, message) if is_empty_string(subject_source) else (True, None)

    def is_page(subject_page):
        message = "A tutorial subject's 'page' field must be a non-empty string."
        return (False, message) if is_empty_string(subject_page) else (True, None)

    def is_attribution(subject_attribution):
        message = "A tutorial subject's 'attribution' field must be a non-empty string."
        return (False, message) if is_empty_string(subject_attribution) else (True, None)

    def are_subject_assertions(subject_assertions):
        check_arg_type(are_subject_assertions, "subject_assertions", subject_assertions, dict)
        from question import is_question_key
        for key, assertion in subject_assertions.iteritems():
            valid, message = is_question_key(key)
            if not valid:
                return (False, message)
            valid, message = is_tutorial_subject_assertion(assertion, languages)
            if not valid:
                return (False, message)
        return (True, None)

    return is_configuration(
        tutorial_subject,
        required_fields=frozenset(["source", "page", "assertions"]),
        field_validators={
            "source": is_source,
            "page": is_page,
            "attribution": is_attribution,
            "assertions": are_subject_assertions,
        },
        missing_field_message="The tutorial's subject configuration is missing the following field(s): '{}'.",
        unexpected_field_message="The tutorial's subject configuration key '{}' is not recognized."
    )


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
    check_arg_type(is_tutorial_subject_assertion, "languages", languages, (list, type(None)))

    def is_expects(assertion_expects):
        message = "A tutorial subject assertion's 'expects' field must be a non-empty string."
        return (False, message) if is_empty_string(assertion_expects) else (True, None)

    def is_messages(assertion_messages):
        check_arg_type(is_messages, "assertion_messages", assertion_messages, dict)
        if any(not is_configuration_string(m, languages) for m in assertion_messages.itervalues()):
            return (False, "A tutorial subject assertion message must be a non-empty or normalized string.")
        return (True, None)

    def is_autocomplete(assertion_autocomplete):
        message = "A tutorial subject assertion's 'autocomplete' field must contain a boolean value."
        return (True, None) if isinstance(assertion_autocomplete, bool) else (False, message)

    return is_configuration(
        tutorial_subject_assertion,
        required_fields=frozenset(["expects"]),
        field_validators={
            "expects": is_expects,
            "messages": is_messages,
            "autocomplete": is_autocomplete,
        },
        missing_field_message="A tutorial subject assertion configuration is missing the following field(s): '{}'.",
        unexpected_field_message="The tutorial subject assertion configuration key '{}' is not recognized."
    )
