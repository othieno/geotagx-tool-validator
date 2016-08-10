#!/usr/bin/env python
#
# This setup script is inspired by code from the Pip setup.py found
# here: https://github.com/pypa/pip/blob/develop/setup.py
import os, re, codecs
from setuptools import setup, find_packages

cwd = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    # https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(cwd, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="geotagx-validator",
    version=find_version("src", "__init__.py"),
    description="The GeoTag-X Project Validator Tool.",
    long_description=read("README.md"),
    zip_safe=True,
    keywords="geotag-x project validator tool command line",
    author="Jeremy Othieno",
    author_email="j.othieno@gmail.com",
    url="https://github.com/geotagx/geotagx-tool-validator",
    download_url="https://github.com/geotagx/geotagx-tool-validator",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Utilities"
    ],
    platforms="any",
    license="MIT",
    packages=["geotagx_validator"],
    package_dir={"geotagx_validator": "src"},
    entry_points={
        "console_scripts":[
            "geotagx-validator=geotagx_validator.__main__:main"
        ]
    }
)
