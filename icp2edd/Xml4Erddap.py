#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xml4Erddap.py

# --- import -----------------------------------
# import from standard lib
from pathlib import Path
import re
import os
import subprocess
# from importlib import resources
# import from other lib
# > conda forge
import lxml.etree as etree
# import from my project
import icp2edd.case as case

# --- module's variable ------------------------
global erddapPath, erddapWebInfDir, erddapContentDir, datasetXmlPath


def setupcfg(cfg_=None):
    """

    >>> setupcfg()
    >>> setupcfg(toto)
    Traceback (most recent call last):
    ...
        setupcfg(toto)
    NameError: name 'toto' is not defined
    >>> setupcfg('toto')
    Traceback (most recent call last):
    ...
        erddapPath = Path(cfg_['ERDDAP']['path'].get('string'))
    TypeError: string indices must be integers
    """
    import confuse  # Initialize config with your app
    global erddapPath, erddapWebInfDir, erddapContentDir, datasetXmlPath

    if cfg_ is None:
        cfg_ = confuse.Configuration('icp2edd', modname='icp2edd')  # Get a value from your YAML file
        pkg_path = Path(cfg_._package_path)
        cfg_.default_config_path = pkg_path / confuse.DEFAULT_FILENAME

    erddapPath = Path(cfg_['paths']['erddap'].get('string'))

    if not erddapPath.is_dir():
        raise FileNotFoundError('can not find ERDDAP path {}.\n'
                                'Check config file(s) {} and/or {}'.format(erddapPath,
                                                                           cfg_.user_config_path(),
                                                                           cfg_.default_config_path))

    erddapWebInfDir = erddapPath / 'webapps' / 'erddap' / 'WEB-INF'
    if not erddapWebInfDir.is_dir():
        raise FileNotFoundError('can not find ERDDAP sub-directory {} \n'
                                'check ERDDAP installation. '.format(erddapWebInfDir))

    erddapContentDir = erddapPath / 'content' / 'erddap'
    if not erddapContentDir.is_dir():
        raise FileNotFoundError('can not find ERDDAP sub-directory {} \n'
                                'check ERDDAP installation'.format(erddapContentDir))

    datasetXmlPath = Path(cfg_['paths']['dataset']['xml'].as_filename())
    if not datasetXmlPath.is_dir():
        raise FileNotFoundError('can not find path where store dataset xml file {}.\n'
                                'Check config file(s) {} and/or {}'.format(datasetXmlPath,
                                                                           cfg_.user_config_path(),
                                                                           cfg_.default_config_path))


