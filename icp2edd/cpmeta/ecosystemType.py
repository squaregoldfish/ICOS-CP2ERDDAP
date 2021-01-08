#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ecosystemType.py

"""
    The ecosystemType module is used to explore ICOS CP EcosystemTypes' metadata.

    Example usage:

    From ecosystemType import EcosystemType

    ecosystemTypes = EcosystemType()     # initialise ICOS CP EcosystemType object
    ecosystemTypes.get_meta()            # get ecosystemTypes' metadata from ICOS CP
    ecosystemTypes.show()                # print ecosystemTypes' metadata
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
    'cpmeta:broaderEcosystem': 'EcosystemType'
}


# ----------------------------------------------
class EcosystemType(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(self, limit=None, uri=None):
        """ initialise instance of EcosystemType(ICPObj).

        It will be used to set up a sparql query, and get all metadata of EcosystemType from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select EcosystemType:
        - with ICOS CP 'uri'

        Example:
            EcosystemType(limit=5)

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
        self._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/EcosystemType'


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': EcosystemType(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
