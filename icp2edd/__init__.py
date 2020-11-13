#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __init__.py

from pbr.version import VersionInfo

_v = VersionInfo('mock').semantic_version()
__version__ = _v.release_string()
version_info = _v.version_tuple()

# TODO set up here config file ???
