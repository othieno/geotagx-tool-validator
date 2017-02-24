# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project validator tool.
# It contains validators for various components of a project configuration.
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
from helper import is_empty_string, is_url

def is_project_configuration(configuration, enable_logging=False):
    """Validates the specified project configuration.

    Args:
        configuration (dict): A project configuration to validate.
        enable_logging (bool): If set to True, the function will log the operations it performs.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified configuration
            is valid, False otherwise; and an error message in case the name is invalid.

    Raises:
        TypeError: If the configuration argument is not a dictionary or enable_logging is not a boolean.
    """
    if not isinstance(configuration, dict):
        raise TypeError("Invalid argument type: is_project_configuration expects 'dict' for the configuration argument but got '{}'.".format(type(configuration).__name__))
    elif not isinstance(enable_logging, bool):
        raise TypeError("Invalid argument type: is_project_configuration expects 'bool' for the enable_logging argument but got '{}'.".format(type(enable_logging).__name__))
    elif not all(key in configuration for key in ["name", "short_name", "description"]):
        raise ValueError("A required configuration is missing from the specified configuration set.")

    validators = {
        "name": is_project_name,
        "short_name": is_project_short_name,
        "description": is_project_description,
        "repository": is_project_repository,
        "do_not_track": is_project_do_not_track,
    }
    for key, configuration in configuration.iteritems():
        validator = validators.get(key)
        if not validator:
            return (False, "The project configuration key '{}' is not recognized.".format(key))

        valid, message = validator(configuration)
        if not valid:
            return (False, message)

    return (True, None)


def is_project_name(name):
    """Validates the specified project name.

    A valid name is simply a non-empty string.

    Args:
        name (str): A project name to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified name is
            valid, False otherwise; and an error message in case the name is invalid.
    """
    try:
        return (False, "A project name must be a non-empty string.") if is_empty_string(name) else (True, None)
    except TypeError:
        return (False, "The 'name' argument must be a string.")


def is_project_short_name(short_name):
    """Validates the specified project short name.

    A valid short name is a non-empty string that contains only alphanumeric
    characters (a-z, A-Z, 0-9), hyphens (-) and underscores (_).

    Args:
        short_name (str): A project short name to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified short name is
            valid, False otherwise; and an error message in case the short name is invalid.
    """
    ERROR_MESSAGE = "A short name must be a non-empty string containing only of alphanumeric characters (a-z, A-Z, 0-9), hyphens (-) and underscores (_)."
    try:
        if is_empty_string(short_name):
            return (False, ERROR_MESSAGE)
        else:
            from re import match
            matches = match(r"[a-zA-Z0-9-_]+", short_name)
            matched = matches and (matches.group() == short_name)
            return (True, None) if matched else (False, ERROR_MESSAGE)
    except TypeError:
        return (False, "The 'short_name' argument must be a string.")


def is_project_description(description):
    """Validates the specified project description.

    A valid description is simply a non-empty string.

    Args:
        description (str): A project description to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified description
            is valid, False otherwise; and an error message in case the description is invalid.
    """
    try:
        return (False, "A project description must be a non-empty string.") if is_empty_string(description) else (True, None)
    except TypeError:
        return (False, "The 'description' argument must be a string.")


def is_project_repository(url):
    """Validates the specified project repository URL.

    Args:
        url (string): A URL to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified URL
            is valid, False otherwise; and an error message in case the URL is invalid.
    """
    if not isinstance(url, basestring):
        return (False, "A repository URL must be a string.")
    elif not is_url(url):
        return (False, "A repository configuration must be a valid URL and include the URL protocol.")

    return (True, None)


def is_project_do_not_track(do_not_track):
    """Validates the specified project 'Do Not Track' flag.

    A flag is nothing but a boolean value.

    Args:
        do_not_track (bool): A flag to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified flag
            is valid, False otherwise; and an error message in case the flag is invalid.
    """
    ERROR_MESSAGE = "The 'do_not_track' argument must be a boolean."
    return (True, None) if isinstance(do_not_track, bool) else (False, ERROR_MESSAGE)
