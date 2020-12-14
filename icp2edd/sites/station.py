#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# station.py

"""
    The sites.station module is used to explore ICOS CP sites.Stations' metadata.

    Example usage:

    From sites.station import sites.Station

    sites.stations = sites.Station()     # initialise ICOS CP sites.Station object
    sites.stations.get_meta()            # get sites.stations' metadata from ICOS CP
    sites.stations.show()                # print sites.stations' metadata
"""

# --- import -----------------------------------
# import from standard lib
import logging
# import from other lib
# import from my project
from icp2edd.cpmeta.station import Station as cpStation

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
class Station(cpStation):
    """
    >>> t.getMeta()
    >>> t.show()

    """

    def __init__(self, limit=None, uri=None):
        """ initialise instance of sites.Station(Station).

        It will be used to set up a sparql query, and get all metadata of sites.Station from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select sites.Station:
        - with ICOS CP 'uri'

        Example:
            sites.Station(limit=5)

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
        self._object = 'https://meta.fieldsites.se/ontologies/sites/Station'


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': Station(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
