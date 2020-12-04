#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __main__.py

# ----------------------------------------------
# import from standard lib
import logging
# import from other lib
# import from my project
import icp2edd.setup as setup
import icp2edd.Xml4Erddap as x4edd
import icp2edd.csv4Erddap as c4edd
from icp2edd.superIcpObj import SuperICPObj
# import all class from submodules in otcmeta
from icp2edd.otcmeta import *
# import all class from submodules in cpmeta
from icp2edd.cpmeta import *


# ----------------------------------------------
def main():

    # TODO test args
    # set up logger, paths, ...
    setup.main()
    _logger = logging.getLogger(__name__)

    # TODO first part get new dataObj on ICOS CP, and create associated ERDDAP dataset.xml
    _logger.info('-1- get new dataObj on ICOS CP, and create associated ERDDAP dataset.xml\n')

    _logger.info('get DataObj metadata from ICOS CP')
    try:
        uri = 'https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z'
        dataobjs = DataObject(uri=uri)
    except Exception:
        _logger.exception('Something goes wrong when setting up DataObj')
        raise  # Throw exception again so calling code knows it happened

    # dataobjs=DataObj(lastupdate='2020-01-01T00:00:00.000Z',
    #                  endupdate='2020-08-05T00:00:00.000Z',
    #                  product='icosOtcL1Product_v2',
    #                  lastVersion=True)

    _logger.info('read DataObj from ICOS-CP:')
    try:
        dataobjs.getMeta()
    except Exception:
        _logger.exception('Something goes wrong when loading DataObj metadata')
        raise  # Throw exception again so calling code knows it happened

    # dataobjs.show()

    try:
        dd = dataobjs.download()
    except Exception:
        _logger.exception('Something goes wrong when downloading DataObj data')
        raise  # Throw exception again so calling code knows it happened

    for csv, rep in dd.items():

        _logger.info('change in csv file :\n\t\t- change Date/Time format\n\t\t- remove units for variable name')
        try:
            fileout = Path.joinpath(rep, csv)
            c4edd.modify(fileout)
        except Exception:
            _logger.exception('Something goes wrong when modifying cvs file')
            raise  # Throw exception again so calling code knows it happened

        _logger.info('run ERDDAP GenerateDatasetXml tool to create dataset.xml file')
        try:
            dirout = fileout.parents[0]
            xml = x4edd.Xml4Erddap(dirout)
        except Exception:
            _logger.exception('Something goes wrong when initialising Xml2ERDDAP object')
            raise  # Throw exception again so calling code knows it happened

        # run GenerateDatasetXml
        try:
            xml.generate()
        except Exception:
            _logger.exception('Something goes wrong when generating ERDDAP dataset.xml file')
            raise  # Throw exception again so calling code knows it happened

    _logger.info('concatenate every dataset file(s) into one')
    # concatenate header.xml dataset.XXX.xml footer.xml into local datasets.xml
    dsxmlout = x4edd.concatenate()

    # TODO second part get ICOS CP metadata up to date, and update ERDDAP datasets.xml
    _logger.info('-2- get ICOS CP metadata up to date, and update ERDDAP datasets.xml\n')
    _logger.info('change/add metadata on datasets.xml file, considering metadata from ICOS CP')

    _logger.info('get Station metadata from ICOS CP')
    try:
        stations = Station()
        stations.getMeta()
        # stations.show()
    except Exception:
        _logger.exception('Something goes wrong when loading metadata from Station')
        raise  # Throw exception again so calling code knows it happened

    _logger.info('get GeoRegion metadata from ICOS CP')
    try:
        georegions = GeoRegion()
        georegions.getMeta()
        # georegions.show()
    except Exception:
        _logger.exception('Something goes wrong when loading metadata from GeoRegion')
        raise  # Throw exception again so calling code knows it happened

    _logger.info('get DataSubmission metadata from ICOS CP')
    try:
        datasubmissions = DataSubmission()
        datasubmissions.getMeta()
        # datasubmissions.show()
    except Exception:
        _logger.exception('Something goes wrong when loading metadata from DataSubmission')
        raise  # Throw exception again so calling code knows it happened

    # TODO what about new metadata add directly in older DataObj ??
    # get all metadata from dataObj use by ERDDAP

    _logger.info('loop on every new dataset load on ICOS CP (here just one)')
    uri = ['https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z']
    _logger.info(f'get DataObj metadata from ICOS CP')
    try:
        dataobjs = DataObject(uri=uri)
        dataobjs.getMeta()
        # dataobjs.show()
    except Exception:
        _logger.exception('Something goes wrong when loading metadata from DataSubmission')
        raise  # Throw exception again so calling code knows it happened

    _logger.info(f'initialise SuperICPObj object')
    try:
        extra = SuperICPObj(dataSubmission=False)
        gloatt = extra.getAttr()
        gloatt['Date/Time'] = {'standard_name': 'tutu', 'titi': 'tata'}

        # extra.show(gloatt)
    except Exception:
        _logger.exception('Something goes wrong when initialising SuperICPObj')
        raise  # Throw exception again so calling code knows it happened

    try:
        _logger.info('change/add attributes into local datasets.xml')
        x4edd.changeAttr(dsxmlout, gloatt)
        _logger.info('replace ERDDAP datasets.xml file with the new one')
        x4edd.replaceXmlBy(dsxmlout)
    except Exception:
        _logger.exception('Something goes wrong when changing/adding attributes into ERDDAP datasets.xml')
        raise  # Throw exception again so calling code knows it happened


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        main()
    except Exception:
        logging.exception('Something goes wrong!!!')
        raise  # Throw exception again so calling code knows it happened

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
