#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# superIcpObj.py

"""
    This module set up a generic class for super ICOS CP Object.

    Example usage:

    from superIcpObj import SuperICPObj

    supericpobj = SuperICPObj()     # initialise SuperICPObj
    supericpobj.get_meta()          # get metadata from ICOS CP
    supericpobj.show()              # print metadata
"""

# --- import -----------------------------------
# import from standard lib
import logging
from pprint import pformat
# import from other lib
# > conda-forge
# import from my project
from icp2edd.icpObj import ICPObj
# import all class from submodules in cpmeta
from icp2edd.cpmeta import *
import icp2edd.case as case

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)


# ----------------------------------------------
class SuperICPObj(object):
    def __init__(self):
        self.m = {}

        # TODO list uri of all datasets already loaded
        uri = ['https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z']
        try:
            _logger.info('get DataObject metadata from ICOS CP')
            _ = DataObject(uri=uri)
            _.getMeta()
            _.show()
            self.m['DataObject'] = _.meta
            # dataobjs.show()
        except Exception:
            _logger.exception('Something goes wrong when loading metadata from DataObject')
            raise  # Throw exception again so calling code knows it happened

    def getAttr(self):
        """
        superAtts = { ID : atts }
            atts = {name: value, ...}
        """
        superAtts = {}
        for k in self.m['DataObject'].keys():
            fname = self.m['DataObject'][k]['name'].value[:self.m['DataObject'][k]['name'].value.rfind(".")]
            _logger.debug(f'get attribute from DataObject {fname}')
            newDatasetId = case.camel('icos_'+fname, sep='_')
            _logger.debug(f'rename it to {newDatasetId}')
            # newDatasetId = 'icos58gs20190711SocatEnhanced'
            superAtts[newDatasetId] = self._getSubAttr('DataObject', k)

        return superAtts

    def _getKlassMeta(self, key_, uri_):
        """
        """
        try:
            klass = type(globals()[key_]())
            _ = klass(uri=uri_)
            try:
                _.getMeta()
                # _.show()
                self.m[key_][uri_] = _.meta[uri_]
            except Exception:
                _logger.exception(f'can not found metadata from {key_}[{uri_}]')
                raise
        except Exception:
            _logger.exception(f'can not found class {key_}')
            raise

    def _getSubAttr(self, key_, uri_):
        """
        dict1 = {name: value, name: value, ...}
        """
        # check object type
        _ = ICPObj(uri=uri_)
        objtype = _.objtype

        dict1 = {}
        if objtype in self.m:
            if uri_ in self.m[objtype]:
                _logger.debug(f'explore dic[{objtype}][{uri_}]')
                for k, v in self.m[objtype][uri_].items():
                    if v.type != 'uri' or k == 'uri':
                        _logger.debug(f'attr name: {k} value: {v.value}')
                        dict1[k] = v.value
                    else:
                        _logger.debug(f'dic[{k}][{v.value}]')
                        dict2 = self._getSubAttr(k, v.value)
                        # Merge contents of dict2 in dict1
                        dict1.update(dict2)
            else:
                _logger.debug(f'can not found dic[{objtype}][{uri_}]')
                # look for metadata on ICOS CP
                self._getKlassMeta(objtype, uri_)
                dict2 = self._getSubAttr(objtype, uri_)
                # Merge contents of dict2 in dict1
                dict1.update(dict2)
        else:
            _logger.debug(f'can not found key {objtype}')
            # add empty sub dictionary
            self.m[objtype] = {}
            dict2 = self._getSubAttr(objtype, uri_)
            # Merge contents of dict2 in dict1
            dict1.update(dict2)

        return dict1

    def show(self, superAtts=None):
        """ print metadata read (name, type and value)

        superAtts = { ID : atts }
            atts = {name: value, ...}
        """
        if superAtts is None:
            superAtts = self.getAttr()

        _logger.info("\nSuperAtts:")
        _logger.info('\t'+pformat(superAtts))


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