class Xml4Erddap(object):
    """
    >>> xxx = Xml4Erddap()
    Traceback (most recent call last):
    ...
        xxx = Xml4Erddap()
    TypeError: __init__() missing 1 required positional argument: 'dirout_'
    >>> xxx = Xml4Erddap(Path('/home/jpa029/Data/ICOS2ERDDAP/58GS20190711_SOCAT_enhanced'))
    >>> xxx = Xml4Erddap('/home/jpa029/Data/ICOS2ERDDAP/58GS20190711_SOCAT_enhanced', eddType='EDDTableFromAsciiFiles')
    >>> xxx = Xml4Erddap('/home/jpa029/Data/ICOS2ERDDAP/58GS20190711_SOCAT_enhanced', eddType='EDDTableFromAscii')
    Traceback (most recent call last):
    ...
        raise NameError('EDDType -{}- unknown by ERDDAP'.format(self._eddType))
    NameError: EDDType -EDDTableFromAscii- unknown by ERDDAP
    >>> xxx._show()
    >>> xxx._checkArgs()
    21
    >>> xxx._eddType='EDDTableFromAscii'
    >>> xxx._checkArgs()
    Traceback (most recent call last):
    ...
        raise NameError('EDDType -{}- unknown by ERDDAP'.format(self._eddType))
    NameError: EDDType -EDDTableFromAscii- unknown by ERDDAP
    >>> xxx._eddType='EDDTableFromAsciiFiles'
    >>> xxx.generate()
    creates dataset: ...
    renames datasetID to ...
    """
    def __init__(self, dirout_, eddType='EDDTableFromAsciiFiles'):
        """

        :param dirout_:
        :param eddType:

        read parameters

        datasetDir : global file
        """
        if not isinstance(dirout_, Path):
            dirout_ = Path(dirout_)

        # TODO check for csv file in sub directories
        if len(list(dirout_.glob('*.csv'))) <= 0:
            raise FileNotFoundError('no csv file in '+dirout_)

        self._stem = dirout_.stem
        self._eddType = eddType
        # dataset name
        self._ds = "dataset." + self._stem + ".xml"
        # dataset file
        self.ds = None

        self._cmd = []
        if self._eddType == 'EDDTableFromAsciiFiles':
            # TODO read those parameters in some config file,
            #  see https://github.com/beetbox/confuse/issues/30
            # Which EDDType (default="EDDGridFromDap")
            self._eddType = 'EDDTableFromAsciiFiles'
            self._cmd.append(self._eddType)
            # Starting directory (default="")
            self._cmd.append(dirout_)
            # File name regex (e.g., ".*\.asc") (default="")
            self._cmd.append(r'.*\.csv')
            # Full file name of one file (or leave empty to use first matching fileName) (default="")
            self._cmd.append('nothing')
            # Charset (e.g., ISO-8859-1 (default) or UTF-8) (default="")
            self._cmd.append('UTF-8')
            # Column names row (e.g., 1) (default="")
            self._cmd.append('1')
            # First data row (e.g., 2) (default="")
            self._cmd.append('2')
            # Column separator (e.g., ',') (default="")
            self._cmd.append(',')
            # ReloadEveryNMinutes (e.g., 10080) (default="")
            self._cmd.append('default')
            # PreExtractRegex (default="")
            self._cmd.append('default')
            # PostExtractRegex (default="")
            self._cmd.append('default')
            # ExtractRegex (default="")
            self._cmd.append('default')
            # Column name for extract (default="")
            self._cmd.append('default')
            # Sorted column source name (default="")
            self._cmd.append('default')
            # Sort files by sourceNames (default="")
            self._cmd.append('default')
            # infoUrl (default="")
            self._cmd.append('default')
            # institution (default="")
            self._cmd.append('default')
            # summary (default="")
            self._cmd.append('default')
            # title (default="")
            self._cmd.append('default')
            # standardizeWhat (-1 to get the class' default) (default="")
            self._cmd.append('default')
            # cacheFromUrl (default="")
            self._cmd.append('default')
        else:
            raise NameError('EDDType -{}- unknown by ERDDAP'.format(self._eddType))

    def _show(self):
        print('EDDType:', self._eddType)
        print('dataset:', self._ds)
        print('cmd    :', self._cmd)
        print('stem   :', self._stem)

    def _checkArgs(self):
        """

        :return: the number of arguments needed by ERDDAP's GenerateDatasetsXml.sh tool
        """
        if self._eddType == 'EDDTableFromAsciiFiles':
            # number of arguments -without executable-
            return 21
        else:
            raise NameError('EDDType -{}- unknown by ERDDAP'.format(self._eddType))

    def generate(self):
        """ generate dataset.xml file using ERDDAP tools -GenerateDatasetsXml.sh-
        """
        # This is a global variable
        global datasetXmlPath

        if len(self._cmd) != self._checkArgs():
            raise ValueError('Invalid arguments number -{}-, expected -{}-'.format(len(self._cmd), self._checkArgs()))

        # output dataset file
        if not isinstance(datasetXmlPath, Path):
            datasetXmlPath = Path(datasetXmlPath)

        # creates sub directory
        datasetSubDir = datasetXmlPath / self._stem
        try:
            datasetSubDir.mkdir(parents=True)
        except FileExistsError:
            # directory already exists
            pass

        # creates empty dataset file
        self.ds = Path.joinpath(datasetSubDir, self._ds)
        tag = '#' + self._stem
        tagline = '<!-- Begin GenerateDatasetsXml ' + tag + ' someDate -->'
        if not self.ds.is_file():
            with open(self.ds, 'w') as f:
                f.write(tagline+'\n')
                f.write(re.sub('Begin', 'End', tagline))
        else:
            # if file already exists, check taglines in file
            if not self._checkTag(self.ds, tagline):
                raise ValueError('file {} does not contains tags: {} and {}'
                                 .format(self.ds, tagline, re.sub('Begin', 'End', tagline)))

        # inserts executable
        exe = './GenerateDatasetsXml.sh'
        self._cmd.insert(0, exe)

        # add tag to dataset name
        dstag = Path.joinpath(datasetSubDir, self._ds + tag)
        self._cmd.append('-i' + str(dstag))

        e = Path.joinpath(erddapWebInfDir, exe)
        # Check file exists
        if not e.is_file():
            raise FileNotFoundError("Can not find ERDDAP tools {}".format(e))

        # Check for execution access
        if not os.access(e, os.X_OK):
            # change permission mode
            e.chmod(0o744)
            # raise PermissionError("")

        # run process 'GenerateDatasetsXml.sh' from directory 'erddapWebInfDir' with arguments 'self._cmd'
        # => creates file: ds
        process = subprocess.run(self._cmd,
                                 cwd=erddapWebInfDir,
                                 stdout=subprocess.PIPE,
                                 timeout=60,
                                 universal_newlines=True)
        process.check_returncode()
        print('creates dataset: {}'.format(self.ds))

        newDatasetId = case.camel('icos_'+self._stem, sep='_')
        self.renameDatasetId(newDatasetId)

    def renameDatasetId(self, newDatasetId):
        """ search for and replace datasetId name in dataset file.

        :param newDatasetId: datasetId name to be put in
        :return: overwrite dataset file
        """
        content = self.ds.read_text()
        regex = '(^<dataset .* datasetID=")(.*)(" .*>$)'
        self.ds.write_text(re.sub(regex, r'\1' + newDatasetId + r'\3', content, flags=re.M))
        print('renames datasetID to {}'.format(newDatasetId))

    def _checkTag(self, ds_, tagline_):
        """
        check if both taglines:
            <!-- Begin GenerateDatasetsXml #XXX someDate -->
            <!-- End GenerateDatasetsXml #XXX someDate -->
        are presented in ds file.

        XXX is the name of the dataset (without suffix)
        """
        content = ds_.read_text()

        # 2020-11-04T15:34:08
        # tagline = re.sub('someDate', '.*', tagline_)
        tagline = re.sub('someDate', '(someDate|[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2})', tagline_)
        if re.search(tagline, content):
            tagline = re.sub('Begin', 'End', tagline)

        return re.search(tagline, content)


