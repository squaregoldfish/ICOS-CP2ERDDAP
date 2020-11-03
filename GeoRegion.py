#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    The GeoRegion is used to explore ICOS CP georegions' metadata.

    Example usage:

    From GeoRegion import GeoRegion

    georegions = GeoRegion()    # initialise ICOS CP GeoRegion object
    georegions.get_meta()       # get georegions' metadata from ICOS CP
    georegions.show()           # print georegions' metadata
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
# import from my project
from ICPObj import ICPObj


class GeoRegion(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show()
    <BLANKLINE>
    type: <class '__main__.GeoRegion'>
    <BLANKLINE>
    Class name: GeoRegion
    ...
    <BLANKLINE>
    \tlabel               : type: literal    value: ...
    \turi                 : type: uri        value: ...
    <BLANKLINE>
    ...
    """

    def __init__(self, limit=None, uri=None):
        """
        This functions initialise instance of GeoRegion(ICPObj).
        Set up a sparql query to get all metadata of GeoRegion from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select GeoRegion:
        - with ICOS CP 'uri'

        Example:
            GeoRegion(limit=5)

        :param limit: number of returned results
        :param uri: ICOS CP URI ('https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z')
        """
        super().__init__()
        # overwrite class name
        self._name = 'GeoRegion'
        # overwrite conventional attributes renaming dictionary
        self._convAttr = {}
        # overwrite query string
        self._queryString = """
            select ?xxx ?label ?comment ?seeAlso
            where {
                %s # _filterObj(uri=uri)
                ?xxx rdf:type/rdfs:subClassOf*  <http://meta.icos-cp.eu/ontologies/otcmeta/GeoRegion> .

                OPTIONAL { ?xxx rdfs:label ?label .}
                OPTIONAL { ?xxx rdfs:comment ?comment .}
                OPTIONAL { ?xxx rdfs:seeAlso ?seeAlso .}
            }
            %s  # _checklimit(limit)
        """ % (self._filterObj(uri_=uri),
               self._checkLimit(limit_=limit))
        #


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': GeoRegion(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
