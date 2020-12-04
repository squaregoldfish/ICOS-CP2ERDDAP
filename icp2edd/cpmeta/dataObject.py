#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# dataObject.py

"""
    The dataObject module is used to explore ICOS CP DataObjects' metadata.

    Example usage:

    From dataObject import DataObject

    dataobjects = DataObject()      # initialise ICOS CP DataObject object
    dataobjects.get_meta()          # get dataobjects' metadata from ICOS CP
    dataobjects.show()              # print dataobjects' metadata
    dataobjects.download()          # download every files associated with dataobjects selected
"""

# --- import -----------------------------------
# import from standard lib
from pathlib import Path
import logging
# import from other lib
import requests
from requests.exceptions import HTTPError
# import from my project
import icp2edd.setup as setup
from icp2edd.cpmeta.staticObject import StaticObject

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

# object attributes' dictionary with RDF 'property' as key and RDF 'object' as value
#   RDF triples: 'subject' + 'property/predicate' + 'object/value'
# {'property/predicate': 'object/value'}
# Note: 'object/value' will be the output attribute name
_attr = {
    'cpmeta:hasObjectSpec': 'DataObjectSpec',
    'cpmeta:wasAcquiredBy': 'DataAcquisition',
    'cpmeta:wasProducedBy': 'DataProduction',
    'cpmeta:hasFormatSpecificMetadata': 'formatSpecificMetadata',
    'cpmeta:hasKeyword': 'keyword',
    'cpmeta:hasVariableName': 'variableName',
    'cpmeta:hasActualVariable': 'VariableInfo',
    'cpmeta:hasTemporalResolution': 'temporalResolution',
    'cpmeta:hasSpatialCoverage': 'SpatialCoverage'
}


# ----------------------------------------------
class DataObject(StaticObject):
    """
    >>> t.getMeta()
    >>> t.show()
    <BLANKLINE>
    type: <class '__main__.DataObject'>
    <BLANKLINE>
    Class name: xxx
    <BLANKLINE>
    \tDataObjectSpec      : type: uri        value: ...
    \tDataAcquisition     : type: uri        value: ...
    \tDataProduction      : type: uri        value: ...
    \tSpatialCoverage     : type: uri        value: ...
    \tsizeInBytes         : type: literal    value: ...
    \tsha256sum           : type: literal    value: ...
    \tcitation            : type: literal    value: ...
    \tname                : type: literal    value: ...
    \tDataSubmission      : type: uri        value: ...
    \turi                 : type: uri        value: ...

    >>> tt = DataObject(lastupdate='2020-01-01T00:00:00.000Z',
    ...                 endupdate='2020-11-01T00:00:00.000Z',
    ...                 product='icosOtcL1Product_v2',
    ...                 lastversion=True)
    >>> tt.getMeta()
    >>> tt.show()
    <BLANKLINE>
    type: <class '__main__.DataObject'>
    <BLANKLINE>
    Class name: xxx
    <BLANKLINE>
    ...
    \tDataObjectSpec      : type: uri        value: ...
    \tDataAcquisition     : type: uri        value: ...
    \tDataProduction      : type: uri        value: ...
    \tSpatialCoverage     : type: uri        value: ...
    \tsizeInBytes         : type: literal    value: ...
    \tsha256sum           : type: literal    value: ...
    \tcitation            : type: literal    value: ...
    \tname                : type: literal    value: ...
    \tDataSubmission      : type: uri        value: ...
    \turi                 : type: uri        value: ...
    ...
    """

    def __init__(self, limit=None, lastupdate=None, endupdate=None, product=None, lastversion=None, uri=None):
        """ initialise instance of DataObject(StaticObject).

        It will be used to set up a sparql query, and get all metadata of DataObject from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select DataObject:
        - submitted since 'lastupdate'
        - submitted until 'endupdate'
        - of data type 'product'
        - only from the 'lastversion'
        - with ICOS CP 'uri'

        Example:
            DataObject(lastupdate='2020-01-01T00:00:00.000Z',
                    endupdate='2020-01-05T00:00:00.000Z',
                    product='icosOtcL1Product_v2',
                    lastversion=False )

        :param limit: number of returned results
        :param lastupdate: submitted since last update ( '2020-01-01T00:00:00.000Z' )
        :param endupdate: submitted until end update ( '2020-01-01T00:00:00.000Z' )
        :param product: select this product type ('icosOtcL1Product_v2'), it could be a list
        :param lastversion: select only last release [True,False]
        :param uri: ICOS CP URI ('https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z')
        """
        super().__init__()
        # set up class/instance variables
        self._uri = uri
        self._limit = limit
        self._lastupdate = lastupdate
        self._endupdate = endupdate
        self._product = product
        self._lastversion = lastversion

        # object attributes' dictionary
        if isinstance(_attr, dict):
            self._attr = {**_attr, **self._attr}

        # object type URI
        self._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/DataObject'

    def download(self):
        """ download file associated to dataobject

        download every file associated with the dataobjects selected on ICOS CP,
        and store them on local directory named by the dataset 'name'

        :return: dictionary with csv file as key, and dirout as value

        >>> t.getMeta()
        >>> output = t.download()
        download file  https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z  on
            .../58GS20190711_SOCAT_enhanced/58GS20190711_SOCAT_enhanced.csv
        """

        d = {}
        for _, val in self.meta.items():

            uri = val['uri'].value  # Warning do not convert to Path (https:// => https./)
            pid = uri.split("/")[-1]
            filename = Path(val['name'].value)
            stemname = filename.stem

            dirout = setup.datasetCsvPath / stemname
            try:
                dirout.mkdir(parents=True)
            except FileExistsError:
                # directory already exists
                pass

            url = str(uri).replace('meta', 'data')
            fileout = dirout / filename
            d[filename] = dirout

            cookies = dict(CpLicenseAcceptedFor=pid)
            # Fill in your details here to be posted to the login form.
            # user, pswd = 'julien.paul@uib.no', 'Lw9ucQr5EEQ9SaK'

            # Use 'with' to ensure the session context is closed after use.
            with requests.Session() as s:
                # LOGIN_URL = 'https://cpauth.icos-cp.eu/login/'
                # p = s.post(LOGIN_URL, data={user : pswd})
                # print the html returned or something more intelligent to see if it's a successful login page.
                # print('html return ')#, p.text)

                # TODO check error case
                # TODO use this 'try except else' format everywhere
                try:
                    # an authorised request.
                    # r = s.get(url, auth=(user,pswd), stream=True)
                    # r = s.get(url, auth=HTTPDigestAuth(user, pswd), stream=True)
                    r = s.get(str(url), cookies=cookies, stream=True)
                    # If the response was successful, no Exception will be raised
                    r.raise_for_status()
                except HTTPError:  # as http_err:
                    # https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
                    # raise HTTPError(f'HTTP error occurred: {http_err}')  # Python 3.6
                    _logger.exception(f'HTTP error occurred:')
                    raise  #
                except Exception:  # as err:
                    # raise Exception(f'Other error occurred: {err}')  # Python 3.6
                    _logger.exception(f'Other error occurred:')
                    raise  #
                else:
                    # Success!
                    _logger.info(f'download file {uri} on {fileout}')
                    with open(fileout, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:  # filter out keep-alive new chunks
                                f.write(chunk)

        return d


if __name__ == '__main__':
    import doctest

    uri = 'https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z'
    setup.main()
    doctest.testmod(extraglobs={'t': DataObject(uri=uri), 'datasetCsvPath': setup.datasetCsvPath},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
