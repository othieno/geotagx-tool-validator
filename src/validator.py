# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project validator tool.
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
def is_configuration_set(configurations, enable_logging=False):
    """Validates the specified set of configurations.

    A configuration set must contain the project (project.json) and task presenter
    (task_presenter.json) configurations for a given GeoTag-X project. Optionally,
    a tutorial configuration (tutorial.json) may be included.

    A configuration set is considered valid if and only if each of its configurations
    is valid.

    Args:
        configurations (dict): A dictionary containing a set of configurations to validate.
        enable_logging (bool): If set to True, the function will log the operations it performs.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified configuration
            set is valid, False otherwise; and an error message in case the set is invalid.

    Raises:
        TypeError: If the configurations argument is not a dictionary or enable_logging is not a boolean.
        ValueError: If a required configuration is missing from the configuration set.
    """
    if not isinstance(configurations, dict):
        raise TypeError("Invalid argument type: validate_configurations expects 'dict' for the configurations parameter but got '{}'.".format(type(configurations).__name__))
    elif not isinstance(enable_logging, bool):
        raise TypeError("Invalid argument type: validate_configurations expects 'bool' for the enable_logging parameter but got '{}'.".format(type(enable_logging).__name__))

    is_nonempty_dictionary = lambda d: isinstance(d, dict) and len(d) > 0
    if not all(is_nonempty_dictionary(configurations.get(k)) for k in ["project", "task_presenter"]):
        raise ValueError("A required configuration is missing from the specified configuration set.")

    from functools import partial
    validators = {
        "project": is_project,
        "task_presenter": is_task_presenter,
        "tutorial": partial(is_tutorial, task_presenter=configurations["task_presenter"]),
    }

    for key, configuration in configurations.iteritems():
        validator = validators[key]
        valid, message = validator(configuration, enable_logging=enable_logging)
        if not valid:
            return (False, message)

    return (True, None)


def is_project(project, enable_logging=False):
    """Validates the specified project configuration.
    """
    raise NotImplementedError()


def is_task_presenter(task_presenter, enable_logging=False):
    """Validates the specified task presenter configuration.
    """
    raise NotImplementedError()


def is_tutorial(tutorial, task_presenter, enable_logging=False):
    """Validates the specified tutorial configuration.
    """
    raise NotImplementedError()
