python-fitparse
===============

> **NOTE:** This is a fork of [dtcooper/python-fitparse](https://github.com/dtcooper/python-fitparse).
> The original maintainer has limited time to work on this package.
> This fork continues active development with support for new FIT SDK versions and patches.

Here's a Python library to parse ANT/Garmin `.FIT` files.
[![Build Status](https://github.com/nbr23/python-fitparse/workflows/test/badge.svg)](https://github.com/nbr23/python-fitparse/actions?query=workflow%3Atest)


Install from [![PyPI](https://img.shields.io/pypi/v/python-fitparse.svg)](https://pypi.python.org/pypi/python-fitparse/):
```
pip install python-fitparse
```

Usage
-----
A simple example of printing records from a fit file:

```python
import fitparse

# Load the FIT file
fitfile = fitparse.FitFile("my_activity.fit")

# Iterate over all messages of type "record"
# (other types include "device_info", "file_creator", "event", etc)
for record in fitfile.get_messages("record"):

    # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
    for data in record:

        # Print the name and value of the data (and the units if it has any)
        if data.units:
            print(" * {}: {} ({})".format(data.name, data.value, data.units))
        else:
            print(" * {}: {}".format(data.name, data.value))

    print("---")
```

The library also provides a `fitdump` command-line tool for parsing FIT files. Run `fitdump --help` for details.

License
-------

This project is licensed under the MIT License - see the [`LICENSE`](LICENSE)
file for details.
