#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# simpleDataObject.py

"""
    The simpleDataObject module is used to explore ICOS CP SimpleDataObjects' metadata.

    Example usage:

    From simpleDataObject import SimpleDataObject

    simpleDataObjects = SimpleDataObject()  # initialise ICOS CP SimpleDataObject object
    simpleDataObjects.get_meta()            # get simpleDataObjects' metadata from ICOS CP
    simpleDataObjects.show()                # print simpleDataObjects' metadata
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
    'cpmeta:hasActualColumnNames': 'simple_obj_actual_column_name',
    'cpmeta:hasNumberOfRows': 'simple_obj_number_of_rows'
}


# ----------------------------------------------
class SimpleDataObject(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(self, limit=None, product=None, uri=None):
        """ initialise instance of SimpleDataObject(ICPObj).

        It will be used to set up a sparql query, and get all metadata of SimpleDataObject from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select SimpleDataObject:
        - of data type 'product'
        - with ICOS CP 'uri'

        Example:
            SimpleDataObject(limit=5)

        :param limit: number of returned results
        :param uri: ICOS CP URI ('https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z')
        """
        super().__init__()
        # set up class/instance variables
        self._uri = uri
        self._limit = limit
        self._product = product

        # object attributes' dictionary
        if isinstance(_attr, dict):
            self._attr = {**_attr, **self._attr}

        # object type URI
        self._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/SimpleDataObject'


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': SimpleDataObject(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