def concatenate():
    """ concatenate header.xml dataset.XXX.xml footer.xml into local datasets.xml

    >>> xmlout = concatenate()
    concatenate in .../datasets.xml
    \t.../header.xml
    ...
    \t.../footer.xml
    >>> xmlout.__str__()
    '.../datasets.xml'
    """
    # This is a global variable
    global datasetXmlPath

    if not isinstance(datasetXmlPath, Path):
        datasetXmlPath = Path(datasetXmlPath)

    dsxmlout = datasetXmlPath / 'datasets.xml'
    print('concatenate in {}'.format(dsxmlout))
    mod_path = Path(__file__).parent
    with dsxmlout.open("w") as fp:
        # add header
        header = mod_path / 'dataset' / 'header.xml'
        # TODO see how to use resources
        # header = resources.path('dataset', 'header.xml')
        print('\t{}'.format(header))
        fp.write(header.read_text())
        # add single dataset
        for ff in datasetXmlPath.glob('**/dataset.*.xml'):
            print('\t{}'.format(ff))
            fp.write(ff.read_text())
        # add footer
        footer = mod_path / 'dataset' / 'footer.xml'
        print('\t{}'.format(footer))
        fp.write(footer.read_text())

    return dsxmlout


def changeAttr(ds, gloatt, out=None):
    """
    :param ds: str
       input filename
    :param gloatt: dictionary
       global and variable attribute to be added
    :param out: str
        output filename, optional
    """

    if not isinstance(ds, Path):
        ds = Path(ds)

    if not ds.is_file():
        raise FileExistsError(' File {} does not exist.'.format(ds))
    else:
        print('tree : ', ds)
    # keep CDATA as it is
    parser = etree.XMLParser(strip_cdata=False, encoding='ISO-8859-1')

    tree = etree.parse(str(ds), parser)
    root = tree.getroot()

    # prevent creation of self-closing tags
    for node in root.iter():
        if node.text is None:
            node.text = ''

    print('\n---------------')
    # for node in list(root):
    #    if node is not None:
    # TODO need to test with variable attributes to add at every variables whatever datasedID
    for node in root.findall('dataset'):
        print('node :', node.tag, node.attrib)
        if 'datasetID' in node.attrib:

            dsID = node.attrib.get('datasetID')
            if dsID in gloatt:
                print('dsID:', dsID)
                for attrNode in node.findall('addAttributes'):
                    print('attrNode :', attrNode.tag, attrNode.attrib)
                    for att in attrNode.iter('att'):
                        print('att name:', att.get('name'), 'val:', att.text)
                        if att.get('name') in gloatt[dsID]:
                            # TODO figure out how to keep information not to be changed
                            attrNode.remove(att)
                    for k, v in gloatt[dsID].items():
                        # for k, v in gloatt.items():
                        subnode = etree.SubElement(attrNode, 'att', name=k)
                        subnode.text = str(v)

        for varNode in node.iter('dataVariable'):
            print('varNode :', varNode.tag, varNode.attrib)
            srcname = None
            for attrNode in varNode.findall('sourceName'):
                srcname = attrNode.text
                print('srcname', srcname)
            # for attrNode in varNode.findall('destinationName'):
            #     dstname = attrnode.text
            if srcname in gloatt:
                for attrNode in varNode.findall('addAttributes'):
                    print('attrNode :', attrNode.tag, attrNode.attrib)
                    for att in attrNode.iter('att'):
                        print('att name:', att.get('name'), 'val:', att.text)
                        if att.get('name') in gloatt[srcname]:
                            attrNode.remove(att)
                    for k, v in gloatt[srcname].items():
                        subnode = etree.SubElement(attrNode, 'att', name=k)
                        subnode.text = str(v)

            etree.indent(node)

    # write xml output
    print('input ', str(ds))
    if out is not None:
        dsout = out
    else:
        dsout = ds

    print('output', str(dsout))
    tree.write(str(dsout), encoding='ISO-8859-1', xml_declaration=True)


