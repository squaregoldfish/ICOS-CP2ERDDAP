#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# as.py

"""
    The as module is used to explore ICOS CP ASs' metadata.

    Example usage:

    From as import AS

    ass = AS()                # initialise ICOS CP AS object
    ass.get_meta()            # get ass' metadata from ICOS CP
    ass.show()                # print ass' metadata
"""

# --- import -----------------------------------
# import from standard lib
import logging
# import from other lib
# import from my project
from icp2edd.cpmeta.icosStation import IcosStation

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
class AS(IcosStation):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(self, limit=None, uri=None):
        """ initialise instance of AS(IcosStation).

        It will be used to set up a sparql query, and get all metadata of AS from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select AS:
        - with ICOS CP 'uri'

        Example:
            AS(limit=5)

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
        self._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/AS'


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': AS(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
