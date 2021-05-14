#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# station.py

"""
    The station module is used to explore ICOS CP Stations' metadata.

    Example usage:

    From station import Station

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
from icp2edd.cpmeta.organization import Organization

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

# object attributes' dictionary with RDF 'property' as key and RDF 'object' as value
#   RDF triples: 'subject' + 'property/predicate' + 'object/value'
# {'property/predicate': 'object/value'}
# Note: 'object/value' will be the output attribute name
_attr = {
    'cpmeta:belongsToTheNetworkOf': 'thematic_center',
    'cpmeta:country': 'country',
    'cpmeta:countryCode': 'country_code',
    'cpmeta:hasAncillaryEntry': 'ancillary_entry',
    'cpmeta:hasClimateZone': 'climate_zone',
    'cpmeta:hasDocumentationObject': 'documentation',
    'cpmeta:hasEasternBound': 'eastern_bound',
    'cpmeta:hasElevation': 'elevation',
    'cpmeta:hasFunding': 'funding',
    'cpmeta:hasLatitude': 'latitude',
    'cpmeta:hasLongitude': 'longitude',
    'cpmeta:hasMeanAnnualTemp': 'mean_annual_temperature',
    'cpmeta:hasNorthernBound': 'northern_bound',
    'cpmeta:hasOperationalPeriod': 'operational_period',
    'cpmeta:hasResponsibleOrganization': 'organization',
    'cpmeta:hasSouthernBound': 'southern_bound',
    'cpmeta:hasSpatialCoverage': 'location',
    'cpmeta:hasStationClass': 'class',
    'cpmeta:hasStationId': 'id',
    'cpmeta:hasStationSpecificParam': 'specific_parameter',
    'cpmeta:hasWesternBound': 'western_bound',
    'cpmeta:operatesOn': 'station_Site'
}
# list of equivalent class
_equivalentClass = []


# ----------------------------------------------
class Station(Organization):
    """
    >>> t.getMeta()
    >>> t.show(True)

    """

    def __init__(self, limit=None, uri=None):
        """ initialise instance of Station(ICPObj).

        It will be used to set up a sparql query, and get all metadata of Station from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select Station:
        - with ICOS CP 'uri'

        Example:
            Station(limit=5)

        :param limit: number of returned results
        :param uri: ICOS CP URI ('https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z')
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

        if isinstance(_equivalentClass, list):
            self._equivalentClass = _equivalentClass

        # object type URI
        self._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/Station'

        #
        self._objtype = None
        if self._object is not None:
            self.objtype = self._getObjectType()

        # get instance name
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self._instance_name = text[:text.find('=')].strip()


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': Station(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