def replaceXmlBy(dsxmlout):
    """ overwrite erddap datasets.xml with the new one
    :param dsxmlout:
    """
    # remove erddap datasets.xml and create hard link to the new one
    dsxml = erddapContentDir / 'datasets.xml'
    if dsxml.is_file():  # and not dsxml.is_symlink():
        dsxml.unlink()

    print('create hard link to:', dsxmlout)
    dsxmlout.link_to(dsxml)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # d = Path('/home/jpa029/Data/ICOS2ERDDAP/dataset/58GS20190711_SOCAT_enhanced')
    # i = d / 'dataset.58GS20190711_SOCAT_enhanced.xml'
    # renameDatasetId(i, 'toto')

    # d = '/home/jpa029/PycharmProjects/ICOS2ERDDAP/data'
    # d = Path('/home/jpa029/Data/ICOS2ERDDAP/dataset')
    # i = d / 'datasets.xml'
    # o = d / 'datasets.new.xml'
    # i = d / 'testcdata.xml'
    # o = d / 'testcdata.new.xml'
    # m = {}
    # changeAttr(i, o, m)

    import doctest
    setupcfg()
    doctest.testmod(extraglobs={'datasetXmlPath': datasetXmlPath, 'erddapPath': erddapPath,
                                'erddapWebInfDir': erddapWebInfDir, 'erddapContentDir': erddapContentDir},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

    dirout = '/home/jpa029/Data/ICOS2ERDDAP/58GS20190711_SOCAT_enhanced'

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
