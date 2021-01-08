#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# site.py

"""
    The site module is used to explore ICOS CP Sites' metadata.

    Example usage:

    From site import Site

    sites = Site()              # initialise ICOS CP Site object
    sites.get_meta()            # get sites' metadata from ICOS CP
    sites.show()                # print sites' metadata
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
    'cpmeta:hasSamplingPoint': 'Site_position',
    'cpmeta:hasEcosystemType': 'Site_ecosystem_type',
    'geosparql:hasGeometry': 'Site_geometry',
    'cpmeta:hasSpatialCoverage': 'Site_spatial_coverage'
}


# ----------------------------------------------
class Site(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(self, limit=None, uri=None):
        """ initialise instance of Site(ICPObj).

        It will be used to set up a sparql query, and get all metadata of Site from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select Site:
        - with ICOS CP 'uri'

        Example:
            Site(limit=5)

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
        self._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/Site'


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': Site(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
