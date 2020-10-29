# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import Station
import GeoRegion
import DataSubmission
import DataObj
import chgXml
import chgCsv
from pathlib import Path
import subprocess

cc = chgXml.CamelCase()

storage = Path('/home/jpa029/Data/ICOS2ERDDAP')


def wait(msg=''):
    """

    :return:
    """
    if msg:
        print('\n'+msg)

    input("\nPress the <ENTER> key to continue...")
    print('\n')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    wait('get metadata from ICOS CP')

    stations = Station.get_meta()
    georegions = GeoRegion.get_meta()
    # dataSubmissions = DataSubmission.get_meta()

    print("\nstations")
    for k, v in stations.items():
        # print(k,' : ',v.stationId,v.stationName,v.countryCode)
        for kk, vv in v.items():
            print(kk, ' : ', 'type:', vv.type, 'value:', vv.value)

    print('\ngeoregions')
    for k, v in georegions.items():
        # print(k,' : ',v.label,v.comment)
        for kk, vv in v.items():
            print(kk, ' : ', 'type:', vv.type, 'value:', vv.value)

    print('\ndataSubmissions =================')
    if 'dataSubmissions' in locals():
        for k, v in dataSubmissions.items():
            print('k:', k)

    # what about new metadata add directly in older DataObj ??

    wait('loop on every new dataset load on ICOS CP (here just one)')
    # dataobjs=DataObj.get_meta(lastupdate='2020-01-01T00:00:00.000Z', endupdate='2020-08-05T00:00:00.000Z',
    #                           product='icosOtcL1Product_v2', lastVersion=True, dobj=)

    wait('\tget dataObj metadata from ICOS CP')
    dobj = 'https://meta.icos-cp.eu/objects/uwXo3eDGipsYBv0ef6H2jJ3Z'
    dataobjs = DataObj.get_meta(dobj=dobj)

    # output directory
    datasetDir = Path('/home/jpa029/Data/ICOS2ERDDAP/dataset')
    # erddap directories
    erddapDir = Path('/home/jpa029/Code/apache-tomcat-8.5.57')
    erddapWebInfDir = erddapDir / 'webapps' / 'erddap' / 'WEB-INF'
    erddapContentDir = erddapDir / 'content' / 'erddap'

    print('\ndataobjs')
    for k, v in dataobjs.items():
        for kk, vv in v.items():
            print(kk, ' : ', 'type:', vv.type, 'value:', vv.value
                  )

        uri = v['uri'].value  # Warning do not convert to Path (https:// => https./)
        pid = uri.split("/")[-1]
        print('pid', pid)
        filename = Path(v['name'].value)
        stemname = filename.stem
        # fname = v['name'].value[:v['name'].value.rfind(".")]
        print('filename: ', filename)
        print('stemname: ', stemname)

        # dirout = (storage / v['name'].value).with_suffix('')
        dirout = storage / stemname
        try:
            dirout.mkdir(parents=True)
        except FileExistsError:
            # directory already exists
            print('do nothing:', dirout)

        wait('\tdownload data locally')
        # load data
        url = str(uri).replace('meta', 'data')
        print('url:', url)
        fileout = dirout / filename
        DataObj.download(url, fileout)

        wait('\t change in csv file :\n\t\t- change Date/Time format\n\t\t- remove units for variable name')

        chgCsv.modify(fileout)

        wait('\trun ERDDAP GenerateDatasetXml tool to create dataset.xml file')

        # run GenerateDatasetXml
        cmdList = []
        exe = './GenerateDatasetsXml.sh'
        cmdList.append(exe)
        # Which EDDType (default="EDDGridFromDap")
        EDDType = 'EDDTableFromAsciiFiles'
        cmdList.append(EDDType)
        # Starting directory (default="")
        StartingDirectory = dirout
        cmdList.append(StartingDirectory)
        # File name regex (e.g., ".*\.asc") (default="")
        FileNameRegex = r'.*\.csv'
        cmdList.append(FileNameRegex)
        # Full file name of one file (or leave empty to use first matching fileName) (default="")
        FullFileNameOfOneFile = 'nothing'
        cmdList.append(FullFileNameOfOneFile)
        # Charset (e.g., ISO-8859-1 (default) or UTF-8) (default="")
        Charset = 'UTF-8'
        cmdList.append(Charset)
        # Column names row (e.g., 1) (default="")
        ColumnNamesRow = '1'
        cmdList.append(ColumnNamesRow)
        # First data row (e.g., 2) (default="")
        FirstDataRow = '2'
        cmdList.append(FirstDataRow)
        # Column separator (e.g., ',') (default="")
        ColumnSeparator = ','
        cmdList.append(ColumnSeparator)
        # ReloadEveryNMinutes (e.g., 10080) (default="")
        ReloadEveryNMinutes = 'default'
        cmdList.append(ReloadEveryNMinutes)
        # PreExtractRegex (default="")
        PreExtractRegex = 'default'
        cmdList.append(PreExtractRegex)
        # PostExtractRegex (default="")
        PostExtractRegex = 'default'
        cmdList.append(PostExtractRegex)
        # ExtractRegex (default="")
        ExtractRegex = 'default'
        cmdList.append(ExtractRegex)
        # Column name for extract (default="")
        ColumnNameForExtract = 'default'
        cmdList.append(ColumnNameForExtract)
        # Sorted column source name (default="")
        SortedColumnSourceName = 'default'
        cmdList.append(SortedColumnSourceName)
        # Sort files by sourceNames (default="")
        SortFilesBySourceNames = 'default'
        cmdList.append(SortFilesBySourceNames)
        # infoUrl (default="")
        infoUrl = 'default'
        cmdList.append(infoUrl)
        # institution (default="")
        institution = 'default'
        cmdList.append(institution)
        # summary (default="")
        summary = 'default'
        cmdList.append(summary)
        # title (default="")
        title = 'default'
        cmdList.append(title)
        # standardizeWhat (-1 to get the class' default) (default="")
        standardizeWhat = 'default'
        cmdList.append(standardizeWhat)
        # cacheFromUrl (default="")
        cacheFromUrl = 'default'
        cmdList.append(cacheFromUrl)

        # output dataset file
        datasetSubDir = datasetDir / stemname
        try:
            datasetSubDir.mkdir(parents=True)
        except FileExistsError:
            # directory already exists
            pass

        fout = Path.joinpath(datasetSubDir, "dataset."+stemname+".xml")
        if not fout.is_file():
            with open(fout, 'w') as f:
                f.write('<!-- Begin GenerateDatasetsXml #'+stemname+' someDate -->\n')
                f.write('<!-- End GenerateDatasetsXml #'+stemname+' someDate -->')

        # add tagName
        foutTag = Path.joinpath(datasetSubDir, "dataset."+stemname+".xml#"+stemname)
        cmdList.append('-i'+str(foutTag))

        print('running GenerateDatasetsXml.sh', cmdList)
        process = subprocess.run(cmdList,
                                 cwd=erddapWebInfDir,
                                 stdout=subprocess.PIPE,
                                 timeout=60,
                                 universal_newlines=True)
        process.check_returncode()

        newDatasetId = cc.datasetID(v)
        chgXml.renameDatasetId(fout, newDatasetId)

    wait('outside of the loop, concatenate every dataset file into one')
    # concatenate header.xml dataset.XXX.xml footer.xml into local datasets.xml
    dsxmlout = datasetDir / 'datasets.xml'
    print('dsxmlout:', dsxmlout)
    with dsxmlout.open("w") as fp:
        # add header
        header = datasetDir / 'header.xml'
        fp.write(header.read_text())
        # add single dataset
        for ff in datasetDir.glob('**/dataset.*.xml'):
            print('append ', ff)
            fp.write(ff.read_text())
        # add footer
        footer = datasetDir / 'footer.xml'
        fp.write(footer.read_text())

    wait('change/add metadata on datasets.xml file, considering metadata from ICOS CP')

    # change/add attributes into local datasets.xml
    meta = {'dataObj': dataobjs,
            'station': stations,
            'geoRegion': georegions}
    if 'dataSubmissions' in locals():
        meta['dataSubmission'] = dataSubmissions

    # o = dsxmlout.parents[0] / 'datasets.new.xml'
    o = dsxmlout
    chgXml.changeAttr(dsxmlout, o, meta)

    wait('replace erddap datasets.xml file with the new one')
    # remove erddap datasets.xml and create hard link to the new one
    dsxml = erddapContentDir / 'datasets.xml'
    if dsxml.is_file():  # and not dsxml.is_symlink():
        dsxml.unlink()

    print('create hard link to:', dsxmlout)
    dsxmlout.link_to(dsxml)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
