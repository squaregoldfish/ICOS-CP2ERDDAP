#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# assumedRole.py

"""
    The assumedRole module is used to explore ICOS CP AssumedRoles' metadata.

    Example usage:

    From assumedRole import AssumedRole

    assumedroles = AssumedRole()      # initialise ICOS CP AssumedRole object
    assumedroles.get_meta()           # get assumedroles' metadata from ICOS CP
    assumedroles.show()               # print assumedroles' metadata
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
    'otcmeta:atOrganization': 'Organization',
    'otcmeta:hasHolder': 'Person',
    'otcmeta:hasRole': 'Role',
    'otcmeta:hasAttributionWeight': 'attributionWeight',
    'otcmeta:hasEndTime': 'endTime',
    'otcmeta:hasStartTime': 'startTime'
}


# ----------------------------------------------
class AssumedRole(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show()
    """

    def __init__(self, limit=None, uri=None):
        """ initialise instance of AssumedRole(ICPObj).

        It will be used to set up a sparql query, and get all metadata of AssumeRole from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select AssumedRole:
        - with ICOS CP 'uri'

        Example:
            AssumedRole(limit=5)

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
        self._object = 'http://meta.icos-cp.eu/ontologies/otcmeta/AssumedRole'


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': AssumedRole(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
