#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# icpObj.py

"""
    This module set up a generic class for ICOS CP Object.

    Example usage:

    from icpObj import ICPObj

    icpobj = ICPObj()   # initialise ICPObj
    icpobj.get_meta()   # get metadata from ICOS CP
    icpobj.show()       # print metadata
"""

# --- import -----------------------------------
# import from standard lib
from pathlib import Path
from urllib.parse import urlparse
import logging
import traceback
from pprint import pformat
# import from other lib
# > conda-forge
from SPARQLWrapper import SPARQLWrapper2
from dateutil.parser import parse
# import from my project
import icp2edd.util as util

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

# object attributes' dictionary with RDF 'property' as key and RDF 'object' as value
#   RDF triples: 'subject' + 'property/predicate' + 'object/value'
# {'property/predicate': 'object/value'}
# Note: 'object/value' will be the output attribute name
_attr = {
    'rdfs:comment': 'comment',
    'rdfs:label': 'label',
    'rdfs:seeAlso': 'see_also'
}
# list of equivalent class
_equivalentClass = []
# namespace
_ns = {
    'cpmeta': 'http://meta.icos-cp.eu/ontologies/cpmeta/',
    'geosparql': 'http://www.opengis.net/ont/geosparql#',
    'otcmeta': 'http://meta.icos-cp.eu/ontologies/otcmeta/',
    'owl': 'http://www.w3.org/2002/07/owl#',
    'prov': 'http://www.w3.org/ns/prov#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'xsd': 'http://www.w3.org/2001/XMLSchema#'
}


