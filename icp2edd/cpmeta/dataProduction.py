#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# dataProduction.py

"""
    The dataProduction module is used to explore ICOS CP DataProductions' metadata.

    Example usage:

    From dataProduction import DataProduction

    dataProductions = DataProduction()    # initialise ICOS CP DataProduction object
    dataProductions.get_meta()            # get dataProductions' metadata from ICOS CP
    dataProductions.show()                # print dataProductions' metadata
"""

# --- import -----------------------------------
# import from standard lib
import logging
import traceback
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
    'cpmeta:wasPerformedAt': 'feature',
    'prov:endedAtTime': 'ended_at_time',
    'prov:startedAtTime': 'started_at_time',
    'prov:wasAssociatedWith': 'thematic_center'
}
# list of equivalent class
_equivalentClass = []


# ----------------------------------------------
class DataProduction(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(self, limit=None, uri=None):
        """ initialise instance of DataProduction(ICPObj).

        It will be used to set up a sparql query, and get all metadata of DataProduction from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select DataProduction:
        - with ICOS CP 'uri'

        Example:
            DataProduction(limit=5)

        :param limit: number of returned results
        :param uri: ICOS CP URI ('https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z')
        """
        super().__init__()
        # set up class/instance variables
        self._uri = uri
        self._limit = limit

        # object attributes' dictionary
        if isinstance(_attr, dict):
            self.attr = {**_attr, **self.attr}

        if isinstance(_equivalentClass, list):
            self._equivalentClass = _equivalentClass

        # object type URI
        self._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/DataProduction'

        #
        self._objtype = None
        if self._object is not None:
            self.objtype = self._getObjectType()

        # get instance name
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self._instance_name = text[:text.find('=')].strip()


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': DataProduction(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
