#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# collection.py

"""
    The collection module is used to explore ICOS CP Collections' metadata.

    Example usage:

    From collection import Collection

    collections = Collection()        # initialise ICOS CP Collection object
    collections.get_meta()            # get collections' metadata from ICOS CP
    collections.show()                # print collections' metadata
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
    'cpmeta:wasAcquiredBy': 'Collection_acquirer',
    'cpmeta:wasProducedBy': 'Collection_producer',
    'cpmeta:wasSubmittedBy': 'Collection_submitter',
    'prov:hadPrimarySource': 'collection_primary_source',
    'prov:wasGeneratedBy': 'collection_generator',
    'prov:wasRevisionOf': 'collection_previous_revision',
    # Warning: if change, do not forget to change in:
    #   superIcpObj.py:_getSubAttr(): elif k in 'NextVersionOf':
    'cpmeta:isNextVersionOf': 'NextVersionOf',
    'cpmeta:hasDoi': 'collection_doi'
}


# ----------------------------------------------
class Collection(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(self, limit=None, lastversion=None, uri=None):
        """ initialise instance of Collection(Organization).

        It will be used to set up a sparql query, and get all metadata of Collection from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select Collection:
        - only from the 'lastversion'
        - with ICOS CP 'uri'

        Example:
            Collection(limit=5)

        :param limit: number of returned results
        :param lastversion: select only last release [True,False]
        :param uri: ICOS CP URI ('https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z')
        """
        super().__init__()
        # set up class/instance variables
        self._uri = uri
        self._limit = limit
        self._lastversion = lastversion

        # object attributes' dictionary
        if isinstance(_attr, dict):
            self._attr = {**_attr, **self._attr}

        # object type URI
        self._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/Collection'


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': Collection(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
