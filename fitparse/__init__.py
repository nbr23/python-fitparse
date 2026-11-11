#!/usr/bin/env python

import importlib.metadata

# Make classes available
from fitparse.base import FitFile, FitFileDecoder, UncachedFitFile, \
                          FitParseError, CacheMixin, DataProcessorMixin
from fitparse.records import DataMessage
from fitparse.processors import FitFileDataProcessor, StandardUnitsDataProcessor


try:
    __version__ = importlib.metadata.version("python-fitparse")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
