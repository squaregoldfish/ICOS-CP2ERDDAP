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
import traceback
from pprint import pformat
# import from other lib
# > conda-forge
# import from my project
import icp2edd.setupcfg as setupcfg
from icp2edd.icpObj import ICPObj
# import all class from submodules in cpmeta
from icp2edd.cpmeta import *
import icp2edd.util as util

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

list_VariableObject = ["DatasetVariable", "DatasetColumn"]
list_DataObject = ["DataObject"]


# ----------------------------------------------
class SuperICPObj(object):
    """ """
    def __init__(self):
        """ """
        self.meta = {}
        self.DataObject = {}
        self.DataVariable = {}
        #
        self.tmp = {}

        # list uri of all datasets already loaded
        listuri = self._listDatasetLoaded()
        try:
            _logger.info('get DataObject metadata from ICOS CP')
            _ = DataObject(uri=listuri)
            _.getMeta()
            _.show()
            #
            self.meta = _.meta
        except Exception:
            _logger.exception('Something goes wrong when loading metadata from DataObject')
            raise  # Throw exception again so calling code knows it happened

        # get instance name
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self._instance_name = text[:text.find('=')].strip()

    def getAttr(self):
        """
        """
        list_dataObj = self.meta.keys()
        # fill self.meta
        for uri in list_dataObj:
            print(f"\nlook in uri: {uri} ", end="")
            _logger.info(f"look in uri: {uri}")
            self._getSubAttr(uri)
        print(f"")

        # ll=['http://meta.icos-cp.eu/resources/cpmeta/temperature','http://meta.icos-cp.eu/resources/cpmeta/portion','http://meta.icos-cp.eu/resources/cpmeta/salinity']
        # self.repackMeta(self.meta.keys())
        # print(pformat(self.tmp))

        # repack with objtype
        for uri in list_dataObj:
            # get object type
            print(f"\nspread in uri: {uri} ", end="")
            self.repack(uri)
        print(f"")

        return {**self.DataObject, **self.DataVariable}

    def repack(self, uri_):
        # TODO see if it could be merge with getSubAttr
        def spread(uri_, exclude_=[], cnt_=0):

            cnt_ += 1
            print('.'*cnt_, end="", flush=True)

            self.tmp[uri_] = {}
            if uri_ not in self.meta.keys():
                _logger.critical(f"Try to spread unknown uri -{uri_}-")
                raise SystemExit(1)

            for k, lv in self.meta[uri_].items():
                if k in ['uri']:
                    _logger.debug(f"ignore uri attribute")
                    # if k not in self.tmp[uri_].keys():
                    #     d = {k: str(lv[0].value)}
                    #     self.tmp[uri_] = util.combine_dict_in_list(d, self.tmp[uri_])
                elif k in ['NextVersionOf', 'RevisionOf', 'PrimarySource', 'QualityFlagFor']:  # TODO create global list shared between modules
                    _logger.debug(f'ignore {k} attribute. do not iterate to avoid recursive search')
                else:
                    for v in lv:
                        d = {}
                        if v.type != 'uri':
                            d[k] = [v.value]
                        else:
                            objtype = ICPObj(uri=v.value).objtype
                            if objtype not in exclude_:
                                if v.value in self.tmp.keys():
                                    for kk, vv in self.tmp[v.value].items():
                                        kkk = k + '_' + kk
                                        d[kkk] = vv
                                else:
                                    d = spread(v.value, exclude_=exclude_, cnt_=cnt_)
                            else:
                                self.repack(v.value)

                        self.tmp[uri_] = util.combine_dict_in_list(d, self.tmp[uri_])

            return self.tmp[uri_]

        # check object type
        _ = ICPObj(uri=uri_)
        objtype = _.objtype

        if objtype in list_DataObject:
            filename = Path(self.meta[uri_]['static_object_name'][0].value)
            # datasetId = case.camel('icos_' + filename.stem, sep='_')
            datasetId = util.datasetidCase(filename)

            self.DataObject[datasetId] = spread(uri_, exclude_=list_VariableObject)

        elif objtype in list_VariableObject:
            varname = self.meta[uri_]['dataset_column_column_title'][0].value
            # variableId = case.camel(varname, sep='_')

            self.DataVariable[varname] = spread(uri_)

        else:
            _logger.error(f"should not be run on {objtype}")

        # clean
        self.tmp = {}

    # def repackMeta(self, list_obj_)        # TODO see if it could be merge with getSubAttr:

    #     def _repack_list_uri(list_uri_):
    #         """ set up dictionaries for each uri

    #         :param list_uri_: list of uri to fill
    #         :return: list of uri not filled yet
    #         """
    #         list_uri = []
    #         for uri in list_uri_:
    #             if not uri in self.tmp.keys():
    #                 _ = _repack_uri(uri)
    #                 empty = not bool(_)
    #                 if not empty:
    #                     self.tmp[uri] = _

    #                     # check object type
    #                     objtype = ICPObj(uri=uri).objtype

    #                     if objtype in list_DataObject:
    #                         filename = Path(self.meta[uri]['static_object_name'][0].value)
    #                         # datasetId = case.camel('icos_' + filename.stem, sep='_')
    #                         datasetId = util.datasetidCase(filename)
    #                         # self.DataObject[datasetId] = _
    #                         self.DataObject[datasetId] = {k:v for k,v in _.items() if not any(x in k for x in list_VariableObject)}

    #                     elif objtype in list_VariableObject:
    #                         varname = self.meta[uri]['dataset_column_column_title'][0].value
    #                         # variableId = case.camel(varname, sep='_')
    #                         self.DataVariable[varname] = _

    #                 else:
    #                     list_uri.append(uri)

    #         return list_uri

    #     def _repack_uri(uri_):
    #         """ set up dictionary for one uri

    #         :param uri_:
    #         "return: dictionary
    #         """
    #         _ = {}
    #         for k, lv in self.meta[uri_].items():
    #             if k in ['uri']:
    #                 _logger.debug(f"ignore uri attribute")
    #             elif k in ['NextVersionOf', 'RevisionOf', 'PrimarySource', 'QualityFlagFor']: # TODO create global list shared between modules
    #                 _logger.debug(f'ignore {k} attribute. do not iterate to avoid recursive search')
    #             else:
    #                 for v in lv:
    #                     d = _repack_key_val(k, v)
    #                     empty = not bool(d)
    #                     if not empty:
    #                         _ = util.combine_dict_in_list(d, _)
    #                     else:
    #                         return {}
    #         return _

    #     def _repack_key_val(k_, v_):
    #         """
    #         >>> k_ = 'x'
    #         >>> v_ = Value('literal','toto')
    #         >>> _repack_key_val(k_, v_)
    #         {'x': ['toto']}

    #         >>> k_ = 'y'
    #         >>> v_ = Value('uri','http://x')
    #         >>> _repack_key_val(k_, v_)
    #         {'y_x':['toto']}

    #         :param k_:
    #         :param v_:
    #         :return: dictionary
    #         """
    #         _ = {}
    #         if v_.type != 'uri':
    #             _[k_] = [v_.value]
    #         else:
    #             if v_.value in self.tmp.keys():
    #                 for kk, vv in self.tmp[v_.value].items():
    #                     kkk = k_ + '_' + kk
    #                     _[kkk] = vv
    #             else:
    #                 return {}
    #         return _

    #     attempt = 0
    #     max_allowed = 10
    #     list_obj = list_obj_
    #     while list_obj:
    #         attempt += 1
    #         if attempt == max_allowed+1:
    #             _logger.critical(f"You've reached the maximum number of attempt to repack metadata.")
    #             raise RuntimeError
    #         else:
    #             list_obj = _repack_list_uri(list_obj)

    def _getSubAttr(self, uri_, cnt_=0):
        """
        dict1 = {name: value, name: value, ...}

        special cases for keys 'uri' and 'NextVersionOf'.
        - 'uri': do not iterate to avoid infinity loop
        - 'NextVersionOf' : do not iterate to avoid recursive search inside previous versions
        """
        cnt_ += 1
        print('.'*cnt_, end="", flush=True)

        for k, lv in self.meta[uri_].items():
            if k == 'uri':
                # do nothing, you are currently exploring it
                _logger.debug(f"do nothing, you are currently exploring this uri -{k}-")
            elif k in ['NextVersionOf', 'RevisionOf', 'PrimarySource', 'QualityFlagFor']:
                # Warning: linked to:
                # - 'cpmeta:isNextVersionOf' in StaticObject, and Collection
                # - 'cpmeta:isQualityFlagFor' in DatasetColumn
                # - 'prov:hadPrimarySource'  in StaticObject, and Collection
                # - 'prov:wasRevisionOf'     in StaticObject, and Collection
                _logger.debug(f'key {k} found. do not iterate to avoid recursive search')
            else:
                for v in lv:
                    if v.type == 'uri':
                        uri = v.value
                        if uri in self.meta:
                            _logger.debug(f"do nothing, uri -{uri}- already in meta")
                        else:
                            # check object type
                            _ = ICPObj(uri=uri)
                            objtype = _.objtype

                            try:
                                klass = type(globals()[objtype]())
                                _ = klass(uri=uri)
                                try:
                                    _.getMeta()
                                    self.meta = {**_.meta, **self.meta}
                                    _logger.debug(f'dig into to explore {objtype} uri: {uri}')
                                    self._getSubAttr(uri, cnt_)
                                except Exception:
                                    _logger.exception(f'can not found metadata from {objtype}[{uri}]')
                                    raise
                            except Exception:
                                _logger.exception(f'can not found class {objtype}')
                                raise

    def _listDatasetLoaded(self):
        """
        """
        # list directory containing csv file, return directory name
        output = set()
        for csv in setupcfg.datasetCsvPath.glob('**/*.csv'):
            output.add(csv.parent.name+'.csv')

        # list URI related to those directory name(s)
        _ = DataObject()
        return _.listUri(list(output))

    def show(self,  print_=False):

        if not isinstance(print_, bool):
            _logger.error(f"Invalid type argument -{print_}-")
            raise TypeError("Invalid type argument")

        _logger.info(f"Class name: SuperICPObj:\n {pformat(self.meta)}")
        if print_:
            print("\nClass name: SuperICPObj")
            print('\t'+pformat(self.meta))

        _logger.info(f"DataObject dictionary:\n {pformat(self.DataObject)}")
        if print_:
            # Check if dictionary is empty
            empty = not bool(self.DataObject)
            print("\nDataObject dictionary:")
            if not empty:
                print(f"\t{pformat(self.DataObject)}")
            else:
                print(f"\tself.DataObject dictionary empty !")

        _logger.info(f"DataVariable dictionary:\n {pformat(self.DataVariable)}")
        if print_:
            # Check if dictionary is empty
            empty = not bool(self.DataVariable)
            print("\nDataVariable dictionary:")
            if not empty:
                print(f"\t{pformat(self.DataVariable)}")
            else:
                print(f"\tself.DataVariable dictionary empty !")


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
