#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# documentObject.py

"""
    The documentObject module is used to explore ICOS CP cpmeta::DocumentObjects' metadata.

    Example usage:

    from cpmeta import DocumentObject

    documentObjects = DocumentObject()    # initialise ICOS CP DocumentObject object
    documentObjects.get_meta()            # get documentObjects' metadata from ICOS CP
    documentObjects.show()                # print documentObjects' metadata
"""

# --- import -----------------------------------
# import from standard lib
import logging
import traceback

# import from other lib
# import from my project
from icp2edd.icpobj.cpmeta.staticObject import StaticObject

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

# object attributes' dictionary with RDF 'property' as key and RDF 'object' as value
#   RDF triples: 'subject' + 'property/predicate' + 'object/value'
# {'property/predicate': 'object/value'}
# Note: 'object/value' will be the output attribute name
_attr = {}
# list of equivalent class
_equivalentClass = []


# ----------------------------------------------
class DocumentObject(StaticObject):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(
        self, limit=None, submfrom=None, submuntil=None, lastversion=None, uri=None
    ):
        """initialise instance of DocumentObject(StaticObject).

        It will be used to set up a sparql query, and get all metadata of DocumentObject from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select DocumentObject:
        - submitted from 'submfrom'
        - submitted until 'submuntil'
        - only from the 'lastversion'
        - with ICOS CP 'uri'

        Example:
            DocumentObject(limit=5)

        :param limit: number of returned results
        :param submfrom: submitted from date ( '2020-01-01T00:00:00.000Z' )
        :param submuntil: submitted until date ( '2020-01-01T00:00:00.000Z' )
        :param lastversion: select only last release [True,False]
        :param uri: ICOS CP URI ('https://meta.fieldsites.se/objects/0gBYH7QTXlCebkAGhE0iKc4v')
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
            # Note:  .attr's values are overwritten by the self.attr's
            self.attr = {**self._attr, **self._inherit}
            # add subproperties
            for prop in self.attr:
                self._addSubProperties(prop)

        if isinstance(_equivalentClass, list):
            self._equivalentClass = _equivalentClass

        # object type URI
        self._object = "http://meta.icos-cp.eu/ontologies/cpmeta/DocumentObject"

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
        extraglobs={"t": DocumentObject(limit=10)},
        optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
    )


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
