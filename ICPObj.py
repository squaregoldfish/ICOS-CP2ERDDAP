#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module set up a generic class for ICOS CP Object.

    Example usage:

    from ICPObj import ICPObj

    icpobj = ICPObj()   # initialise ICPObj
    icpobj.get_meta()   # get metadata from ICOS CP
    icpobj.show()       # print metadata
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
from urllib.parse import urlparse
# import from other lib
# > conda-forge
from SPARQLWrapper import SPARQLWrapper2
from dateutil.parser import parse
# import from my project


# ----------------------------------------------
class ICPObj(object):
    """
    >>> t.getMeta()
    >>> t.show()
    <BLANKLINE>
    type: <class '__main__.ICPObj'>
    <BLANKLINE>
    Class name: xxx
    <BLANKLINE>
    \tsizeInBytes         : type: literal    value:...
    \tsha256sum           : type: literal    value:...
    \tname                : type: literal    value:...
    \tDataSubmission      : type: uri        value:...
    \tDatAcquisition      : type: uri        value:...
    \tDataProduction      : type: uri        value:...
    \turi                 : type: uri        value:...
    <BLANKLINE>
    ...
    """
    def __init__(self, limit=None, lastupdate=None, endupdate=None, product=None, lastversion=None, uri=None):
        """
        This functions initialise generic ICOS CP object (ICPObj).
        Set up a sparql query to get all metdata of ICPObj from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select DataObj:
        - submitted since 'lastupdate'
        - submitted until 'endupdate'
        - of data type 'product'
        - only from the 'lastversion'
        - with ICOS CP 'uri'

        Example:
            ICPObj(lastupdate = '2020-01-01T00:00:00.000Z',
                   endupdate = '2020-01-05T00:00:00.000Z',
                   product = 'icosOtcL1Product_v2',
                   lastversion = False )

        :param limit: number of returned results
        :param lastupdate: submitted since last update ( '2020-01-01T00:00:00.000Z' )
        :param endupdate: submitted until end update ( '2020-01-01T00:00:00.000Z' )
        :param product: select this product type ('icosOtcL1Product_v2')
        :param lastversion: select only last release [True,False]
        :param uri: ICOS CP URI ('https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z')
        """
        # default name for test only
        self._name = 'xxx'
        # default conventional attributes renaming dictionary
        self._convAttr = {'citationString': 'citation', 'tata': 'toto'}
        # list of prefix used in SPARQL query
        self._prefix = """
            prefix cpmeta: <http://meta.icos-cp.eu/ontologies/cpmeta/>
            prefix otcmeta: <http://meta.icos-cp.eu/ontologies/otcmeta/>
            prefix prov: <http://www.w3.org/ns/prov#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix xsd: <http://www.w3.org/2001/XMLSchema#>
            """
        # default query for test only
        self._queryString = """
            select  ?xxx ?sizeInBytes ?sha256sum ?citationString ?name ?doi ?nextVersionOf
                    ?DataSubmission ?DatAcquisition ?DataProduction ?formatSpecificMetadata ?keyword ?variableName
                    ?actualVariable ?temporalResolution ?spatialCoverage ?label ?comment ?seeAlso
            where {
                %s # _filterObj(uri=uri)
                %s # _filterProduct(product=product)
                ?xxx cpmeta:hasObjectSpec ?spec . # restriction property for DataObject and/or SimpleDataObject
                ?xxx cpmeta:wasSubmittedBy [
                    prov:endedAtTime ?submTime ;
                    prov:wasAssociatedWith ?submitter
                    ] .
                %s # _filterSubmTime(datestr=lastupdate, op='>=')
                %s # _filterSubmTime(datestr=endupdate, op='<=')
                %s # _filterLastVersion(lastversion=lastversion)

                OPTIONAL { ?xxx cpmeta:hasSizeInBytes ?sizeInBytes .}          # as subClassOf DataObject
                OPTIONAL { ?xxx cpmeta:hasSha256sum ?sha256sum .}               # as subClassOf DataObject
                OPTIONAL { ?xxx cpmeta:hasCitationString ?citationString .}     # as subClassOf DataObject
                OPTIONAL { ?xxx cpmeta:hasName ?name .}
                OPTIONAL { ?xxx cpmeta:hasDoi ?doi .}
                OPTIONAL { ?xxx cpmeta:isNextVersionOf ?nextVersionOf .}

                OPTIONAL { ?xxx cpmeta:wasSubmittedBy ?DataSubmission .}           # as subClassOf DataObject
                OPTIONAL { ?xxx cpmeta:hasObjectSpec ?DataObjectSpec .}       # domain

                OPTIONAL { ?xxx cpmeta:wasAcquiredBy ?DatAcquisition .}       # domain
                OPTIONAL { ?xxx cpmeta:wasProducedBy ?DataProduction .}       # domain

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
            %s  # _checklimit(limit)
        """ % (self._filterObj(uri_=uri),
               self._filterProduct(product_=product),
               self._filterSubmTime(datestr_=lastupdate, op_='>='),
               self._filterSubmTime(datestr_=endupdate, op_='<='),
               self._filterLastVersion(lastversion_=lastversion),
               self._checkLimit(limit_=limit))
        #
        self.meta = {}

    def _query(self):
        """
        This functions run a sparql query on ICOS CP.
        Here we select metadata from every stations store in the ICOS CP.

        :return: SPARQLWrapper Bindings object (each binding is a dictionary)
        """
        sparql = SPARQLWrapper2("https://meta.icos-cp.eu/sparql")

        query = self._prefix + self._queryString
        sparql.setQuery(query)
        try:
            return sparql.query()
        except Exception as err:
            print("\nAn exception was caught!\n")
            print(str(err))
            raise err

    def getMeta(self):
        """
        fill instance's dictionary _meta (keys are: 'type','value')
        with metadata, and their attributes from ICOS CP

        meta = { ?uri : ?result, ... }
            ?result = { ?attr : {type: ? , value: ?}, ... }
        """
        # init empty dict
        res = self._query()
        for result in res.bindings:
            # result = { ? :{type: ? , value: ?}, ... }
            result['uri'] = result.pop("xxx")
            uri = result['uri'].value
            self.meta[uri] = self._renameKeyDic(result)

    def show(self):
        """
        print metadata read (name, type and value)

        ICPObj.meta = { ?uri = ?result }
         ?result = { ?attr : {type: ? , value: ? }, ... }
        """
        print("\ntype: {}".format(type(self)))
        print("\nClass name: {}".format(self._name))
        for k, v in self.meta.items():
            print('')
            for kk, vv in v.items():
                print('\t{:20}: type: {:10} value: {}'.format(kk, vv.type, vv.value))

    def _renameKeyDic(self, _):
        """
        rename dictionary keys:
        :return: renamed dictionary
        """
        for oldKey, newKey in self._convAttr.items():
            _ = dict((newKey, v) if k == oldKey else (k, v) for k, v in _.items())
        return _

    def _checkLimit(self, limit_=0):
        """
        create a string to inject into sparql queries to limit the
        amount of returned results

        :return: string

        >>> t._checkLimit()
        ''
        >>> t._checkLimit(None)
        ''
        >>> t._checkLimit(3)
        'limit 3'
        >>> t._checkLimit('a')
        Traceback (most recent call last):
        ...
            raise ValueError('limit is not an integer')
        ValueError: limit is not an integer
        """
        if limit_:
            try:
                limit_ = int(limit_)
                if limit_ > 0:
                    return 'limit ' + str(limit_)
                else:
                    return ''
            except TypeError:
                raise TypeError('limit has wrong type')
            except ValueError:
                raise ValueError('limit is not an integer')
        else:
            return ''

    def _filterSubmTime(self, datestr_='', op_='>='):
        """
        create a string to inject into sparql queries to select object
        submitted since 'datestr_'

        optionaly, you could select object submitted before 'datestr_', using operator '<='

        :param datestr_: string of date
        :param op_: string of operator to use ['<=', '>=', '<', '>']

        :return: string

        >>> t._filterSubmTime()
        ''
        >>> t._filterSubmTime(23/12/99, op_='<')
        Traceback (most recent call last):
            ...
        TypeError: ('Invalid date format ', 0.019360269360269362)
        >>> t._filterSubmTime('toto', op_='<')
        Traceback (most recent call last):
            ...
            raise ParserError("Unknown string format: %s", timestr)
        dateutil.parser._parser.ParserError: Unknown string format: toto
        >>> t._filterSubmTime('23/12/99', op_='<')
        "FILTER( ?submTime < '1999-12-23T00:00:00.000000Z'^^xsd:dateTime )"
        >>> t._filterSubmTime('23/12/99', op_='=')
        Traceback (most recent call last):
            ...
            raise ValueError("Invalid operator: {}; valid operator are {}".format(op, valid_operator))
        ValueError: Invalid operator: =; valid operator are ['<=', '>=', '<', '>']
        """
        # check operator
        valid_operator = ['<=', '>=', '<', '>']
        if op_ not in valid_operator:
            raise ValueError("Invalid operator: {}; valid operator are {}".format(op_, valid_operator))

        if datestr_:
            try:
                date_time_string = parse(datestr_, fuzzy=False).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                return "FILTER( ?submTime %s '%s'^^xsd:dateTime )" % (op_, date_time_string)
            except TypeError:
                raise TypeError('Invalid date format ', datestr_)
        else:
            return ''

    def _filterProduct(self, product_=''):
        """
        create a string to inject into sparql queries to select object
        of 'product_' type

        example:
            product_ = 'icosOtcL1Product_v2'

        :param product_: string of product type

        :return: string

        >>> t._filterProduct()
        ''
        >>> t._filterProduct('product')
        'VALUES ?spec {<http://meta.icos-cp.eu/resources/cpmeta/product>}'
        >>> t._filterProduct(22)
        Traceback (most recent call last):
            ...
            raise TypeError('Invalid product format', product)
        TypeError: ('Invalid product format', 22)
        >>> t._filterProduct(['product','product2'])
        'VALUES ?spec {<http://meta.icos-cp.eu/resources/cpmeta/product http://meta.icos-cp.eu/resources/cpmeta/%sproduct2>}'
        >>> t._filterProduct(['product',2])
        Traceback (most recent call last):
        ...
            raise TypeError('Invalid product format', product_)
        TypeError: ('Invalid product format', ['product', 2])
        >>> t._filterProduct(['product'])
        'VALUES ?spec {<http://meta.icos-cp.eu/resources/cpmeta/product>}'
        """
        if product_:
            if isinstance(product_, str):
                return "VALUES ?spec {<http://meta.icos-cp.eu/resources/cpmeta/%s>}" % product_
            elif isinstance(product_, list) and all(isinstance(n, str)for n in product_):
                _ = " http://meta.icos-cp.eu/resources/cpmeta/%s".join(product_)
                return "VALUES ?spec {<http://meta.icos-cp.eu/resources/cpmeta/%s>}" % _
            else:
                raise TypeError('Invalid product format', product_)
        else:
            return ''

    def _filterLastVersion(self, lastversion_=True):
        """
        create a string to inject into sparql queries to select object
        from the last release only

        :param lastversion_: boolean [True,False]

        :return: string

        >>> t._filterLastVersion()
        'FILTER NOT EXISTS {[] cpmeta:isNextVersionOf ?xxx}'
        >>> t._filterLastVersion(False)
        ''
        >>> t._filterLastVersion(True)
        'FILTER NOT EXISTS {[] cpmeta:isNextVersionOf ?xxx}'
        >>> t._filterLastVersion('toto')
        Traceback (most recent call last):
            ...
            raise TypeError('Invalid ', lastversion)
        TypeError: ('Invalid ', 'toto')
        """
        if lastversion_:
            if isinstance(lastversion_, bool):
                return "FILTER NOT EXISTS {[] cpmeta:isNextVersionOf ?xxx}"
            else:
                raise TypeError('Invalid ', lastversion_)
        else:
            return ''

    def _is_url(self, url_):
        """
        check if argument is an url

        :param url_: string of url to check

        :return: boolean
        """
        try:
            result = urlparse(url_)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def _filterObj(self, uri_=''):
        """
        create a string to inject into sparql queries to select object
        of ICOS CP URI equal to 'uri_'

        :param uri_: string of ICOS CP uri

        :return: string

        >>> t._filterObj('toto')
        Traceback (most recent call last):
            ...
            raise TypeError('Invalid object format', uri)
        TypeError: ('Invalid object format', 'toto')
        >>> t._filterObj(33)
        Traceback (most recent call last):
        ...
            raise TypeError('Invalid object format', uri_)
        TypeError: ('Invalid object format', 33)
        >>> t._filterObj('https://www.jetbrains.com/help/pycharm')
        'VALUES ?xxx {<https://www.jetbrains.com/help/pycharm>}'
        >>> t._filterObj(['toto',33])
        Traceback (most recent call last):
        ...
            raise TypeError('Invalid object format', uri_)
        TypeError: ('Invalid object format', ['toto', 33])
        >>> t._filterObj(['https://www.jetbrains.com/help/pycharm','https://docs.python.org/3/tutorial/errors.html'])
        'VALUES ?xxx {<https://www.jetbrains.com/help/pycharm https://docs.python.org/3/tutorial/errors.html>}'
        """
        if uri_:
            if self._is_url(uri_):
                return "VALUES ?xxx {<%s>}" % uri_
            elif isinstance(uri_, list) and all(self._is_url(n) for n in uri_):
                return "VALUES ?xxx {<%s>}" % " ".join(uri_)
            else:
                raise TypeError('Invalid object format', uri_)
        else:
            return ''


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': ICPObj(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
