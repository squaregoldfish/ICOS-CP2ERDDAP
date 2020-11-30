#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SuperICPObj.py

"""
    This module set up a generic class for ICOS CP Object.

    Example usage:

    from ICPObj import ICPObj

    icpobj = ICPObj()   # initialise ICPObj
    icpobj.get_meta()   # get metadata from ICOS CP
    icpobj.show()       # print metadata
"""

# --- import -----------------------------------
# import from standard lib
import logging
# import from other lib
# > conda-forge
# import from my project
from icp2edd.DataObj import DataObj
from icp2edd.Station import Station
from icp2edd.GeoRegion import GeoRegion
from icp2edd.DataSubmission import DataSubmission
import icp2edd.case as case

# load logger
_logger = logging.getLogger(__name__)


# ----------------------------------------------
class SuperICPObj(object):
    def __init__(self, station=False, geoRegion=False, dataSubmission=False):
        self.m = {}

        uri = ['https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z']
        _logger.info('get DataObj metadata from ICOS CP')
        try:
            _ = DataObj(uri=uri)
            _.getMeta()
            self.m['DataObj'] = _.meta
            # dataobjs.show()
        except Exception:
            _logger.exception('Something goes wrong when loading metadata from DataObj')
            raise  # Throw exception again so calling code knows it happened

        if station:
            _logger.info('get Station metadata from ICOS CP')
            try:
                _ = Station()
                _.getMeta()
                self.m['Station'] = _.meta
            except Exception:
                _logger.exception('Something goes wrong when loading metadata from Station')
                raise  # Throw exception again so calling code knows it happened

        if geoRegion:
            _logger.info('get GeoRegion metadata from ICOS CP')
            try:
                _ = GeoRegion()
                _.getMeta()
                self.m['GeoRegion'] = _.meta
            except Exception:
                _logger.exception('Something goes wrong when loading metadata from GeoRegion')
                raise  # Throw exception again so calling code knows it happened

        if dataSubmission:
            _logger.info('get DataSubmission metadata from ICOS CP')
            try:
                _ = DataSubmission()
                _.getMeta()
                self.m['DataSubmission'] = _.meta
            except Exception:
                _logger.exception('Something goes wrong when loading metadata from DataSubmission')
                raise  # Throw exception again so calling code knows it happened

    def getAttr(self):
        """
        superAtts = { ID : atts }
            atts = {name: value, ...}
        """
        superAtts = {}
        for k in self.m['DataObj'].keys():
            fname = self.m['DataObj'][k]['name'].value[:self.m['DataObj'][k]['name'].value.rfind(".")]
            _logger.debug(f'get attribute from DataObj {fname}')
            newDatasetId = case.camel('icos_'+fname, sep='_')
            _logger.debug(f'rename it to {newDatasetId}')
            # newDatasetId = 'icos58gs20190711SocatEnhanced'
            superAtts[newDatasetId] = self._getSubAttr('DataObj', k)

        return superAtts

    def _getSubAttr(self, key, uri):
        dict1 = {}
        if key in self.m:
            if uri in self.m[key]:
                _logger.debug(f'explore dic[{key}][{uri}]')
                for k, v in self.m[key][uri].items():
                    if v.type != 'uri' or k == 'uri':
                        _logger.debug(f'attr name: {k} value: {v.value}')
                        dict1[k] = v.value
                    else:
                        _logger.debug(f'dic[{k}][{v.value}]')
                        dict2 = self._getSubAttr(k, v.value)
                        # Merge contents of dict2 in dict1
                        dict1.update(dict2)
            else:
                _logger.debug(f'can not found dic[{key}][{uri}]')
        else:
            _logger.debug(f'can not found dic[{key}]')

        return dict1

    def show(self, superAtts=None):
        """ print metadata read (name, type and value)

        superAtts = { ID : atts }
            atts = {name: value, ...}
        """
        if superAtts is None:
            superAtts = self.getAttr()

        for k, v in superAtts.items():
            print('datasetID: {}'.format(k))
            for kk, vv in v.items():
                print('\t{:10}: {}'.format(kk, vv))


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
