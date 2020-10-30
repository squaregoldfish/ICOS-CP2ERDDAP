#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    The DataObj module is used to explore ICOS dataObjs metadata.

    Example usage:

    import DataObj

    dataObjs = DataObj.get_meta() # return a list of dataObjs' dictionary
    myDataObj = dataObjs[uri]     # uri is the ICOS CP URI
"""

__author__ = ["Julien Paul"]
__credits__ = ""
__license__ = "CC BY-SA 4.0"
__version__ = "0.0.0"
__maintainer__ = "BCDC"
__email__ = ['julien.paul@uib.no']
__status__ = ""

# ----------------------------------------------
# import from standard lib
# import from other lib
import requests
from requests.exceptions import HTTPError
# > conda-forge
from SPARQLWrapper import SPARQLWrapper2
# import from my project

# ----------------------------------------------
abc = {
    'citationString': 'citation',
    'sha256sum': 'toto'
}


def query(lastupdate='', endupdate='', product='', lastVersion=False, uri=''):
    """
    This functions create and run a sparql query on ICOS CP.
    Here we select metadata from every dataObjects store in the ICOS CP.

    Optionally we could select dataObject:
    - submitted since 'lastupdate'
    - submitted until 'endupdate'
    - of data type 'product'
    - only from the 'lastVersion'
    - with ICOS CP 'uri'

    Example:
        query(lastupdate = '2020-01-01T00:00:00.000Z',
              endupdate = '2020-01-05T00:00:00.000Z',
              product = 'icosOtcL1Product_v2',
              lastVersion = False )

    :param lastupdate: submitted since last update ( '2020-01-01T00:00:00.000Z' )
    :param endupdate: submitted until end update ( '2020-01-01T00:00:00.000Z' )
    :param product: select this product type ('icosOtcL1Product_v2')
    :param lastVersion: select only last release [True,False]
    :param uri: ICOS CP URI ('https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z')
    :return: SPARQLWrapper Bindings object (each binding is a dictionary)
    """

    filterLastUpDate = ''
    if lastupdate:
        filterLastUpDate = "FILTER( ?submTime >= '%s'^^xsd:dateTime )" % lastupdate

    filterEndUpDate = ''
    if endupdate:
        filterEndUpDate = "FILTER( ?submTime <= '%s'^^xsd:dateTime )" % endupdate

    filterProdcut = ''
    if product:
        filterProdcut = "VALUES ?spec {<http://meta.icos-cp.eu/resources/cpmeta/%s>}" % product

    filterLastVersion = ''
    if lastVersion:
        filterLastVersion = "FILTER NOT EXISTS {[] cpmeta:isNextVersionOf ?dataObj}"

    filterDobj = ''
    if uri:
        filterDobj = "VALUES ?dataObj {<%s>}" % uri

    queryString = """
        prefix cpmeta: <http://meta.icos-cp.eu/ontologies/cpmeta/>
        prefix otcmeta: <http://meta.icos-cp.eu/ontologies/otcmeta/>
        prefix prov: <http://www.w3.org/ns/prov#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>

        select ?dataObj ?sizeInBytes ?sha256sum ?citationString ?name ?doi ?nextVersionOf ?dataSubmission 
               ?dataObjectSpec ?datAcquisition ?dataProduction ?formatSpecificMetadata ?keyword ?variableName 
               ?actualVariable ?temporalResolution ?spatialCoverage ?label ?comment ?seeAlso
        where {
            %s #VALUES ?dataObj {<http://meta.icos-cp.eu/object>}
            %s #VALUES ?spec {<http://meta.icos-cp.eu/resources/cpmeta/icosOtcL1Product_v2>}
            ?dataObj cpmeta:hasObjectSpec ?spec . # restriction property for DataObject and/or SimpleDataObject
            ?dataObj cpmeta:wasSubmittedBy [
                prov:endedAtTime ?submTime ;
                prov:wasAssociatedWith ?submitter
                ] .
            %s #FILTER( ?submTime <= '2020-02-01T00:00:00.000Z'^^xsd:dateTime )
            %s #FILTER( ?submTime >= '2020-01-01T00:00:00.000Z'^^xsd:dateTime )
            %s #FILTER NOT EXISTS {[] cpmeta:isNextVersionOf ?dataObj}
             
            OPTIONAL { ?dataObj cpmeta:hasSizeInBytes ?sizeInBytes .}          # as subClassOf DataObject
            OPTIONAL { ?dataObj cpmeta:hasSha256sum ?sha256sum .}               # as subClassOf DataObject
            OPTIONAL { ?dataObj cpmeta:hasCitationString ?citationString .}     # as subClassOf DataObject
            OPTIONAL { ?dataObj cpmeta:hasName ?name .}
            OPTIONAL { ?dataObj cpmeta:hasDoi ?doi .}
            OPTIONAL { ?dataObj cpmeta:isNextVersionOf ?nextVersionOf .}

            OPTIONAL { ?dataObj cpmeta:wasSubmittedBy ?dataSubmission .}           # as subClassOf DataObject
            OPTIONAL { ?dataObj cpmeta:hasObjectSpec ?dataObjectSpec .}       # domain

            OPTIONAL { ?dataObj cpmeta:wasAcquiredBy ?datAcquisition .}       # domain
            OPTIONAL { ?dataObj cpmeta:wasProducedBy ?dataProduction .}       # domain

            OPTIONAL { ?dataObj cpmeta:hasFormatSpecificMetadata ?formatSpecificMetadata .}
            OPTIONAL { ?dataObj cpmeta:hasKeyword ?keyword . }
            OPTIONAL { ?dataObj cpmeta:hasVariableName ?variableName .}
            OPTIONAL { ?dataObj cpmeta:hasActualVariable ?actualVariable .}
            OPTIONAL { ?dataObj cpmeta:hasTemporalResolution ?temporalResolution .}
            OPTIONAL { ?dataObj cpmeta:hasSpatialCoverage ?spatialCoverage .}

            OPTIONAL { ?dataObj rdfs:label ?label .}
            OPTIONAL { ?dataObj rdfs:comment ?comment .}
            OPTIONAL { ?dataObj rdfs:seeAlso ?seeAlso .}
        }
        limit 10
    """ % (filterDobj, filterProdcut, filterLastUpDate, filterEndUpDate, filterLastVersion)

    sparql = SPARQLWrapper2("https://meta.icos-cp.eu/sparql")

    sparql.setQuery(queryString)
    try:
        return sparql.query()
    except Exception as err:
        print("\nAn exception was caught!\n")
        print(str(err))
        raise err


def download(uri, o):
    """

    curl -JO -H "Cookie: CpLicenseAcceptedFor=PID" URL

    :param uri: ICOS CP dataObj URI
    :param o: output file
    """

    # uri = 'https://data.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z'
    pid = uri.split("/")[-1]
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
            # r = requests.get(url, auth=HTTPDigestAuth(user, pswd), stream=True)
            print(uri, type(uri))
            print(cookies)
            r = s.get(str(url), cookies=cookies, stream=True)
            # If the response was successful, no Exception will be raised
            r.raise_for_status()
        except HTTPError as http_err:
            # https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')
            # etc...
            print('download file ', uri, ' on ', o)
            with open(o, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)


def renameKeyDic(mydict):
    """
    renaming dictionary keys:
    :return:
    """
    for oldKey, newKey in abc.items():
        mydict = dict((newKey, v) if k == oldKey else (k, v) for k, v in mydict.items())
    return mydict


def get_meta(lastupdate='', endupdate='', product='', lastVersion=False, uri=''):
    """
    get all selected dataOjs, and their attributes from ICOS CP

    :return: dataObjs' dictionary
    """
    # init empty dict
    dataObjs = {}

    res = query(lastupdate, endupdate, product, lastVersion, uri)

    for result in res.bindings:
        result['uri'] = result.pop("dataObj")
        uri = result['uri'].value
        dataObjs[uri] = result

        print(result)
        print('\nrename attribute\n---------\n')
        dataObjs[uri] = renameKeyDic(result)

    return dataObjs


if __name__ == '__main__':

    uri = 'https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z'

    print('\nquery on last submission\n')
    dataObjs = get_meta(lastupdate='2020-01-01T00:00:00.000Z', endupdate='2020-08-05T00:00:00.000Z',
                        product='icosOtcL1Product_v2', lastVersion=True)
    for k, v in dataObjs.items():
        for kk, vv in v.items():
            print(kk, ' : ', 'type:', vv.type, 'value:', vv.value)

    print('\nquery on one dataObj\n')
    dataObjs = get_meta(uri=uri)
    for k, v in dataObjs.items():
        for kk, vv in v.items():
            print(kk, ' : ', 'type:', vv.type, 'value:', vv.value)

    print('\n\n')
    # url = 'https://data.icos-cp.eu/objects/8Pj-v7cmVZUm-8j0zFG96USA'   # 26NA_NRT_20190327.csv
    url = 'https://data.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z'
    out = 'toto.csv'
    # download(url,out)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
