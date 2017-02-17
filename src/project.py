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
    }
    for key, configuration in configuration.iteritems():
        validator = validators[key]
        valid, message = validator(configuration, enable_logging=enable_logging)
        if not valid:
            return (False, message)

    return (True, None)


def is_project_name(name, enable_logging=False):
    raise NotImplementedError()


def is_project_short_name(short_name, enable_logging=False):
    raise NotImplementedError()


def is_project_description(description, enable_logging=False):
    raise NotImplementedError()


def is_project_repository(url, enable_logging=False):
    raise NotImplementedError()
