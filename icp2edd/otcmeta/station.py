#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# station.py

"""
    The station module is used to explore ICOS CP Stations' metadata.

    Example usage:

    From station import Station

    stations = Station()    # initialise ICOS CP Station object
    stations.get_meta()     # get stations' metadata from ICOS CP
    stations.show()         # print stations' metadata
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
    'otcmeta:countryCode': 'countryCode',
    'otcmeta:hasName': 'name',
    'otcmeta:hasStationId': 'stationId',
    'otcmeta:hasGeoRegion': 'GeoRegion'
}


# ----------------------------------------------
class Station(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show()
    <BLANKLINE>
    type: <class '__main__.Station'>
    <BLANKLINE>
    Class name: xxx
    ...
    <BLANKLINE>
    \tcountryCode         : type: literal    value: ...
    \tname                : type: literal    value: ...
    \tstationId           : type: literal    value: ...
    \tGeoRegion           : type: uri        value: ...
    \tlabel               : type: literal    value: ...
    \tcomment             : type: literal    value: ...
    \tseeAlso             : type: literal    value: ...
    \turi                 : type: uri        value: ...
    <BLANKLINE>
    ...
    """

    def __init__(self, limit=None, uri=None):
        """ initialise instance of Station(ICPObj).

        It will be used to set up a sparql query, and get all metadata of Station from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select Station:
        - with ICOS CP 'uri'

        Example:
            Station(limit=5)

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
        self._object = 'http://meta.icos-cp.eu/ontologies/otcmeta/Station'


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': Station(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
