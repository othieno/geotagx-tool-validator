# -*- coding: utf-8 -*-
#
# This module is part of the GeoTag-X project validator tool.
# It contains miscellaneous helper functions.
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
import os
import re

def check_arg_type(f, arg_name, arg_value, expected_type): # pragma: no cover
    """Checks the specified argument's type.

    Args:
        f (function): The function that the argument belongs to.
        arg_name (str): The argument's name in string format.
        arg_value: The argument's value.
        expected_type: The argument's expected type(s).

    Raises:
        TypeError: If the specified argument value's type is not expected.
        AssertionError: If the f argument is not a function, or the arg_name is not a string.
    """
    assert(callable(f))
    assert(isinstance(arg_name, str))

    if not isinstance(arg_value, expected_type):
        message = "Invalid argument type: {} expects '{}' for the '{}' argument but got '{}'."
        arg_type = type(arg_value).__name__
        try:
            types = "' or '".join([t.__name__ for t in expected_type])
        except TypeError:
            types = expected_type.__name__
        finally:
            raise TypeError(message.format(f.func_name, types, arg_name, arg_type))


def is_empty_string(empty_string):
    """Checks if the specified string is empty.

    A string is considered empty if it does not contain characters other than
    whitespace or escape sequences.

    Args:
        empty_string (basestring): An empty string to check.

    Returns:
        bool: True if the specified string is empty, False otherwise.

    Raises:
        TypeError: If the empty_string argument is not a string.
    """
    check_arg_type(is_empty_string, "empty_string", empty_string, basestring)

    return not empty_string or empty_string.isspace()


def is_normalized_string(normalized_string, language_codes=None):
    """Checks if the specified string is normalized.

    A normalized string is not a true string but rather a non-empty dictionary where each key is a
    language code that is mapped to a non-empty string.

    Args:
        normalized_string (dict): A normalized string to validate.
        language_codes (list): A list of language codes that the normalized string dictionary must contain.
            If unspecified, the function only verifies that the dictionary keys are indeed valid language codes.

    Returns:
        bool: True if the specified string is normalized, False otherwise.

    Raises:
        TypeError: If the normalized_string argument is not a dictionary or if the language_codes argument is
            not a list or a NoneType.
    """
    check_arg_type(is_normalized_string, "normalized_string", normalized_string, dict)

    if language_codes is not None and not isinstance(language_codes, list):
        raise TypeError("Invalid argument type: is_normalized_string expects 'list' for language_codes argument but got '{}'.".format(type(language_codes).__name__))

    try:
        return normalized_string and \
               (True if language_codes is None else all(l in normalized_string for l in language_codes)) and \
               all(is_language_code(k) and not is_empty_string(v) for k, v in normalized_string.iteritems())
    except TypeError:
        # The is_empty_string function will raise a TypeError if the code argument is not a
        # string. So if the argument is not a string, it stands to reason that it's not a
        # valid ISO code.
        return False


def is_configuration_string(configuration_string, language_codes=None):
    """Checks if the specified string is a configuration string.

    A configuration string, for lack of a better term, is a non-empty string, or a
    normalized string, usually used in GeoTag-X's project configurations.

    Args:
        configuration_string (basestring|dict): A string or dictionary to validate.
        language_codes (list): A list of languages that the normalized string dictionary must
            contain, where each item of the list is a language code. Note that this argument
            is used if and only if the string argument a dictionary (i.e., a normalized string).

    Returns:
        bool: True if the specified configuration string is valid, False otherwise.

    Raises:
        TypeError: If the configuration_string argument is not a string or dictionary,
            or if the language_codes argument is not a list or NoneType.
    """
    check_arg_type(is_configuration_string, "configuration_string", configuration_string, (basestring, dict))

    if isinstance(configuration_string, basestring):
        return not is_empty_string(configuration_string)
    elif isinstance(configuration_string, dict):
        return is_normalized_string(configuration_string, language_codes)


def is_url(url):
    """Checks if the specified URL is valid.

    Args:
        url (str): A URL to check.

    Returns:
        bool: True if the specified URL is valid, False otherwise.

    Raises:
        TypeError: If the specified url argument is not a string.
    """
    if is_empty_string(url):
        return False
    else:
        # The following code is inspired by the validators package from Konsta Vesterinen. Please
        # refer to https://github.com/kvesteri/validators/blob/master/validators/url.py for more
        # information.
        regex = (
            r'^[a-z]+://([^/:]+\.[a-z]{2,10}|([0-9]{{1,3}}\.)'
            r'{{3}}[0-9]{{1,3}})(:[0-9]+)?(\/.*)?$'
        )
        return re.compile(regex).match(url)


