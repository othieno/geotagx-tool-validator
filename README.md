# GeoTag-X Project Validator

[![Coverage Status](https://coveralls.io/repos/github/othieno/geotagx-tool-validator/badge.svg?branch=master)](https://coveralls.io/github/othieno/geotagx-tool-validator?branch=master)
[![Build Status](https://travis-ci.org/othieno/geotagx-tool-validator.svg?branch=master)](https://travis-ci.org/othieno/geotagx-tool-validator)

The project validator is a command line tool used to validate GeoTag-X project configurations as per their technical specifications which may be found [here][project_specification] (project), [here][task_presenter_specification] (task presenter) and [here][tutorial_specification] (tutorial).



## Validating a Project

With the tool installed (please refer to the [installation guide](INSTALL.md)), you may display its help and usage manual by running
```bash
geotagx-validator --help
```

Validating a project located at `/path/to/geotagx/project/` is as simple as running
```bash
geotagx-validator /path/to/geotagx/project/
```



## Getting Involved

Have you noticed a bug in our code? Do you think we can improve this project? Learn how to [contribute to this project](CONTRIBUTING.md)!



[project_specification]: https://github.com/geotagx/geotagx-documentation/specifications/project-configuration.md "Project Configuration Specification"
[task_presenter_specification]: https://github.com/geotagx/geotagx-documentation/specifications/task-presenter-configuration.md "Task Presenter Configuration Specification"
[tutorial_specification]: https://github.com/geotagx/geotagx-documentation/specifications/tutorial-configuration.md "Tutorial Configuration Specification"
