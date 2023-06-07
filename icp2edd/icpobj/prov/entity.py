#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# entity.py

"""
    The entity module is used to explore prov::Entitys' metadata.

    Example usage:

    from prov import Activity

    entitys = Entity()    # initialise ICOS CP Entity object
    entitys.get_meta()            # get entitys' metadata from ICOS CP
    entitys.show()                # print entitys' metadata
"""

# --- import -----------------------------------
# import from standard lib
import logging
import traceback

# import from other lib
# import from my project
from icp2edd.icpobj import ICPObj

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

# object attributes' dictionary with RDF 'property' as key and RDF 'object' as value
#   RDF triples: 'subject' + 'property/predicate' + 'object/value'
# {'property/predicate': 'object/value'}
# Note: 'object/value' will be the output attribute name
_attr = {
    "prov:wasRevisionOf": "NextVersionOf",  # prov#Entity
    # subproperty {
    # "cpmeta:isNextVersionOf": "NextVersionOf",  # prov#Entity
    # Warning: linked to:
    # - superIcpObj.py:_getSubAttr(): elif k in 'NextVersionOf':
    # }
    "prov:wasGeneratedBy": "activity",  # prov#Activity
    # subproperty {
    # "cpmeta:wasAcquiredBy": "acquisition",  # cpmeta/DataAcquisition
    # "cpmeta:wasProducedBy": "production",  # cpmeta/DataProduction
    # "cpmeta:wasSubmittedBy": "submission",  # cpmeta/DataSubmission
    # }
    "prov:hadPrimarySource": "PrimarySource",  # prov#Entity
    # Warning: linked to:
    # - superIcpObj.py:_getSubAttr(): elif k in 'PrimarySource':
    # subproperty {
    # "cpmeta:hasName": "name",  # xsd:string
    # "cpmeta:hasVariableTitle": "variable_title",  # xsd:string
    #   subproperty {
    # "cpmeta:hasColumnTitle": "column_title",  # xsd:string
    #   }
    # }
}
# list of equivalent class
_equivalentClass = []

# cpmeta/Collection     is subClassOf prov#Entity
# cpmeta/StaticObject   is subClassOf prov#Entity

# ----------------------------------------------
class Entity(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(self, limit=None, uri=None):
        """initialise instance of Activity(ICPObj).

        It will be used to set up a sparql query, and get all metadata of Entity from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select Entity:
        - with ICOS CP 'uri'

        Example:
            Entity(limit=5)

        :param limit: number of returned results
        :param uri: ICOS CP 'uri'
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
        self._object = "http://www.w3.org/ns/prov#Entity"
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
        extraglobs={"t": Entity(limit=10)},
        optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
    )


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
