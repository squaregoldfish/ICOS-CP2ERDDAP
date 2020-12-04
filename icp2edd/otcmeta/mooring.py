#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# mooring.py

"""
    The mooring module is used to explore ICOS CP Moorings' metadata.

    Example usage:

    From mooring import Mooring

    moorings = Mooring()        # initialise ICOS CP Mooring object
    moorings.get_meta()         # get moorings' metadata from ICOS CP
    moorings.show()             # print moorings' metadata
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
    'otcmeta:hasLatitude': 'latitude',
    'otcmeta:hasLongitude': 'longitude',
    'otcmeta:hasDeploymentSchedule': 'deploymentSchedule',
    'otcmeta:hasDiscreteSamplingSchedule': 'discreteSamplingSchedule',
    'otcmeta:hasInstrumentSetup': 'instrumentSetup',
    'otcmeta:hasRetrievalMethod': 'retrievalMethod'
}


# ----------------------------------------------
class Mooring(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show()
    """

    def __init__(self, limit=None, uri=None):
        """ initialise instance of Mooring(ICPObj).

        It will be used to set up a sparql query, and get all metadata of Mooring from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select Mooring:
        - with ICOS CP 'uri'

        Example:
            Mooring(limit=5)

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
        self._object = 'http://meta.icos-cp.eu/ontologies/otcmeta/Mooring'


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': Mooring(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
