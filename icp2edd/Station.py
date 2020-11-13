#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Station.py

"""
    The Station module is used to explore ICOS CP stations' metadata.

    Example usage:

    From Station import Station

    stations = Station()    # initialise ICOS CP Station object
    stations.get_meta()     # get stations' metadata from ICOS CP
    stations.show()         # print stations' metadata
"""

# --- import -----------------------------------
# import from standard lib
# import from other lib
# import from my project
from icp2edd.ICPObj import ICPObj


# ----------------------------------------------
class Station(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show()
    <BLANKLINE>
    type: <class '__main__.Station'>
    <BLANKLINE>
    Class name: Station
    ...
    <BLANKLINE>
    \tGeoRegion           : type: uri        value: ...
    \tstationId           : type: literal    value: ...
    \tname                : type: literal    value: ...
    \tcountryCode         : type: literal    value: ...
    \tlabel               : type: literal    value: ...
    \tcomment             : type: literal    value: ...
    \tseeAlso             : type: literal    value: ...
    \turi                 : type: uri        value: ...
    <BLANKLINE>
    ...
    """

    def __init__(self, limit=None, uri=None):
        """
        This functions initialise instance of Station(ICPObj).
        Set up a sparql query to get all metadata of Station from ICOS CP.

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
        # overwrite class name
        self._name = 'Station'
        # overwrite conventional attributes renaming dictionary
        self._convAttr = {}
        # overwrite query string
        self._queryString = """
            select ?xxx ?GeoRegion ?stationId ?name ?countryCode ?label ?comment ?seeAlso
            where {
                %s # _filterObj(uri_=uri)
                ?Station rdf:type/rdfs:subClassOf*  <http://meta.icos-cp.eu/ontologies/otcmeta/Station> .

                OPTIONAL { ?xxx otcmeta:hasGeoRegion ?GeoRegion .}
                OPTIONAL { ?xxx otcmeta:hasStationId ?stationId .}
                OPTIONAL { ?xxx otcmeta:hasName ?name .}
                OPTIONAL { ?xxx otcmeta:countryCode ?countryCode .}

                OPTIONAL { ?xxx rdfs:label ?label .}
                OPTIONAL { ?xxx rdfs:comment ?comment .}
                OPTIONAL { ?xxx rdfs:seeAlso ?seeAlso .}
            }
            %s  # _checkLimit(limit_=limit)
        """ % (self._filterObj(uri_=uri),
               self._checkLimit(limit_=limit))
        #


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': Station(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
