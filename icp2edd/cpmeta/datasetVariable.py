#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# datasetVariable.py

"""
    The datasetVariable module is used to explore ICOS CP DatasetVariables' metadata.

    Example usage:

    From datasetVariable import DatasetVariable

    datasetVariables = DatasetVariable()   # initialise ICOS CP DatasetVariable object
    datasetVariables.get_meta()            # get datasetVariables' metadata from ICOS CP
    datasetVariables.show()                # print datasetVariables' metadata
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
    'cpmeta:hasColumnTitle': 'dataset_variable_column_title',
    'cpmeta:hasValueType': 'Dataset_variable_value_type',
    'cpmeta:hasVariableTitle': 'dataset_variable_variable_title',  # variable_name ? see http://meta.icos-cp.eu/resources/cpmeta/co2flux_land_flow_rate
    'cpmeta:isOptionalColumn': 'dataset_variable_is_optional_column',
    'cpmeta:isOptionalVariable': 'dataset_variable_is_optional_variable',
    'cpmeta:isRegexColumn': 'dataset_variable_is_regex_column',
    'cpmeta:isRegexVariable': 'dataset_variable_is_regex_variable'
}
# list of equivalent class
_equivalentClass = []


# ----------------------------------------------
class DatasetVariable(DataObjectSpecifyingThing):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(self, limit=None, uri=None):
        """ initialise instance of DatasetVariable(DataObjectSpecifyingThing).

        It will be used to set up a sparql query, and get all metadata of DatasetVariable from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select DatasetVariable:
        - with ICOS CP 'uri'

        Example:
            DatasetVariable(limit=5)

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
        self._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/DatasetVariable'

        #
        self._objtype = None
        if self._object is not None:
            self.objtype = self._getObjectType()

        # get instance name
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self._instance_name = text[:text.find('=')].strip()


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': DatasetVariable(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
