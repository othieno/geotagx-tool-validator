# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project validator tool.
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
from project import is_project_configuration
from task_presenter import is_task_presenter_configuration
from tutorial import is_tutorial_configuration
from helper import check_arg_type

def is_configuration_set(configurations):
    """Validates the specified set of configurations.

    A configuration set must contain the project (project.json) and task presenter
    (task_presenter.json) configurations for a given GeoTag-X project. Optionally,
    a tutorial configuration (tutorial.json) may be included.

    A configuration set is considered valid if and only if each of its configurations
    is valid.

    Args:
        configurations (dict): A dictionary containing a set of configurations to validate.

    Returns:
        <bool, str|None>: A pair containing the value True if the specified configuration
            set is valid, False otherwise; and an error message in case the set is invalid.

    Raises:
        TypeError: If the configurations argument is not a dictionary.
        ValueError: If a required configuration is missing from the configuration set.
    """
    check_arg_type(is_configuration_set, "configurations", configurations, dict)

    is_nonempty_dictionary = lambda d: isinstance(d, dict) and len(d) > 0
    if not all(is_nonempty_dictionary(configurations.get(k)) for k in ["project", "task_presenter"]):
        raise ValueError("A required configuration is missing from the specified configuration set.")

    from collections import OrderedDict
    validators = OrderedDict({
        "project": is_project_configuration,
        "task_presenter": is_task_presenter_configuration,
        "tutorial": lambda t: is_tutorial_configuration(t, configurations["task_presenter"], False),
    })
    for key, configuration in configurations.iteritems():
        validator = validators[key]
        valid, message = validator(configuration)
        if not valid:
            return (False, message)

    return (True, None)
