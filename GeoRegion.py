#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    The GeoRegion module is used to explore ICOS geoRegions metadata.

    Example usage:

    import GeoRegion

    geoRegions = GeoRegion.get_meta() # return a list of geoRegions' dictionary
    myGeoRegion = geoRegions[uri]     # uri is the ICOS CP URI
"""

__author__ = ["Julien Paul"]
__credits__ = ""
__license__ = "CC BY-SA 4.0"
__version__ = "0.0.0"
__maintainer__ = "BCDC"
__email__ = ['julien.paul@uib.no']
__status__ = ""

# ----------------------------------------------
from SPARQLWrapper import SPARQLWrapper2


# ----------------------------------------------
def query():
    """
    This functions create and run a sparql query on ICOS CP.
    Here we select metadata from every geoRegions store in the ICOS CP.

    :return: SPARQLWrapper Bindings object (each binding is a dictionary)
    """

    queryString = """
        prefix cpmeta: <http://meta.icos-cp.eu/ontologies/cpmeta/>
        prefix otcmeta: <http://meta.icos-cp.eu/ontologies/otcmeta/>
        prefix prov: <http://www.w3.org/ns/prov#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>


        select ?geoRegion ?label ?comment ?seeAlso
        where {
           ?geoRegion rdf:type/rdfs:subClassOf*  <http://meta.icos-cp.eu/ontologies/otcmeta/GeoRegion> .

           OPTIONAL { ?geoRegion rdfs:label ?label .}
           OPTIONAL { ?geoRegion rdfs:comment ?comment .}
           OPTIONAL { ?geoRegion rdfs:seeAlso ?seeAlso .}
        }
        limit 10
    """

    sparql = SPARQLWrapper2("https://meta.icos-cp.eu/sparql")

    sparql.setQuery(queryString)
    try:
        return sparql.query()
    except Exception as err:
        print("\nAn exception was caught!\n")
        print(str(err))
        raise err


def get_meta():
    """
    get all geoRegions, and their attributes from ICOS CP

    :return: geoRegions' dictionary
    """
    # init empty dict
    geoRegions = {}

    res = query()

    for result in res.bindings:
        uri = result.pop("geoRegion").value
        geoRegions[uri] = result

    return geoRegions


if __name__ == '__main__':

    geoRegions = get_meta()

    for k, v in geoRegions.items():
        for kk, vv in v.items():
            print(kk, ' : ', 'type:', vv.type, 'value:', vv.value)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
