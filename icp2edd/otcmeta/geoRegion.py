#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# geoRegion.py

"""
    The geoRegion module is used to explore ICOS CP GeoRegions' metadata.

    Example usage:

    From geoRegion import GeoRegion

    georegions = GeoRegion()    # initialise ICOS CP GeoRegion object
    georegions.get_meta()       # get georegions' metadata from ICOS CP
    georegions.show()           # print georegions' metadata
"""

# --- import -----------------------------------
# import from standard lib
import logging
# import from other lib
# import from my project
from icp2edd.icpObj import ICPObj

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
class GeoRegion(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show()
    <BLANKLINE>
    type: <class '__main__.GeoRegion'>
    <BLANKLINE>
    Class name: xxx
    ...
    <BLANKLINE>
    \tlabel               : type: literal    value: ...
    \tcomment             : type: literal    value: ...
    \tseeAlso             : type: literal    value: ...
    \turi                 : type: uri        value: ...
    <BLANKLINE>
    ...
    """

    def __init__(self, limit=None, uri=None):
        """ initialise instance of GeoRegion(ICPObj).

        It will be used to set up a sparql query, and get all metadata of GeoRegion from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select GeoRegion:
        - with ICOS CP 'uri'

        Example:
            GeoRegion(limit=5)

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
        self._object = 'http://meta.icos-cp.eu/ontologies/otcmeta/GeoRegion'


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': GeoRegion(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
