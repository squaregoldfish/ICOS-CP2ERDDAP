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
    'cpmeta:belongsToTheNetworkOf': 'Station_thematic_center',
    'cpmeta:country': 'station_country',
    'cpmeta:countryCode': 'station_country_code',
    'cpmeta:hasAncillaryEntry': 'Station_ancillary_entry',
    'cpmeta:hasClimateZone': 'Station_climate_zone',
    'cpmeta:hasDocumentationObject': 'Station_document_object',
    'cpmeta:hasEasternBound': 'station_eastern_bound',
    'cpmeta:hasElevation': 'station_elevation',
    'cpmeta:hasFunding': 'Station_funding',
    'cpmeta:hasLatitude': 'station_latitude',
    'cpmeta:hasLongitude': 'station_longitude',
    'cpmeta:hasMeanAnnualTemp': 'station_mean_annual_temperature',
    'cpmeta:hasNothernBound': 'station_northern_bound',
    'cpmeta:hasOperationalPeriod': 'station_operational_period',
    'cpmeta:hasResponsibleOrganization': 'Station_organization',
    'cpmeta:hasSouthernBound': 'station_southern_bound',
    'cpmeta:hasSpatialCoverage': 'Station_spatial_coverage',
    'cpmeta:hasStationClass': 'station_class',
    'cpmeta:hasStationId': 'station_id',
    'cpmeta:hasStationSpecificParam': 'station_spec_param',
    'cpmeta:hasWesternBound': 'station_western_bound',
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

        # object attributes' dictionary
        if isinstance(_attr, dict):
            self._attr = {**_attr, **self._attr}

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