def is_iso_3166_1_alpha_2_code(code):
    """Validates the specified ISO 3166-1 alpha-2 code.

    An ISO 3166-1 alpha-2 code is a two-letter uppercase string assigned to a region,
    e.g. GB (United Kingdom), US (United States) or CH (Switzerland).

    Args:
        code (str): An ISO 3166-1 alpha-2 code to validate.

    Returns:
        bool: True if the specified code is a valid ISO 3166-1 alpha-2 code, False otherwise.
    """
    try:
        if is_empty_string(code):
            return False
        else:
            # TODO Optimize this: Regular expressions are a bit of an overkill.
            matches = re.match("[A-Z]{2}", code)
            return matches and matches.group() == code
    except TypeError:
        # The is_empty_string function will raise a TypeError if the code argument is not a
        # string. So if the argument is not a string, it stands to reason that it's not a
        # valid ISO code.
        return False


def is_iso_15924_code(code):
    """Validates the specified ISO 15924 code.

    An ISO 15924 code is a four-letter capitalized string assigned to a language's writing system,
    for instance Latn (Latin), Cyrl (Cyrillic), or Arab (Arabic).

    Args:
        code (str): An ISO 15924 code to validate.

    Returns:
        bool: True if the specified code is a valid ISO 15924 code, False otherwise.
    """
    try:
        if is_empty_string(code):
            return False
        else:
            matches = re.match("[A-Z]{1}[a-z]{3}", code)
            return matches and matches.group() == code
    except TypeError:
        # The is_empty_string function will raise a TypeError if the code argument is not a
        # string. So if the argument is not a string, it stands to reason that it's not a
        # valid ISO code.
        return False


def is_language_code(code):
    """Validates the specified language code.

    A language code is a non-empty string containing two or three lowercase letters. It may
    be extended with one of the following variety codes:
    - an ISO 3166-1 alpha-2 code to denote the region in which the language is spoken,
    - an ISO 15924 code which represents the name of the language's writing system (script).

    A variety code must always be preceded by a hyphen (-) e.g. en-GB, zh-Hans, az-Latn or fr-CH.

    Args:
        code (str): A language code to validate.

    Returns:
        bool: True if the specified code is a valid language code, False otherwise.
    """
    try:
        if is_empty_string(code):
            return False
        elif code in is_language_code.KNOWN_LANGUAGE_CODES:
            return True
        else:
            matches = re.match(r"([a-z]{2,3})(-[a-zA-Z]{2,4})?", code)
            if matches and matches.group() == code:
                valid = True
                variety = matches.group(2)
                if variety:
                    variety = variety[1:] # Skip the hyphen separator.
                    valid = is_iso_3166_1_alpha_2_code(variety) or is_iso_15924_code(variety)

                if valid:
                    is_language_code.KNOWN_LANGUAGE_CODES.add(code)

                return valid
            else:
                return False
    except TypeError:
        # The is_empty_string function will raise a TypeError if the code argument is not a
        # string. So if the argument is not a string, it stands to reason that it's not a
        # valid ISO code.
        return False

is_language_code.KNOWN_LANGUAGE_CODES = set()
"""A cache used by the is_language_code function to store and quickly retrieve verified language codes."""


def is_directory(path, check_writable=False): #pragma: no cover
    """Checks if the specified path is a readable directory.

    Args:
        path (str): A path to a directory to check.
        check_writable (bool): If set to True, the function checks if the directory is writable too.

    Returns:
        bool: True if the specified path is a readable directory, False otherwise. If check_writable
            is set to True, True will be returned if the directory is read/writable, False otherwise.

    Raises:
        TypeError: If the path argument is not a string or check_writable argument is not a boolean.
    """
    check_arg_type(is_directory, "path", path, basestring)
    check_arg_type(is_directory, "check_writable", check_writable, bool)

    return os.path.isdir(path) and os.access(path, os.R_OK | os.W_OK if check_writable else os.R_OK)


