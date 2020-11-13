# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

__author__ = ["Julien Paul"]
__credits__ = ""
__license__ = "CC BY-SA 4.0"
__version__ = "0.0.0"
__maintainer__ = "BCDC"
__email__ = ['julien.paul@uib.no']
__status__ = ""

# ----------------------------------------------
# import from standard lib
from pathlib import Path
# import from other lib
# import from my project
from icp2edd.SuperICPObj import SuperICPObj
from icp2edd.Station import Station
from icp2edd.GeoRegion import GeoRegion
from icp2edd.DataSubmission import DataSubmission
from icp2edd.DataObj import DataObj
import icp2edd.Xml4Erddap as x4edd
import icp2edd.csv4Erddap as c4edd

# ----------------------------------------------
storage = Path('/home/jpa029/Data/ICOS2ERDDAP')
# TODO check input argument everywhere


# ----------------------------------------------
def wait(msg=''):
    """

    :return:
    """
    if msg:
        print('\n'+msg)

    # input("\nPress the <ENTER> key to continue...")
    print('\n')


def main():

    # TODO create config file
    # TODO first part get new dataObj on ICOS CP, and create associated ERDDAP dataset.xml

    # wait('\tget DataObj metadata from ICOS CP')
    uri = 'https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z'
    dataobjs = DataObj(uri=uri)

    # dataobjs=DataObj(lastupdate='2020-01-01T00:00:00.000Z',
    #                  endupdate='2020-08-05T00:00:00.000Z',
    #                  product='icosOtcL1Product_v2',
    #                  lastVersion=True)

    print('\nDataObj')
    dataobjs.getMeta()
    dataobjs.show()
    dd = dataobjs.download()
    for csv, rep in dd.items():

        wait('\t change in csv file :\n\t\t- change Date/Time format\n\t\t- remove units for variable name')

        fileout = Path.joinpath(rep, csv)
        c4edd.modify(fileout)

        wait('\trun ERDDAP GenerateDatasetXml tool to create dataset.xml file')
        dirout = fileout.parents[0]
        xml = x4edd.Xml4Erddap(dirout)
        # run GenerateDatasetXml
        xml.generate()

    # wait('outside of the loop, concatenate every dataset file into one')
    # concatenate header.xml dataset.XXX.xml footer.xml into local datasets.xml
    dsxmlout = x4edd.concatenate()

    # TODO second part get ICOS CP metadata up to date, and update ERDDAP datasets.xml
    wait('change/add metadata on datasets.xml file, considering metadata from ICOS CP')

    wait('get metadata from ICOS CP')

    print("\nStation")
    stations = Station()
    stations.getMeta()
    # stations.show()

    print('\nGeoRegion')
    georegions = GeoRegion()
    georegions.getMeta()
    # georegions.show()

    print('\nDataSubmission')
    # datasubmissions = DataSubmission()
    # datasubmissions.getMeta()
    # datasubmissions.show()

    # TODO what about new metadata add directly in older DataObj ??
    # get all metadata from dataObj use by ERDDAP

    wait('loop on every new dataset load on ICOS CP (here just one)')
    uri = 'https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z'
    print('\nDataObj')
    dataobjs = DataObj(uri=uri)
    dataobjs.getMeta()
    # dataobjs.show()

    print('==============================')
    extra = SuperICPObj(dataSubmission=False)
    gloatt = extra.getAttr()
    gloatt['Date/Time'] = {'standard_name': 'tutu', 'titi': 'tata'}

    extra.show(gloatt)

    # change/add attributes into local datasets.xml
    x4edd.changeAttr(dsxmlout, gloatt)

    wait('replace erddap datasets.xml file with the new one')
    x4edd.replaceXmlBy(dsxmlout)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
