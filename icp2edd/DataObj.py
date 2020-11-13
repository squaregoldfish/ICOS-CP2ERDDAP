#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    The DataObj module is used to explore ICOS CP dataobjs' metadata.

    Example usage:

    From DataObj import DataObj

    dataobjs = DataObj()    # initialise ICOS CP DataObj object
    dataobjs.get_meta()     # get dataobjs' metadata from ICOS CP
    dataobjs.show()         # print dataobjs' metadata
    dataobjs.download()     # download every files associated with dataobjs selected
"""

__author__ = ["Julien Paul"]
__credits__ = ""
__license__ = "CC BY-SA 4.0"
__version__ = "0.0.0"
__maintainer__ = "BCDC"
__email__ = ['julien.paul@uib.no']
__status__ = ""

# --- import -----------------------------------
# import from standard lib
from pathlib import Path
# import from other lib
import requests
from requests.exceptions import HTTPError
# import from my project
from ICPObj import ICPObj

# --- module's variables -----------------------
storage = Path('/home/jpa029/Data/ICOS2ERDDAP')


# ----------------------------------------------
class DataObj(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show()
    <BLANKLINE>
    type: <class '__main__.DataObj'>
    <BLANKLINE>
    Class name: DataObj
    <BLANKLINE>
    \tsizeInBytes         : type: literal    value: ...
    \tsha256sum           : type: literal    value: ...
    \tcitation            : type: literal    value: ...
    \tname                : type: literal    value: ...
    \tDataSubmission      : type: uri        value: ...
    \tDataObjectSpec      : type: uri        value: ...
    \tDatAcquisition      : type: uri        value: ...
    \tDataProduction      : type: uri        value: ...
    \tspatialCoverage     : type: uri        value: ...
    \turi                 : type: uri        value: ...

    >>> tt = DataObj(lastupdate='2020-01-01T00:00:00.000Z',
    ...              endupdate='2020-11-01T00:00:00.000Z',
    ...              product='icosOtcL1Product_v2',
    ...              lastversion=True)
    >>> tt.getMeta()
    >>> tt.show()
    <BLANKLINE>
    type: <class '__main__.DataObj'>
    <BLANKLINE>
    Class name: DataObj
    <BLANKLINE>
    ...
    \tsizeInBytes         : type: literal    value: ...
    \tsha256sum           : type: literal    value: ...
    \tcitation            : type: literal    value: ...
    \tname                : type: literal    value: ...
    \tDataSubmission      : type: uri        value: ...
    \tDataObjectSpec      : type: uri        value: ...
    \tDatAcquisition      : type: uri        value: ...
    \tDataProduction      : type: uri        value: ...
    \tspatialCoverage     : type: uri        value: ...
    \turi                 : type: uri        value: ...
    ...
    """

    def __init__(self, limit=None, lastupdate=None, endupdate=None, product=None, lastversion=None, uri=None):
        """
        This functions initialise instance of DataObj(ICPObj).
        Set up a sparql query to get all metadata of DataObj from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select DataObj:
        - submitted since 'lastupdate'
        - submitted until 'endupdate'
        - of data type 'product'
        - only from the 'lastversion'
        - with ICOS CP 'uri'

        Example:
            DataObj(lastupdate='2020-01-01T00:00:00.000Z',
                    endupdate='2020-01-05T00:00:00.000Z',
                    product='icosOtcL1Product_v2',
                    lastversion=False )

        :param limit: number of returned results
        :param lastupdate: submitted since last update ( '2020-01-01T00:00:00.000Z' )
        :param endupdate: submitted until end update ( '2020-01-01T00:00:00.000Z' )
        :param product: select this product type ('icosOtcL1Product_v2')
        :param lastversion: select only last release [True,False]
        :param uri: ICOS CP URI ('https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z')
        """
        super().__init__()
        # overwrite class name
        self._name = 'DataObj'
        # overwrite conventional attributes renaming dictionary
        self._convAttr = {
            'citationString': 'citation'
            }
        # overwrite query string
        self._queryString = """
            select  ?xxx ?sizeInBytes ?sha256sum ?citationString ?name ?doi ?nextVersionOf
                    ?DataSubmission ?DataObjectSpec ?DatAcquisition ?DataProduction
                    ?formatSpecificMetadata ?keyword ?variableName
                    ?actualVariable ?temporalResolution ?spatialCoverage ?label ?comment ?seeAlso
            where {
                %s # _filterObj(uri_=uri)
                %s # _filterProduct(product_=product)
                ?xxx cpmeta:hasObjectSpec ?spec . # restriction property for DataObject and/or SimpleDataObject
                ?xxx cpmeta:wasSubmittedBy [
                    prov:endedAtTime ?submTime ;
                    prov:wasAssociatedWith ?submitter
                    ] .
                %s # _filterSubmTime(datestr_=lastupdate, op_='>=')
                %s # _filterSubmTime(datestr_=endupdate, op_='<=')
                %s # _filterLastVersion(lastversion_=lastversion)

                OPTIONAL { ?xxx cpmeta:hasSizeInBytes ?sizeInBytes .}           # as subClassOf DataObject
                OPTIONAL { ?xxx cpmeta:hasSha256sum ?sha256sum .}               # as subClassOf DataObject
                OPTIONAL { ?xxx cpmeta:hasCitationString ?citationString .}     # as subClassOf DataObject
                OPTIONAL { ?xxx cpmeta:hasName ?name .}
                OPTIONAL { ?xxx cpmeta:hasDoi ?doi .}
                OPTIONAL { ?xxx cpmeta:isNextVersionOf ?nextVersionOf .}

                OPTIONAL { ?xxx cpmeta:wasSubmittedBy ?DataSubmission .}        # as subClassOf DataObject
                OPTIONAL { ?xxx cpmeta:hasObjectSpec ?DataObjectSpec .}         # domain

                OPTIONAL { ?xxx cpmeta:wasAcquiredBy ?DatAcquisition .}         # domain
                OPTIONAL { ?xxx cpmeta:wasProducedBy ?DataProduction .}         # domain

                OPTIONAL { ?xxx cpmeta:hasFormatSpecificMetadata ?formatSpecificMetadata .}
                OPTIONAL { ?xxx cpmeta:hasKeyword ?keyword . }
                OPTIONAL { ?xxx cpmeta:hasVariableName ?variableName .}
                OPTIONAL { ?xxx cpmeta:hasActualVariable ?actualVariable .}
                OPTIONAL { ?xxx cpmeta:hasTemporalResolution ?temporalResolution .}
                OPTIONAL { ?xxx cpmeta:hasSpatialCoverage ?spatialCoverage .}

                OPTIONAL { ?xxx rdfs:label ?label .}
                OPTIONAL { ?xxx rdfs:comment ?comment .}
                OPTIONAL { ?xxx rdfs:seeAlso ?seeAlso .}
            }
            %s  # _checkLimit(limit)
        """ % (self._filterObj(uri_=uri),
               self._filterProduct(product_=product),
               self._filterSubmTime(datestr_=lastupdate, op_='>='),
               self._filterSubmTime(datestr_=endupdate, op_='<='),
               self._filterLastVersion(lastversion_=lastversion),
               self._checkLimit(limit_=limit))
        #

    def download(self):
        """
        download every file associated with the dataobjs selected on ICOS CP,
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

            dirout = storage / stemname
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

                try:
                    # an authorised request.
                    # r = s.get(url, auth=(user,pswd), stream=True)
                    # r = s.get(url, auth=HTTPDigestAuth(user, pswd), stream=True)
                    r = s.get(str(url), cookies=cookies, stream=True)
                    # If the response was successful, no Exception will be raised
                    r.raise_for_status()
                except HTTPError as http_err:
                    # https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
                    print(f'HTTP error occurred: {http_err}')  # Python 3.6
                except Exception as err:
                    print(f'Other error occurred: {err}')  # Python 3.6
                else:
                    # Success!
                    print('download file ', uri, ' on ', fileout)
                    with open(fileout, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:  # filter out keep-alive new chunks
                                f.write(chunk)

        return d


if __name__ == '__main__':
    import doctest

    uri = 'https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z'

    doctest.testmod(extraglobs={'t': DataObj(uri=uri)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
