#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# dataSubmission.py

"""
    The dataSubmission module is used to explore ICOS CP DataSubmissions' metadata.

    Example usage:

    From dataSubmission import DataSubmission

    dataSubmissions = DataSubmission()    # initialise ICOS CP DataSubmission object
    dataSubmissions.get_meta()            # get dataSubmissions' metadata from ICOS CP
    dataSubmissions.show()                # print dataSubmissions' metadata
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
        'prov:wasAssociatedWith': 'Thing',
        'prov:startedAtTime': 'startedAtTime',
        'prov:endedAtTime': 'endedAtTime',
        'cpmeta:wasPerformedAt': 'Feature'
}


# ----------------------------------------------
class DataSubmission(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(self, limit=None, uri=None):
        """ initialise instance of DataSubmission(ICPObj).

        It will be used to set up a sparql query, and get all metadata of DataSubmission from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select DataSubmission:
        - with ICOS CP 'uri'

        Example:
            DataSubmission(limit=5)

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
        self._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/DataSubmission'


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': DataSubmission(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
