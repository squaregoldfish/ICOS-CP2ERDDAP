#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __init__.py

# --- import -----------------------------------
# import from standard lib
# import from other lib
from pbr.version import VersionInfo
# import from my project

_v = VersionInfo('mock').semantic_version()
__version__ = _v.release_string()
version_info = _v.version_tuple()
