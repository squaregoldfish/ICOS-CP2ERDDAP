#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# instrument.py

"""
    The instrument module is used to explore ICOS CP Instruments' metadata.

    Example usage:

    From instrument import Instrument

    instruments = Instrument()        # initialise ICOS CP Instrument object
    instruments.get_meta()            # get instruments' metadata from ICOS CP
    instruments.show()                # print instruments' metadata
"""

# --- import -----------------------------------
# import from standard lib
import logging
# import from other lib
# import from my project
from icp2edd.cpmeta.organization import Organization

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

# object attributes' dictionary with RDF 'property' as key and RDF 'object' as value
#   RDF triples: 'subject' + 'property/predicate' + 'object/value'
# {'property/predicate': 'object/value'}
# Note: 'object/value' will be the output attribute name
_attr = {
        'cpmeta:hasInstrumentOwner': 'Owner_Organization',
        'cpmeta:hasVendor': 'Vendor_Organization',
        'cpmeta:hasModel': 'model',
        'cpmeta:hasSerialNumber': 'serialNumber',
        'cpmeta:hasName': 'name',
        'cpmeta:hasTcId': 'tcid'
}


# ----------------------------------------------
class Instrument(Organization):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(self, limit=None, uri=None):
        """ initialise instance of Instrument(Organization).

        It will be used to set up a sparql query, and get all metadata of Instrument from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select Instrument:
        - with ICOS CP 'uri'

        Example:
            Instrument(limit=5)

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
        self._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/Instrument'


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': Instrument(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
