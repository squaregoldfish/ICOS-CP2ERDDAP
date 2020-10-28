#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    The DataSubmission module is used to explore ICOS dataSubmissions metadata.

    Example usage:

    import DataSubmission

    dataSubmissions = DataSubmission.get_meta() # return a list of dataSubmissions' dictionary
    myDataSubmission = dataSubmissions[uri]     # uri is the ICOS CP URI
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
    Here we select metadata from every dataSubmissions store in the ICOS CP.

    :return: SPARQLWrapper Bindings object (each binding is a dictionary)
    """

    queryString = """
        prefix cpmeta: <http://meta.icos-cp.eu/ontologies/cpmeta/>
        prefix otcmeta: <http://meta.icos-cp.eu/ontologies/otcmeta/>
        prefix prov: <http://www.w3.org/ns/prov#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>


        select ?dataSubmission ?project ?startedAtTime ?endedAtTime ?label ?comment ?seeAlso
        where {
           ?dataSubmission rdf:type/rdfs:subClassOf*  <http://meta.icos-cp.eu/ontologies/cpmeta/DataSubmission> .
           OPTIONAL { ?dataSubmission prov:wasAssociatedWith ?project .}
           OPTIONAL { ?dataSubmission prov:startedAtTime     ?startedAtTime .}
           OPTIONAL { ?dataSubmission prov:endedAtTime       ?endedAtTime   .}

           OPTIONAL { ?dataSubmission rdfs:label   ?label .}
           OPTIONAL { ?dataSubmission rdfs:comment ?comment .}
           OPTIONAL { ?dataSubmission rdfs:seeAlso ?seeAlso .}
        }
        #limit 100
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
    get all dataSubmissions, and their attributes from ICOS CP

    :return: dataSubmissions' dictionary
    """
    # init empty dict
    dataSubmissions = {}

    res = query()

    for result in res.bindings:
        uri = result.pop("dataSubmission").value
        dataSubmissions[uri] = result

    return dataSubmissions


if __name__ == '__main__':

    dataSubmissions = get_meta()

    for k, v in dataSubmissions.items():
        print('k:', k)
        for kk, vv in v.items():
            print(kk, ' : ', 'type:', vv.type, 'value:', vv.value)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