# TODO check and replace if x vs if x is None...
# ----------------------------------------------
class ICPObj(object):
    """
    >>> t._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/DataObject'
    >>> t.getMeta()
    >>> t.show(True)
    <BLANKLINE>
    type: <class '__main__.ICPObj'>
    <BLANKLINE>
    Class name: uri
    ...
    <BLANKLINE>
    \turi                 : type: uri        value: ...
    <BLANKLINE>
    ...

    \tlabel               : type: literal    value: ...
    \tcomment             : type: literal    value: ...
    \tseeAlso             : type: literal    value: ...
    \turi                 : type: uri        value: ...
    <BLANKLINE>
    ...
    >>> t._uri = 'https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z'
    >>> t._getObjectType()
    'DataObject'
    """
    def __init__(self, limit=None, submfrom=None, submuntil=None, product=None, lastversion=None, uri=None):
        """ initialise generic ICOS CP object (ICPObj).

        It will be used to set up a sparql query, and get all metadata of ICPObj from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select DataObject:
        - submitted from 'submfrom'
        - submitted until 'submuntil'
        - of data type 'product'
        - only from the 'lastversion'
        - with ICOS CP 'uri'

        Example:
            ICPObj(submfrom = '2020-01-01T00:00:00.000Z',
                   submuntil = '2020-01-05T00:00:00.000Z',
                   product = 'icosOtcL1Product_v2',
                   lastversion = False )

        :param limit: number of returned results
        :param submfrom: submitted from date ( '2020-01-01T00:00:00.000Z' )
        :param submuntil: submitted until date ( '2020-01-01T00:00:00.000Z' )
        :param product: select this product type ('icosOtcL1Product_v2')
        :param lastversion: select only last release [True,False]
        :param uri: ICOS CP URI ('https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z')
        """
        # set up class/instance variables
        # self._name = 'uri'
        self._uri = uri
        self._limit = limit
        self._from = submfrom
        self._until = submuntil
        self._product = product
        self._lastversion = lastversion

        # object attributes' dictionary
        # TODO change to attr to avoid access to protected member of class
        if not hasattr(self, '_attr'):
            # set up if not defined
            self._attr = {}

        if isinstance(_attr, dict):
            # merge _attr and self.attr properties.
            # Note:  _.attr's values are overwritten by the self.attr's
            self._attr = {**_attr, **self._attr}

        # object attributes' dictionary
        if not hasattr(self, '_equivalentClass'):
            # set up if not defined
            self._equivalentClass = []

        self._ns = {**_ns}

        # list of prefix used in SPARQL query
        self._prefix = ''.join(f"prefix {k}: <{v}>\n" for k, v in self._ns.items())

        # dictionary to store metadata
        self.meta = {}

        # object type URI
        # self._object = 'http://meta.icos-cp.eu/ontologies/cpmeta/DataObject'
        self._object = None
        if self._uri is not None:
            self._object = self._getObject()

        self.objtype = None
        if self._object is not None:
            self.objtype = self._getObjectType()

        # get instance name
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self._instance_name = text[:text.find('=')].strip()

    def _queryString(self):
        """create SPARQL query string

        optionally add some filter to the SPARQL query depending on properties available in the object:
        - filter on URI, in any case
        - filter on Product, only if object type is 'DataObject' or 'SimpleDataObject'
        - filter on submission time, if property 'wasSubmittedBy' is available
        - filter on last version, if property 'isNextVersionOf' is available
        - filter on number of output, in any case
        """
        # TODO check every attribute value are unique
        # add equivalent class attribute
        if self._equivalentClass:
            # merge _equivalentClass._attr and self.attr properties.
            # Note:  _equivalentClass.attr's values are overwritten by the self.attr's
            for k in self._equivalentClass:
                exec('from icp2edd.cpmeta import *')
                klass = eval(k)
                inst = klass()
                self._attr = {**inst._attr, **self._attr}

        select = f"select ?uri"
        option = ''
        for k, v in self._attr.items():
            select = select + ' ?' + v
            option = option + "\n\tOPTIONAL { ?uri %s ?%s .}" % (k, v)

        # start where block
        query = select + '\nwhere {'
        # filter: uri
        query = query + f'\n\t{self._filterObj(self._uri)} # _filterObj(uri)'

        # object type name
        objtype = None
        if self._object is not None:
            objtype = Path(self._object).name

        if objtype in ('DataObject', 'SimpleDataObject'):
            # filter: product
            query = query + \
                     f'\n\t{self._filterProduct(self._product)} # _filterProduct(product)'
            # add main object
            query = query + '\n\t ?uri cpmeta:hasObjectSpec ?spec .'
        else:
            # add main object
            query = query + '\n\t ?uri rdf:type/rdfs:subClassOf* <%s> .' % self._object

        # filter: submission time
        if 'cpmeta:wasSubmittedBy' in self._attr.keys():
            query = query + '\n\t?uri cpmeta:wasSubmittedBy [' \
                            '\n\t\tprov:endedAtTime ?submTime ;' \
                            '\n\t\tprov:wasAssociatedWith ?submitter' \
                            '\n\t\t] .'\
                            f"\n\t{self._filterSubmTime(self._from, op_='>=')} " \
                            f"# _filterSubmTime(from, op_='>=')"\
                            f"\n\t{self._filterSubmTime(self._until, op_='<=')} " \
                            f"# _filterSubmTime(until, op_='<=')"

        # filter last version
        if 'cpmeta:isNextVersionOf' in self._attr.keys():
            query = query + f'\n\t{self._filterLastVersion(self._lastversion)} # _filterLastVersion(lastversion)'

        # add optional request (all attributes)
        query = query + '\n' + option
        # close where block
        query = query + '\n}'
        # filter: limit
        query = query + f'\n{self._filterLimit(self._limit)}  # _filterLimit(limit)'

        return query

    def _query(self, queryString_):
        """
        This functions run a sparql query on ICOS CP.
        Here we select metadata from every stations store in the ICOS CP.

        :return: SPARQLWrapper Bindings object (each binding is a dictionary)
        """
        if not isinstance(queryString_, str):
            raise TypeError(f'Invalid type value. queryString: \n"""{queryString_}"""\nmust be string, '
                            f'here {type(queryString_)}')

        _logger.debug(f"queryString_:\n {queryString_}")
        sparql = SPARQLWrapper2("https://meta.icos-cp.eu/sparql")

        query = self._prefix + queryString_
        sparql.setQuery(query)
        try:
            return sparql.query()
        except Exception:  # as err:
            _logger.exception("ERROR with SPARQL query")
            raise  #

    def _getObject(self):

        if self._is_url(self._uri):
            queryString = """
            select ?objtype
            where{
             <%s> rdf:type ?objtype
            }
            """ % self._uri
        else:
            raise TypeError(f'Invalid object format: {self._uri}')

        res = self._query(queryString)
        # keep only icos-cp object
        res.bindings = list(v for v in res.bindings if 'meta.icos-cp.eu' in v['objtype'].value)
        # check only one result
        if len(res.bindings) > 1:
            _logger.error(f'Invalid number of result -{len(res.bindings)}-'
                          f' for uri:{self._uri}')

        for result in res.bindings:
            uri = result['objtype'].value
            # check is uri
            if self._is_url(uri):
                return uri
            else:
                raise TypeError(f'Invalid object format: {uri}')

    def _getObjectType(self):

        uri = self._object
        # check is uri
        if self._is_url(uri):
            otype = Path(uri).name
            # if otype in globals().keys():
            #     print(f'object: {self._object}\n objtype: {otype}')
            return otype
            # else:
            #     raise ValueError(f'Unknown object: {otype}')
        else:
            raise TypeError(f'Invalid object format: {uri}')

    def getMeta(self):
        """
        fill instance's dictionary _meta (keys are: 'type','value')
        with metadata, and their attributes from ICOS CP

        meta = {uri: binding, ...}
            binding = {variable: [SPARQLWrapper.Value,...], ...}
        """
        queryString = self._queryString()
        #
        res = self._query(queryString)
        self.meta = self._groupby(res)
        #
        _logger.debug(f"self.meta: {pformat(self.meta)}")

        # create/overwrite list of uri
        self._uri = self.meta.keys()

    def _groupby(self, res):
        """
        combine bindings of a SPARQL query output in a dictionary

        bindings = [
          {var1: Value11, var2: Value21, var3: Value31 },
          {var1: Value11, var2: Value21, var3: Value32 },
          {var1: Value11, var2: Value21, var3: Value33 },
          {var1: Value11, var2: Value22, var3: Value31 },
          {var1: Value11, var2: Value22, var3: Value32 },
          {var1: Value11, var2: Value22, var3: Value33 }
        ]

        out = { uri: { var1: [Value11],
                       var2: [Value21, Value22],
                       var3: [Value31, Value32, Value33]
                      }
        }

         Furthermore, if the type of the SPARQL Value is 'uri' but not point to a 'meta.icos-cp.eu' element,
         the type value is change to 'literal' to avoid later issue digging into those URI

        :param res: SPARQL query output
        :return: {uri: {variable: [SPARQLWrapper.Value, ...], ...}, ...}
        """
        # exemple SPARQL output variables: 'uri', 'static_object_citation',...
        dict1 = {}
        for binding in res.bindings:
            uri = binding['uri'].value
            if uri not in dict1:
                dict1[uri] = {}
            #
            dict2 = dict1[uri]

            for k, v in binding.items():
                if k not in dict2.keys():
                    dict2[k] = []
                # change type -to avoid later issue digging into those URI-
                if v.type == 'uri' and 'meta.icos-cp.eu' not in v.value:
                    v.type = 'literal'
                # Using a in b is simply translates to b.__contains__(a)
                if v not in dict2[k]:
                    dict2[k] += [v]
                else:
                    pass
                    # already registered
        return dict1

    def show(self, print_=False):
        """
        print metadata read (name, type and value)

        ICPObj.meta = { ?uri = ?result }
         ?result = { ?attr : {type: ? , value: ? }, ... }
        """
        if not isinstance(print_, bool):
            _logger.error(f"Invalid type argument -{print_}-")
            raise TypeError("Invalid type argument")

        _logger.info("Class name: {}".format(self._objtype))
        _logger.info("Instance name: {}".format(self._instance_name))
        _logger.info("\ttype: {}".format(type(self)))
        _logger.info('\t' + pformat(self.meta))

        if print_:
            print("\nClass name: {}".format(self._objtype))
            print("\nInstance name: {}".format(self._instance_name))
            print("\ttype: {}".format(type(self)))
            print('\t' + pformat(self.meta))
            # for binding in self.bindings:
            #     for k, v in binding.items():
            #         print('\tkey:',k,'\n\t\tValue:',v)

    def _filterLimit(self, limit_=0):
        """
        create a string to inject into sparql queries to limit the
        amount of returned results

        :return: string

        >>> t._filterLimit()
        ''
        >>> t._filterLimit(None)
        ''
        >>> t._filterLimit(3)
        'limit 3'
        >>> t._filterLimit('a')
        Traceback (most recent call last):
        ...
            raise ValueError('limit -{}- is not an integer'.format(limit_))
        ValueError: limit -a- is not an integer
        """
        if limit_:
            try:
                limit_ = int(limit_)
                if limit_ > 0:
                    return 'limit ' + str(limit_)
                else:
                    return ''
            except TypeError:
                raise TypeError('limit -{}- has wrong type'.format(limit_))
            except ValueError:
                raise ValueError('limit -{}- is not an integer'.format(limit_))
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
        TypeError: Invalid date format: 0.019360269360269362
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
            raise ValueError("Invalid operator: {} ; valid operator are {}".format(op_, valid_operator))
        ValueError: Invalid operator: = ; valid operator are ['<=', '>=', '<', '>']
        """
        # check operator
        valid_operator = ['<=', '>=', '<', '>']
        if op_ not in valid_operator:
            raise ValueError("Invalid operator: {} ; valid operator are {}".format(op_, valid_operator))

        if datestr_:
            try:
                date_time_string = parse(datestr_, fuzzy=False).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                return "FILTER( ?submTime %s '%s'^^xsd:dateTime )" % (op_, date_time_string)
            except TypeError:
                raise TypeError('Invalid date format: {}'.format(datestr_))
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
            raise TypeError('Invalid product format: {}'.format(product_))
        TypeError: Invalid product format: 22
        >>> t._filterProduct(['pdt','pdt2'])
        'VALUES ?spec {<http://meta.icos-cp.eu/resources/cpmeta/pdt> <http://meta.icos-cp.eu/resources/cpmeta/pdt2>}'
        >>> t._filterProduct(['product',2])
        Traceback (most recent call last):
        ...
            raise TypeError('Invalid product format: {}'.format(product_))
        TypeError: Invalid product format: ['product', 2]
        >>> t._filterProduct(['product'])
        'VALUES ?spec {<http://meta.icos-cp.eu/resources/cpmeta/product>}'
        """
        if product_:
            if isinstance(product_, str):
                return "VALUES ?spec {<http://meta.icos-cp.eu/resources/cpmeta/%s>}" % product_
            elif isinstance(product_, list) and all(isinstance(n, str)for n in product_):
                # _ = "> <http://meta.icos-cp.eu/resources/cpmeta/".join(product_)
                # return "VALUES ?spec {<http://meta.icos-cp.eu/resources/cpmeta/%s>}" % _
                return "VALUES ?spec {%s}" % " ".join('<http://meta.icos-cp.eu/resources/cpmeta/{}>'.format(w)
                                                      for w in product_)
            else:
                raise TypeError('Invalid product format: {}'.format(product_))
        else:
            return ''

    def _filterLastVersion(self, lastversion_=None):
        """
        create a string to inject into sparql queries to select object
        from the last release only

        Note: None act as False value

        :param lastversion_: boolean [True,False]

        :return: string

        >>> t._filterLastVersion()
        ''
        >>> t._filterLastVersion(False)
        ''
        >>> t._filterLastVersion(True)
        'FILTER NOT EXISTS {[] cpmeta:isNextVersionOf ?uri}'
        >>> t._filterLastVersion('toto')
        Traceback (most recent call last):
            ...
            raise TypeError('Invalid lastVersion type: {}'.format(lastversion_))
        TypeError: Invalid lastVersion type: toto
        """

        if lastversion_:
            if isinstance(lastversion_, bool):
                return "FILTER NOT EXISTS {[] cpmeta:isNextVersionOf ?uri}"
            else:
                raise TypeError('Invalid lastVersion type: {}'.format(lastversion_))
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
            raise TypeError('Invalid object format: {}'.format(uri_))
        TypeError: Invalid object format: toto
        >>> t._filterObj(33)
        Traceback (most recent call last):
        ...
            raise TypeError('Invalid object format: {}'.format(uri_))
        TypeError: Invalid object format: 33
        >>> t._filterObj('https://www.jetbrains.com/help/pycharm')
        'VALUES ?uri {<https://www.jetbrains.com/help/pycharm>}'
        >>> t._filterObj(['toto',33])
        Traceback (most recent call last):
        ...
            raise TypeError('Invalid object format: {}'.format(uri_))
        TypeError: Invalid object format: ['toto', 33]
        >>> t._filterObj(['https://www.jetbrains.com/help/pycharm','https://docs.python.org/3/tutorial/errors.html'])
        'VALUES ?uri {<https://www.jetbrains.com/help/pycharm> <https://docs.python.org/3/tutorial/errors.html>}'
        """
        if uri_:
            if self._is_url(uri_):
                return "VALUES ?uri {<%s>}" % uri_
            elif isinstance(uri_, list) and all(self._is_url(n) for n in uri_):
                return "VALUES ?uri {%s}" % " ".join('<{}>'.format(w) for w in uri_)
            else:
                raise TypeError('Invalid object format: {}'.format(uri_))
        else:
            return ''

    def listUri(self, filename_):
        """ given filename, return uri on ICOS CP

        """
        if filename_:
            if isinstance(filename_, str):
                filenames = '"{}"'.format(filename_)
            elif isinstance(filename_, list) and all(isinstance(n, str)for n in filename_):
                filenames = ' '.join('"{}"'.format(w) for w in filename_)
            else:
                raise TypeError('Invalid product format: {}'.format(filename_))

            if self._is_url(self._object):
                queryString = """
                select ?uri
                where{
                 VALUES ?name {%s}
                 ?uri rdf:type <%s> ;
                     cpmeta:hasName ?name .
                 FILTER NOT EXISTS {[] cpmeta:isNextVersionOf ?uri}
                }
                """ % (filenames, self._object)
            else:
                raise TypeError(f'Invalid object format: {self._object}')

            res = self._query(queryString)
            return [r['uri'].value for r in res.bindings]

        else:
            return ''


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': ICPObj(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
