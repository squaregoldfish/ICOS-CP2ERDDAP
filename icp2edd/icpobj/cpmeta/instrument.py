#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# instrument.py

"""
    The instrument module is used to explore ICOS CP cpmeta::Instruments' metadata.

    Example usage:

    from cpmeta import Instrument

    instruments = Instrument()        # initialise ICOS CP Instrument object
    instruments.get_meta()            # get instruments' metadata from ICOS CP
    instruments.show()                # print instruments' metadata
"""

# --- import -----------------------------------
# import from standard lib
import logging
import traceback

# import from other lib
# import from my project
from icp2edd.icpobj.sosa import Sensor

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

# object attributes' dictionary with RDF 'property' as key and RDF 'object' as value
#   RDF triples: 'subject' + 'property/predicate' + 'object/value'
# {'property/predicate': 'object/value'}
# Note: 'object/value' will be the output attribute name
_attr = {
    "cpmeta:hasInstrumentOwner": "owner",  # cpmeta/Organization
    "ssn:hasSubSystem": "subsystem",  #
    # subproperty {
    # "cpmeta:hasInstrumentComponent": "component",  # cpmeta/Instrument
    # }
    "cpmeta:hasVendor": "vendor",  # cpmeta/Organization
    "cpmeta:hasModel": "model",  # xsd:string
    "cpmeta:hasSerialNumber": "serial_number",  # xsd:string
}
# list of equivalent class
_equivalentClass = ["cpmeta.Organization"]


# ----------------------------------------------
class Instrument(Sensor):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(self, limit=None, uri=None):
        """initialise instance of Instrument(Sensor, Organization).

        It will be used to set up a sparql query, and get all metadata of Instrument from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select Instrument:
        - with ICOS CP 'uri'

        Example:
            Instrument(limit=5)

        :param limit: number of returned results
        :param uri: ICOS CP URI ('http://meta.icos-cp.eu/resources/instruments/ATC_283')
        """
        super().__init__()
        # set up class/instance variables
        self._uri = uri
        self._limit = limit

        # inherit properties
        self._inherit = {**self.attr}

        if isinstance(_attr, dict):
            # keep own properties
            self._attr = _attr
            # merge own and inherit properties.
            # Note:  .attr's values are overwritten by the self.attr's
            self.attr = {**self._attr, **self._inherit}
            # add subproperties
            for prop in self.attr:
                self._addSubProperties(prop)

        if isinstance(_equivalentClass, list):
            self._equivalentClass = _equivalentClass

        # object type URI
        self._object = "http://meta.icos-cp.eu/ontologies/cpmeta/Instrument"

        #
        self._objtype = None
        if self._object is not None:
            self.objtype = self._getObjectType()

        # get instance name
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self._instance_name = text[: text.find("=")].strip()


if __name__ == "__main__":
    import doctest

    doctest.testmod(
        extraglobs={"t": Instrument(limit=10)},
        optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
    )


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
