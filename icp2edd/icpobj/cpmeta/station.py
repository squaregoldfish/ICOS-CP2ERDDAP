#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# station.py

"""
    The station module is used to explore ICOS CP cpmeta::Stations' metadata.

    Example usage:

    from cpmeta import Station

    stations = Station()           # initialise ICOS CP Station object
    stations.get_meta()            # get stations' metadata from ICOS CP
    stations.show()                # print stations' metadata
"""

# --- import -----------------------------------
# import from standard lib
import logging
import traceback

# import from other lib
# import from my project
from icp2edd.icpobj.cpmeta.organization import Organization

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

# object attributes' dictionary with RDF 'property' as key and RDF 'object' as value
#   RDF triples: 'subject' + 'property/predicate' + 'object/value'
# {'property/predicate': 'object/value'}
# Note: 'object/value' will be the output attribute name
_attr = {
    "cpmeta:belongsToTheNetworkOf": "thematic_center",  # cpmeta/ThematicCenter
    "cpmeta:hasAncillaryEntry": "ancillary_entry",  # cpmeta/AncillaryEntry
    "cpmeta:hasResponsibleOrganization": "organization",  # cpmeta/Organization
    "cpmeta:hasStationSpecificParam": "specific_parameter",  # rdfs:Literal
    # subproperty {
    # "cpmeta:country": "country",  # xsd:string
    # "cpmeta:countryCode": "country_code",  # xsd:string
    # "cpmeta:hasStationClass": "class",  # rdfs:Datatype
    # "cpmeta:hasStationId": "id",  # xsd:string
    # "cpmeta:hasOperationalPeriod": "operational_period",  # xsd:string
    # "cpmeta:hasLabelingDate": "label_date",  # xsd:date
    # "cpmeta:hasMeanAnnualTemp": "mean_annual_temperature",  # xsd:float
    # "cpmeta:hasMeanAnnualPrecip": "mean_annual_precip",  # xsd:float
    # "cpmeta:hasMeanAnnualRadiation": "mean_annual_radiation",  # xsd:float
    # "cpmeta:hasTimeZoneOffset": "time_zone_offset",  # xsd:integer
    # }
    "cpmeta:hasClimateZone": "climate_zone",  # cpmeta/ClimateZone
    "terms:bibliographicCitation": "bibliographic_citation",  # rdfs:Literal
    # subproperty {
    # "cpmeta:hasAssociatedPublication": "associated_publication",  # xsd:anyURI
    # "cpmeta:hasDocumentationUri": "documentation_uri",  # xsd:anyURI
    # }
    "cpmeta:hasDocumentationObject": "documentation",  # cpmeta/DocumentObject
    "cpmeta:hasElevation": "elevation",  # xsd:float
    "cpmeta:hasFunding": "funding",  # cpmeta/Funding
    "cpmeta:hasSpatialCoverage": "location",  # cpmeta/SpatialCoverage
    "cpmeta:latlongs": "latlongs",  # xsd:double
    # subproperty {
    # "cpmeta:hasLatitude": "latitude",  # xsd:double
    # "cpmeta:hasLongitude": "longitude",  # xsd:double
    # }
    "prov:atLocation": "at_location",  #
    # subproperty {
    # "cpmeta:operatesOn": "station_Site",  # cpmeta/Site
    # }
}
# list of equivalent class
_equivalentClass = ["cpmeta.LatLonBox"]

# sites/Station             is subClassOf cpmeta/Station
# cpmeta/IcosStation        is subClassOf cpmeta/Station
# cpmeta/IngosStation       is subClassOf cpmeta/Station
# cpmeta/WdcggStation       is subClassOf cpmeta/Station
# cpmeta/FluxnetStation     is subClassOf cpmeta/Station
# cpmeta/AtmoStation        is subClassOf cpmeta/Station
# cpmeta/SailDrone          is subClassOf cpmeta/Station
# cpmeta/NeonStation        is subClassOf cpmeta/Station

# ----------------------------------------------
class Station(Organization):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(self, limit=None, uri=None):
        """initialise instance of Station(ICPObj).

        It will be used to set up a sparql query, and get all metadata of Station from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select Station:
        - with ICOS CP 'uri'

        Example:
            Station(limit=5)

        :param limit: number of returned results
        :param uri: ICOS CP URI ('http://meta.icos-cp.eu/resources/wdcgg/station/Pacific%20Ocean%20')
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
        self._object = "http://meta.icos-cp.eu/ontologies/cpmeta/Station"

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
        extraglobs={"t": Station(limit=10)},
        optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
    )


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
