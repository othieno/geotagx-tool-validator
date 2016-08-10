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
def main():
    """Executes the application.
    """
    import sys
    sys.exit(run(get_argparser().parse_args(sys.argv[1:])))


def run(arguments):
    """Executes the application with the specified command-line arguments.

    Args:
        arguments (list): A list of command-line argument strings.
    """
    raise NotImplementedError()


def get_argparser():
    """Constructs the application's command-line argument parser.

    Returns:
        argparse.ArgumentParser: A command-line argument parser instance.
    """
    raise NotImplementedError()


def _version():
    """Returns the tool's version string.
    """
    from __init__ import __version__
    return "GeoTag-X Project Validator v%s, Copyright (C) 2016 UNITAR/UNOSAT." % __version__


if __name__ == "__main__":
    main()
