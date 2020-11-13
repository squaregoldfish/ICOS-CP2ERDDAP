#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DataSubmission.py

"""
    The DataSubmission module is used to explore ICOS CP datasubmissions' metadata.

    Example usage:

    From DataSubmission import DataSubmission

    datasubmissions = DataSubmission()  # initialise ICOS CP DataSubmission object
    datasubmissions.get_meta()          # get datasubmissions' metadata from ICOS CP
    datasubmissions.show()              # print datasubmissions' metadata
"""

# --- import -----------------------------------
# import from standard lib
# import from other lib
# import from my project
from icp2edd.ICPObj import ICPObj

# --- module's variable ------------------------
renameAtt = {
    'startedAtTime': 'submission_started_at_time',
    'endedAtTime': 'submission_ended_at_time'
}


# ----------------------------------------------
class DataSubmission(ICPObj):
    """
    >>> t.getMeta()
    >>> t.show()
    <BLANKLINE>
    type: <class '__main__.DataSubmission'>
    <BLANKLINE>
    Class name: DataSubmission
    ...
    <BLANKLINE>
    \tProject             : type: uri        value: ...
    \tsubmission_started_at_time: type: literal    value: ...
    \tsubmission_ended_at_time: type: literal    value: ...
    \turi                 : type: uri        value: ...
    <BLANKLINE>
    ...
    """

    def __init__(self, limit=None, uri=None):
        """
        This functions initialise instance of DataSubmission(ICPObj).
        Set up a sparql query to get all metadata of DataSubmission from ICOS CP.

        Optionally we could limit the number of output:
        - limit the amount of returned results

        and/or select DataSubmission:
        - with ICOS CP 'uri'

        Example:
            DataSubmission(limit=5)

        :param limit: number of returned results
        :param uri: ICOS CP URI ('https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z')
        """
        super().__init__()
        # overwrite class name
        self._name = 'DataSubmission'
        # overwrite conventional attributes renaming dictionary
        if isinstance(renameAtt, dict):
            self._convAttr = renameAtt
        else:
            self._convAttr = {}
        # overwrite query string
        self._queryString = """
            select ?xxx ?Project ?startedAtTime ?endedAtTime ?label ?comment ?seeAlso
            where {
                %s # _filterObj(uri=uri)
               ?xxx rdf:type/rdfs:subClassOf*  <http://meta.icos-cp.eu/ontologies/cpmeta/DataSubmission> .
               OPTIONAL { ?xxx prov:wasAssociatedWith ?Project .}
               OPTIONAL { ?xxx prov:startedAtTime     ?startedAtTime .}
               OPTIONAL { ?xxx prov:endedAtTime       ?endedAtTime   .}

               OPTIONAL { ?xxx rdfs:label   ?label .}
               OPTIONAL { ?xxx rdfs:comment ?comment .}
               OPTIONAL { ?xxx rdfs:seeAlso ?seeAlso .}
            }
            %s  # _checklimit(limit)
        """ % (self._filterObj(uri_=uri),
               self._checkLimit(limit_=limit))
        #


if __name__ == '__main__':
    import doctest

    doctest.testmod(extraglobs={'t': DataSubmission(limit=10)},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
