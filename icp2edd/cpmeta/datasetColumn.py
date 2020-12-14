#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# datasetColumn.py

"""
    The datasetColumn module is used to explore ICOS CP DatasetColumns' metadata.

    Example usage:

    From datasetColumn import DatasetColumn

    datasetColumns = DatasetColumn()     # initialise ICOS CP DatasetColumn object
    datasetColumns.get_meta()            # get datasetColumns' metadata from ICOS CP
    datasetColumns.show()                # print datasetColumns' metadata
"""

# --- import -----------------------------------
# import from standard lib
import logging
# import from other lib
# import from my project
from icp2edd.cpmeta.dataObjectSpecifyingThing import DataObjectSpecifyingThing

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

# object attributes' dictionary with RDF 'property' as key and RDF 'object' as value
#   RDF triples: 'subject' + 'property/predicate' + 'object/value'
# {'property/predicate': 'object/value'}
# Note: 'object/value' will be the output attribute name
_attr = {
        'cpmeta:hasColumnTitle': 'columnTitle',
        'cpmeta:hasValueFormat': 'ValueFormat',
        'cpmeta:isOptionalColumn': 'optionalColumn',
        'cpmeta:isRegexColumn': 'regexColumn',
        'cpmeta:isQualityFlagFor': 'DatasetColumn'
}


# ----------------------------------------------
class DatasetColumn(DataObjectSpecifyingThing):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(self, limit=None, uri=None):
        """ initialise instance of DatasetColumn(DataObjectSpecifyingThing).

        It will be used to set up a sparql query, and get all metadata of DatasetColumn from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select DatasetColumn:
        - with ICOS CP 'uri'

        Example:
            DatasetColumn(limit=5)

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
        self._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/DatasetColumn'


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': DatasetColumn(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
