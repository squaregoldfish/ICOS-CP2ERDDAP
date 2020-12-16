#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# staticObject.py

"""
    The staticObject module is used to explore ICOS CP StaticObjects' metadata.

    Example usage:

    From staticObject import StaticObject

    staticObjects = StaticObject()      # initialise ICOS CP StaticObject object
    staticObjects.get_meta()            # get staticObjects' metadata from ICOS CP
    staticObjects.show()                # print staticObjects' metadata
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
        'cpmeta:hasSha256sum': 'hexBinary',
        'cpmeta:hasSizeInBytes': 'sizeInBites',
        'cpmeta:wasSubmittedBy': 'DataSubmission',
        'cpmeta:hasCitationString': 'string',
        'cpmeta:isNextVersionOf': 'NextVersionOf',
        'cpmeta:hasDoi': 'doi',
        'cpmeta:hasName': 'name'
}


# ----------------------------------------------
class StaticObject(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(self, limit=None, submfrom=None, submuntil=None, lastversion=None, uri=None):
        """ initialise instance of StaticObject(ICPObj).

        It will be used to set up a sparql query, and get all metadata of StaticObject from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select StaticObject:
        - submitted from 'submfrom'
        - submitted until 'submuntil'
        - only from the 'lastversion'
        - with ICOS CP 'uri'

        Example:
            StaticObject(limit=5)

        :param limit: number of returned results
        :param submfrom: submitted from date ( '2020-01-01T00:00:00.000Z' )
        :param submuntil: submitted until date ( '2020-01-01T00:00:00.000Z' )
        :param lastversion: select only last release [True,False]
        :param uri: ICOS CP URI ('https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z')
        """
        super().__init__()
        # set up class/instance variables
        self._uri = uri
        self._limit = limit
        self._from = submfrom
        self._until = submuntil
        self._lastversion = lastversion

        # object attributes' dictionary
        if isinstance(_attr, dict):
            self._attr = {**_attr, **self._attr}

        # object type URI
        self._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/StaticObject'


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': StaticObject(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
