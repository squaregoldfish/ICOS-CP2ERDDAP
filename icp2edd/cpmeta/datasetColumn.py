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
import traceback
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
    'cpmeta:hasColumnTitle': 'dataset_column_column_title',
    'cpmeta:hasValueType': 'Dataset_variable_value_type',   # TODO see how to get it through checkOnto
    'cpmeta:hasValueFormat': 'Dataset_column_valueFormat',
    'cpmeta:isOptionalColumn': 'dataset_column_is_optional_column',
    'cpmeta:isQualityFlagFor': 'QualityFlagFor',  # Warning: linked to:
    #                                             # - superIcpObj.py:_getSubAttr(): elif k in 'QualityFlagFor':
    'cpmeta:isRegexColumn': 'dataset_column_is_regex_column'
}
# list of equivalent class
_equivalentClass = []


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

        if isinstance(_equivalentClass, list):
            self._equivalentClass = _equivalentClass

        # object type URI
        self._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/DatasetColumn'

        #
        self._objtype = None
        if self._object is not None:
            self.objtype = self._getObjectType()

        # get instance name
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self._instance_name = text[:text.find('=')].strip()


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': DatasetColumn(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
