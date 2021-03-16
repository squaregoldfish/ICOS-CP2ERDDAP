#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# dataObject.py

"""
    The dataObject module is used to explore ICOS CP DataObjects' metadata.

    Example usage:

    From dataObject import DataObject

    dataObjects = DataObject()        # initialise ICOS CP DataObject object
    dataObjects.get_meta()            # get dataObjects' metadata from ICOS CP
    dataObjects.show()                # print dataObjects' metadata
    dataobjects.download()            # download every files associated with dataobjects selected
"""

# --- import -----------------------------------
# import from standard lib
from pathlib import Path
import logging
import traceback
import re
from pprint import pformat
# import from other lib
import requests
from requests.exceptions import HTTPError
# import from my project
import icp2edd.setupcfg as setupcfg
from icp2edd.cpmeta.staticObject import StaticObject

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

# object attributes' dictionary with RDF 'property' as key and RDF 'object' as value
#   RDF triples: 'subject' + 'property/predicate' + 'object/value'
# {'property/predicate': 'object/value'}
# Note: 'object/value' will be the output attribute name
_attr = {
    'cpmeta:hasActualVariable': 'variable',
    'cpmeta:hasFormatSpecificMetadata': 'format',
    'cpmeta:hasKeyword': 'keyword',
    'cpmeta:hasKeywords': 'keywords',
    'cpmeta:hasObjectSpec': 'specification',  # Data Object specification
    'cpmeta:hasSpatialCoverage': 'location',
    'cpmeta:hasTemporalResolution': 'temporal_resolution',  # time_coverage_resolution ?
    'cpmeta:hasVariableName': 'variable_name'
}
# list of equivalent class
_equivalentClass = ['SimpleDataObject', 'SpatialDataObject']


# ----------------------------------------------
class DataObject(StaticObject):
    """
    >>> t.getMeta()
    >>> t.show(True)
    >>> t._queryString()
    """

    def __init__(self, limit=None, submfrom=None, submuntil=None, product=None, lastversion=None, uri=None):
        """ initialise instance of DataObject(StaticObject).

        It will be used to set up a sparql query, and get all metadata of DataObject from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select DataObject:
        - submitted from 'submfrom'
        - submitted until 'submuntil'
        - of data type 'product'
        - only from the 'lastversion'
        - with ICOS CP 'uri'

        Example:
            DataObject(submfrom='2020-01-01T00:00:00.000Z',
                       submuntil='2020-01-05T00:00:00.000Z',
                       product='icosOtcL1Product_v2',
                       lastversion=False )

        :param limit: number of returned results
        :param submfrom: submitted from date ( '2020-01-01T00:00:00.000Z' )
        :param submuntil: submitted until date ( '2020-01-01T00:00:00.000Z' )
        :param product: select this product type ('icosOtcL1Product_v2'), it could be a list
        :param lastversion: select only last release [True,False]
        :param uri: ICOS CP URI ('https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z')
        """
        super().__init__()
        # set up class/instance variables
        self._uri = uri
        self._limit = limit
        self._from = submfrom
        self._until = submuntil
        self._product = product
        self._lastversion = lastversion

        # object attributes' dictionary
        if isinstance(_attr, dict):
            self.attr = {**_attr, **self.attr}

        if isinstance(_equivalentClass, list):
            self._equivalentClass = _equivalentClass

        # object type URI
        self._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/DataObject'

        #
        self._objtype = None
        if self._object is not None:
            self.objtype = self._getObjectType()

        # get instance name
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self._instance_name = text[:text.find('=')].strip()

    def download(self):
        """ download file associated to dataobject

        download every file associated with the dataobjects selected on ICOS CP,
        and store them on a temporary directory named by the dataset 'name'

        :return: dictionary with csv file as key, and dirout as value

        >>> t.getMeta()
        >>> output = t.download()
        download file  https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z  on
            .../58GS20190711_SOCAT_enhanced/58GS20190711_SOCAT_enhanced.csv
        """
        d = {}
        for uri, binding in self.meta.items():
            # there is at least one binding covering the optional "opt", too
            # uri = binding['uri'].value  # Warning do not convert to Path (https:// => https./)
            pid = uri.split("/")[-1]
            # Warning: linked to staticObject.py 'cpmeta:hasName': 'filename'
            if 'filename' not in binding:
                _logger.critical(f"can not find 'filename' attribute in binding.\n "
                                 f"Check value of 'cpmeta:hasName' in StaticObject")

            if len(binding['filename']) > 1:
                _logger.critical(f"several filenames associated to one uri, meta:\n{pformat(binding)}")
            else:
                # replace white space(s) by underscore
                filename = Path(re.sub('\s+', '_', binding['filename'][0].value))
                stemname = filename.stem

                dirout = setupcfg.datasetCsvPath / stemname
                try:
                    dirout.mkdir(parents=True)
                except FileExistsError:
                    # directory already exists
                    pass

                url = str(uri).replace('meta', 'data')
                fileout = dirout / filename
                if filename not in d:
                    # download
                    d[filename] = dirout

                    cookies = dict(CpLicenseAcceptedFor=pid)
                    # Fill in your details here to be posted to the login form.
                    # user, pswd = 'julien.paul at uib.no', 'Lw9ucQr5EEQ9SaK'

                    # Use 'with' to ensure the session context is closed after use.
                    _logger.info(f'downloading file {uri} on {fileout}')
                    with requests.Session() as s:
                        # LOGIN_URL = 'https://cpauth.icos-cp.eu/login/'
                        # p = s.post(LOGIN_URL, data={user : pswd})
                        # print the html returned or something more intelligent to see if it's a successful login page.
                        # print('html return ')#, p.text)

                        # TODO use this 'try except else' format everywhere
                        try:
                            # an authorised request.
                            # r = s.get(url, auth=(user,pswd), stream=True)
                            # r = s.get(url, auth=HTTPDigestAuth(user, pswd), stream=True)
                            r = s.get(str(url), cookies=cookies, stream=True)
                            # If the response was successful, no Exception will be raised
                            r.raise_for_status()
                        except HTTPError as http_err:
                            # https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
                            # raise HTTPError(f'HTTP error occurred: {http_err}')  # Python 3.6
                            _logger.exception(f'HTTP error occurred: {http_err}')
                            raise  #
                        except Exception as err:
                            # raise Exception(f'Other error occurred: {err}')  # Python 3.6
                            _logger.exception(f'Other error occurred: {err}')
                            raise  #
                        else:
                            # Success!
                            _logger.info(f'download completed, output on {fileout}')
                            # perc = float(i) / ?? * 100
                            # print(f'downloading file {uri} [{perc}%] on {fileout}', end='')
                            # print('Downloading File FooFile.txt [%d%%]\r'%i, end="")
                            with open(fileout, 'wb') as f:
                                for chunk in r.iter_content(chunk_size=1024):
                                    if chunk:  # filter out keep-alive new chunks
                                        f.write(chunk)

        return d


if __name__ == '__main__':
    import doctest

    uri = 'https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z'
    setupcfg.main()
    doctest.testmod(extraglobs={'t': DataObject(uri=uri), 'datasetCsvPath': setupcfg.datasetCsvPath},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
