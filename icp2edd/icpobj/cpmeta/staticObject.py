#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# staticObject.py

"""
    The staticObject module is used to explore ICOS CP cpmeta::StaticObjects' metadata.

    Example usage:

    from cpmeta import StaticObject

    staticObjects = StaticObject()      # initialise ICOS CP StaticObject object
    staticObjects.get_meta()            # get staticObjects' metadata from ICOS CP
    staticObjects.show()                # print staticObjects' metadata
"""

# --- import -----------------------------------
# import from standard lib
import logging
import traceback

# import from other lib
# import from my project
from icp2edd.icpobj.prov import Entity

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

# object attributes' dictionary with RDF 'property' as key and RDF 'object' as value
#   RDF triples: 'subject' + 'property/predicate' + 'object/value'
# {'property/predicate': 'object/value'}
# Note: 'object/value' will be the output attribute name
_attr = {
    "cpmeta:hasSha256sum": "sha256_sum",  # xsd:hexBinary
    "cpmeta:hasSizeInBytes": "size_in_bites",  # xsd:long
    "cpmeta:hasCitationString": "citation",  # xsd:string
    "cpmeta:hasDoi": "doi",  # xsd:string
    "cpmeta:hasName": "filename",  # xsd:string
    # Note: overwrite the value from Entity
    # Warning: linked to:
    # - dataObject.py: filename = Path(val['static_object_name'].value)
    # - superIcpObj.py: fname = self.m['DataObject'][k]['static_object_name'...
    #
    "cpmeta:hasBiblioInfo": "biblio_info",  #
}
# list of equivalent class
_equivalentClass = []

# cpmeta/DataObject         is subClassOf cpmeta/StaticObject
# cpmeta/DocumentObject     is subClassOf cpmeta/StaticObject
#

# ----------------------------------------------
class StaticObject(Entity):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(
        self, limit=None, submfrom=None, submuntil=None, lastversion=None, uri=None
    ):
        """initialise instance of StaticObject(ICPObj).

        It will be used to set up a sparql query, and get all metadata of StaticObject from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select StaticObject:
        - submitted from 'submfrom'
        - submitted until 'submuntil'
        - only from the 'lastversion'
        - with ICOS CP 'uri'

        Example:
            StaticObject(limit=5)

        :param limit: number of returned results
        :param submfrom: submitted from date ( '2020-01-01T00:00:00.000Z' )
        :param submuntil: submitted until date ( '2020-01-01T00:00:00.000Z' )
        :param lastversion: select only last release [True,False]
        :param uri: ICOS CP URI
        """
        super().__init__()
        # set up class/instance variables
        self._uri = uri
        self._limit = limit
        self._from = submfrom
        self._until = submuntil
        self._lastversion = lastversion

        # inherit properties
        self._inherit = {**self.attr}

        if isinstance(_attr, dict):
            # keep own properties
            self._attr = _attr
            # merge own and inherit properties.
            # Note:  inherit's values are overwritten by the _attr's
            self.attr = {**self._inherit, **self._attr}
            # add subproperties
            for prop in self.attr:
                self._addSubProperties(prop)

        if isinstance(_equivalentClass, list):
            self._equivalentClass = _equivalentClass

        # object type URI
        self._object = "http://meta.icos-cp.eu/ontologies/cpmeta/StaticObject"

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
        extraglobs={"t": StaticObject(limit=10)},
        optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
    )


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
