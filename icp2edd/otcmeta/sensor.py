#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# sensor.py

"""
    The sensor module is used to explore ICOS CP Sensors' metadata.

    Example usage:

    From sensor import Sensor

    sensors = Sensor()        # initialise ICOS CP Sensor object
    sensors.get_meta()        # get sensors' metadata from ICOS CP
    sensors.show()            # print sensors' metadata
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
    'otcmeta:hasManufacturer': 'Manufacturer',
    'otcmeta:hasModelName': 'modelName',
    'otcmeta:hasName': 'name',
    'otcmeta:hasReportingFrequency': 'reportingFrequency',
    'otcmeta:hasSamplingFrequency': 'samplingFrequency ',
    'otcmeta:hasSerialNumber': 'serialNumber',
    'otcmeta:measuresVariable': 'MeasuresVariable'
}


# ----------------------------------------------
class Sensor(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show()
    """

    def __init__(self, limit=None, uri=None):
        """ initialise instance of Sensor(ICPObj).

        It will be used to set up a sparql query, and get all metadata of Sensor from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select Sensor:
        - with ICOS CP 'uri'

        Example:
            Sensor(limit=5)

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
        self._object = 'http://meta.icos-cp.eu/ontologies/otcmeta/Sensor'


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': Sensor(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