def is_project_directory(path, check_writable=True): #pragma: no cover
    """Checks if the specified path is a directory that contains a GeoTag-X project.

    For the purpose of the validator tool, a complete GeoTag-X project must contain
    the following files:
    - project.json: a project's configuration,
    - task_presenter.json: a task presenter configuration.

    Optionally, a project may contain a tutorial configuration (tutorial.json).

    It is important to note that this function only makes sure the required configuration
    files exist but does not validate their content.

    Args:
        path (str): A path to a directory to check.
        check_writable (bool): If set to True, the function will also check if the directory
            located at the specified path can be written to.

    Returns:
        bool: True if the specified path contains a complete GeoTag-X project, False otherwise.

    Raises:
        TypeError: If the path argument is not a string or check_writable is not a boolean.
        IOError: If the specified path is inaccessible or not a directory.
    """
    if not is_directory(path, check_writable):
        raise IOError("The path '{}' is not a directory or you may not have the appropriate access permissions.".format(path))
    else:
        # Make sure the mandatory configurations exist and are readable.
        filenames = [os.path.join(path, name) for name in ["project.json", "task_presenter.json"]]
        return all(os.path.isfile(f) and os.access(f, os.R_OK) for f in filenames)


def sanitize_paths(paths): #pragma: no cover
    """Removes duplicates as well as paths that do not lead to a valid GeoTag-X project directory.

    Args:
        paths (list): A list of paths to sanitize.

    Returns:
        list: A list of paths that contains no duplicates as well as directories that are
            guaranteed to contain GeoTag-X configuration files. Note that the returned
            list may be empty.

    Raises:
        TypeError: If the paths argument is not a list or one of its elements is not a string.
        IOError: If a path is inaccessible or not a directory.
    """
    check_arg_type(sanitize_paths, "paths", paths, list)

    return filter(is_project_directory, set([os.path.realpath(p) for p in paths]))


def deserialize_json(filename): #pragma: no cover
    """Returns the JSON object from the file with the specified filename.

    Args:
        filename: The name of the file containing the JSON data to deserialize.

    Returns:
        dict: A dictionary containing the deserialized JSON data.

    Raises:
        IOError: If the file with the specified filename could not be opened.
    """
    with open(filename) as file:
        import json, collections
        return json.loads(file.read(), object_pairs_hook=collections.OrderedDict)


def deserialize_configuration_set(path): #pragma: no cover
    """Deserializes the set of configuration files for GeoTag-X project located at the specified path.

    Args:
        path (str): A path to a directory containing a GeoTag-X project.

    Returns:
        dict|None: A dictionary containing deserialized JSON configurations if the specified
            path contains a valid GeoTag-X project, None otherwise.

    Raises:
        TypeError: If the path argument is not a string.
        IOError: If the specified path is inaccessible or not a directory, or if a required
            configuration in the directory at the specified path is inaccessible.
    """
    if not is_project_directory(path):
        return None

    configurations = {}
    filepath = os.path.join(path, "{}.json")
    for key in ["project", "task_presenter", "tutorial"]:
        try:
            configurations[key] = deserialize_json(filepath.format(key))
        except IOError:
            # If a configuration is required but its JSON file is missing, re-raise the exception.
            if key in {"project", "task_presenter"}:
                raise

    # Add the questionnaire help.
    filepath = os.path.join(path, "help", "{}.html")
    for question in configurations["task_presenter"]["questionnaire"]["questions"]:
        key = question["key"]
        filename = filepath.format(key)
        try:
            file = open(filename)
        except IOError:
            # A help file is not always guaranteed to exist so if an IOError occurs, ignore it.
            pass
        else:
            with file:
                from htmlmin import minify
                filedata = file.read().decode("UTF-8").strip()
                question["help"] = minify(filedata, remove_comments=True, remove_empty_space=True)

    return configurations


def find_unexpected_keys(dictionary, expected_keys): # pragma: no cover
    """Returns a list of keys that are not expected to be in the specified dictionary.

    Args:
        dictionary (dict): A dictionary containing keys to check.
        expected_keys (frozenset): A set of keys expected to be in the specified dictionary.

    Returns:
        list: A list of keys that are not expected to be in the specified dictionary.

    Raises:
        TypeError: If the dictionary argument is not a dict, or the expected_keys
            argument is not a frozenset.
    """
    check_arg_type(find_unexpected_keys, "dictionary", dictionary, dict)
    check_arg_type(find_unexpected_keys, "expected_keys", expected_keys, frozenset)

    return [k for k in dictionary.keys() if k not in expected_keys]
