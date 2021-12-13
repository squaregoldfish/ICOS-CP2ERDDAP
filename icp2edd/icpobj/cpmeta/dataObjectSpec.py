#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# dataObjectSpec.py

"""
    The dataObjectSpec module is used to explore ICOS CP cpmeta::DataObjectSpecs' metadata.

    Example usage:

    from cpmeta import DataObjectSpec

    dataObjectSpecs = DataObjectSpec()    # initialise ICOS CP DataObjectSpec object
    dataObjectSpecs.get_meta()            # get dataObjectSpecs' metadata from ICOS CP
    dataObjectSpecs.show()                # print dataObjectSpecs' metadata
"""

# --- import -----------------------------------
# import from standard lib
import logging
import traceback

# import from other lib
# import from my project
from icp2edd.icpobj.cpmeta.dataObjectSpecifyingThing import DataObjectSpecifyingThing

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

# object attributes' dictionary with RDF 'property' as key and RDF 'object' as value
#   RDF triples: 'subject' + 'property/predicate' + 'object/value'
# {'property/predicate': 'object/value'}
# Note: 'object/value' will be the output attribute name
_attr = {
    "cpmeta:hasAssociatedProject": "project",  # cpmeta/Project
    "cpmeta:hasDataTheme": "data_theme",  # cpmeta/DataTheme
    "terms:format": "terms_format",  #
    # subproperty {
    # "cpmeta:hasEncoding": "encoding",  # cpmeta/ObjectEncoding
    # "cpmeta:hasFormat": "format",  # cpmeta/ObjectFormat
    # }
    "cpmeta:hasDataLevel": "data_level",  # Data level according to ICOS classification ?
    "cpmeta:containsDataset": "dataset",  # cpmeta/DatasetSpec
    "cpmeta:hasDocumentationObject": "documentation",  # cpmeta/DocumentObject
    "cpmeta:hasKeywords": "keywords",  # xsd:string
}
# list of equivalent class
_equivalentClass = []


# ----------------------------------------------
class DataObjectSpec(DataObjectSpecifyingThing):
    """
    >>> t.getMeta()
    >>> t.show(True)
    """

    def __init__(self, limit=None, uri=None):
        """initialise instance of DataObjectSpec(DataObjectSpecifyingThing).

        It will be used to set up a sparql query, and get all metadata of DataObjectSpec from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select DataObjectSpec:
        - with ICOS CP 'uri'

        Example:
            DataObjectSpec(limit=5)

        :param limit: number of returned results
        :param uri: ICOS CP URI
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
        self._object = "http://meta.icos-cp.eu/ontologies/cpmeta/DataObjectSpec"

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
        extraglobs={"t": DataObjectSpec(limit=10)},
        optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
    )


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
