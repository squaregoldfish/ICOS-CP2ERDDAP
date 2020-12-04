#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# simpleObjectSpec.py

"""
    The SimpleObjectSpec module is used to explore ICOS CP simpleobjectspecs' metadata.

    Example usage:

    From SimpleObjectSpec import SimpleObjectSpec

    simpleobjectspecs = SimpleObjectSpec()    # initialise ICOS CP SimpleObjectSpec object
    simpleobjectspecs.get_meta()              # get simpleobjectspecs' metadata from ICOS CP
    simpleobjectspecs.show()                  # print simpleobjectspecs' metadata
"""

# --- import -----------------------------------
# import from standard lib
import logging
# import from other lib
# import from my project
from icp2edd.cpmeta.dataObjectSpec import DataObjectSpec

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

# object attributes' dictionary with RDF 'property' as key and RDF 'object' as value
#   RDF triples: 'subject' + 'property/predicate' + 'object/value'
# {'property/predicate': 'object/value'}
# Note: 'object/value' will be the output attribute name
_attr = {
}


# ----------------------------------------------
class SimpleObjectSpec(DataObjectSpec):
    """
    >>> t.getMeta()
    >>> t.show()
    """

    def __init__(self, limit=None, uri=None):
        """
        This functions initialise instance of SimpleObjectSpec(ICPObj).
        Set up a sparql query to get all metadata of SimpleObjectSpec from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select SimpleObjectSpec:
        - with ICOS CP 'uri'

        Example:
            SimpleObjectSpec(limit=5)

        :param limit: number of returned results
        :param uri: ICOS CP URI ('https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z')
        """
        super().__init__()
        # set up class/instance variables
        self._uri = uri
        self._limit = limit

        # object attributes' dictionary
        if isinstance(_attr, dict):
            self._attr = {**_attr, **self._attr}

        # object type URI
        self._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/SimpleObjectSpec'


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': SimpleObjectSpec(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
