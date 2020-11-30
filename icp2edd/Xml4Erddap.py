#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xml4Erddap.py

# --- import -----------------------------------
# import from standard lib
from pathlib import Path
import re
import os
import subprocess
import logging
import warnings
# from importlib import resources
# import from other lib
# > conda forge
import lxml.etree as etree
# import from my project
import icp2edd.case as case
import icp2edd.setup as setup

# load logger
_logger = logging.getLogger(__name__)


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

        if not isinstance(eddType, str):
            raise TypeError(f'Invalid type value, eddType -{eddType}- must be string')

        # TODO check for csv file in sub directories
        if len(list(dirout_.glob('*.csv'))) <= 0:
            raise FileNotFoundError(f'Can not find any csv file in {dirout_}')

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
            raise NameError(f'EDDType -{self._eddType}- unknown by ERDDAP')

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
            raise NameError(f'EDDType -{self._eddType}- unknown by ERDDAP')

    def generate(self):
        """ generate dataset.xml file using ERDDAP tools -GenerateDatasetsXml.sh-
        """
        if len(self._cmd) != self._checkArgs():
            raise ValueError('Invalid arguments number -{}-, expected -{}-'.format(len(self._cmd), self._checkArgs()))

        # creates sub directory
        datasetSubDir = setup.datasetXmlPath / self._stem
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

        exe = Path.joinpath(setup.erddapWebInfDir, exe)
        # Check file exists
        if not exe.is_file():
            raise FileNotFoundError(f"Can not find ERDDAP tools {exe}")

        # Check for execution access
        if not os.access(exe, os.X_OK):
            # change permission mode
            warnings.warn(f'change exectuable -{exe}- permission mode')
            exe.chmod(0o744)
            # raise PermissionError("")

        # run process 'GenerateDatasetsXml.sh' from directory 'erddapWebInfDir' with arguments 'self._cmd'
        # => creates file: ds
        _logger.info(f'creates dataset: {self.ds}')
        _logger.debug(f'from directory {setup.erddapWebInfDir}, run process {self._cmd}')
        process = subprocess.run(self._cmd,
                                 cwd=setup.erddapWebInfDir,
                                 stdout=subprocess.PIPE,
                                 timeout=60,
                                 universal_newlines=True)
        process.check_returncode()

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
        _logger.debug('renames datasetID to {}'.format(newDatasetId))

    def _checkTag(self, ds_, tagline_):
        """
        check if both taglines:
            <!-- Begin GenerateDatasetsXml #XXX someDate -->
            <!-- End GenerateDatasetsXml #XXX someDate -->
        are presented in ds file.

        XXX is the name of the dataset (without suffix)
        """
        if not isinstance(ds_, Path):
            raise TypeError(f'Invalid type value, ds_ -{ds_}- must be Pathlib object')
        if not isinstance(tagline_, str):
            raise TypeError(f'Invalid type value, tagline_ -{tagline_}- must be string')

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
    dsxmlout = setup.datasetXmlPath / 'datasets.xml'
    _logger.debug(f'concatenate in {dsxmlout}')
    mod_path = Path(__file__).parent
    with dsxmlout.open("w") as fp:
        # add header
        header = mod_path / 'dataset' / 'header.xml'
        # TODO see how to use resources
        # header = resources.path('dataset', 'header.xml')
        _logger.debug('\t{}'.format(header))
        fp.write(header.read_text())
        # add single dataset
        for ff in setup.datasetXmlPath.glob('**/dataset.*.xml'):
            _logger.debug('\t{}'.format(ff))
            fp.write(ff.read_text())
        # add footer
        footer = mod_path / 'dataset' / 'footer.xml'
        _logger.debug('\t{}'.format(footer))
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

    if not isinstance(gloatt, dict):
        raise TypeError(f'Invalid type value, gloatt -{gloatt}- must be dictionary')

    if out is not None and not isinstance(out, str):
        raise TypeError(f'Invalid type value, out -{out}- must be string')

    if not ds.is_file():
        raise FileExistsError(f'File {ds} does not exist.')
    else:
        _logger.info('tree : ', ds)

    # keep CDATA as it is
    parser = etree.XMLParser(strip_cdata=False, encoding='ISO-8859-1')

    tree = etree.parse(str(ds), parser)
    root = tree.getroot()

    # prevent creation of self-closing tags
    for node in root.iter():
        if node.text is None:
            node.text = ''

    # for node in list(root):
    #    if node is not None:
    # TODO need to test with variable attributes to add at every variables whatever datasedID
    for node in root.findall('dataset'):
        _logger.debug(f'node: tag -{node.tag}- attribute -{node.attrib}-')
        if 'datasetID' in node.attrib:

            dsID = node.attrib.get('datasetID')
            if dsID in gloatt:
                _logger.debug(f'dsID: {dsID}')
                for attrNode in node.findall('addAttributes'):
                    _logger.debug(f'attrNode: tag -{attrNode.tag}- attribute -{attrNode.attrib}-')
                    for att in attrNode.iter('att'):
                        _logger.debug(f"att name: {att.get('name')} val: {att.text}")
                        if att.get('name') in gloatt[dsID]:
                            # TODO figure out how to keep information not to be changed
                            attrNode.remove(att)
                    for k, v in gloatt[dsID].items():
                        # for k, v in gloatt.items():
                        subnode = etree.SubElement(attrNode, 'att', name=k)
                        subnode.text = str(v)

        for varNode in node.iter('dataVariable'):
            _logger.debug(f'varNode : tag {varNode.tag} attribue {varNode.attrib}')
            srcname = None
            for attrNode in varNode.findall('sourceName'):
                srcname = attrNode.text
                _logger.debug(f'srcname {srcname}')

            # for attrNode in varNode.findall('destinationName'):
            #     dstname = attrnode.text

            if srcname in gloatt:
                for attrNode in varNode.findall('addAttributes'):
                    _logger.debug(f'attrNode : tag {attrNode.tag} attribute {attrNode.attrib}')
                    for att in attrNode.iter('att'):
                        _logger.debug(f"att name: {att.get('name')} val: {att.text}")
                        if att.get('name') in gloatt[srcname]:
                            attrNode.remove(att)
                    for k, v in gloatt[srcname].items():
                        subnode = etree.SubElement(attrNode, 'att', name=k)
                        subnode.text = str(v)

            etree.indent(node)

    # write xml output
    if out is not None:
        dsout = out
    else:
        dsout = ds

    tree.write(str(dsout), encoding='ISO-8859-1', xml_declaration=True)


def replaceXmlBy(dsxmlout):
    """ overwrite erddap datasets.xml with the new one
    :param dsxmlout:
    """
    # remove erddap datasets.xml and create hard link to the new one
    dsxml = setup.erddapContentDir / 'datasets.xml'
    if dsxml.is_file():  # and not dsxml.is_symlink():
        dsxml.unlink()

    _logger.info(f'create hard link to: {dsxmlout}')
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
    doctest.testmod(extraglobs={'datasetXmlPath': setup.datasetXmlPath, 'erddapPath': setup.erddapPath,
                                'erddapWebInfDir': setup.erddapWebInfDir, 'erddapContentDir': setup.erddapContentDir},
                    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

    dirout = '/home/jpa029/Data/ICOS2ERDDAP/58GS20190711_SOCAT_enhanced'

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
