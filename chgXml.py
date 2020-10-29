# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

__author__ = ["Julien Paul"]
__credits__ = ""
__license__ = "CC BY-SA 4.0"
__version__ = "0.0.0"
__maintainer__ = "BCDC"
__email__ = ['julien.paul@uib.no','']

# ----------------------------------------------
import lxml.etree as etree
from pathlib import Path


class CamelCase:
    """

    """
    def formatted(self, word, sep=' '):
        if isinstance(word, list):
            words = word
        else:
            words = word.split(sep=sep)

        s = "".join(word[0].upper() + word[1:].lower() for word in words)
        return s[0].lower() + s[1:]

    def datasetID(self, mydict):
        fname = mydict['name'].value[:mydict['name'].value.rfind(".")]
        return 'icos'+self.formatted(fname, sep='_')


cc = CamelCase()
# words = ["Hello", "World", "Python", "Programming"]
# print(cc.formatted(words))
# words='toto_25_tutu'
# print(cc.formatted(words, sep='_'))
# print(cc.formatted(words))


def renameDatasetId(i, newDatasetId):
    """
    search for and replace datasetId name.

    :param i: file to search/replace in
    :param newDatasetId: datasetId name to be put in
    :return: overwrite input file
    """
    import re

    content = i.read_text()
    regex = '(^<dataset .* datasetID=")(.*)(" .*>$)'
    i.write_text(re.sub(regex, r'\1' + newDatasetId + r'\3', content, flags=re.M))


def truc(dic, key, uri):
    dict1 = {}
    if key in dic:
        if uri in dic[key]:
            print('\nexplore dic[', key, '][', uri, '] \n')
            for k, v in dic[key][uri].items():
                if v.type != 'uri':
                    print('attr name:', k, ' value:', v.value)
                    dict1[k] = v.value
                else:
                    print('dic[', k, '][', v.value, '] \n')
                    dict2 = truc(dic, k, v.value)
                    # Merge contents of dict2 in dict1
                    dict1.update(dict2)
        else:
            print('\ncan not found dic[', key, '][', uri, '] \n')
    else:
        print('\ncan not found dic[', key, '] \n')

    return dict1


def changeAttr(i, o, m):
    """
    d: str
       input directory
    i: str
       input filename
    m: Attribute's instance
       global and variable attribute to be added
    o: str
        output filename

    """

    # keep CDATA as it is
    parser = etree.XMLParser(strip_cdata=False, encoding='ISO-8859-1')

    print('tree : ', i)

    tree = etree.parse(str(i), parser)
    root = tree.getroot()

    # prevent creation of self-closing tags
    for node in root.iter():
        if node.text is None:
            node.text = ''

    varval = 'var2'
    varnam = 'variable'
    gloval = 'title8'
    glonam = 'title'
    print('root :', root.tag, root.attrib)
    # node = context.find('dataset')
    print('\nmeta:=================================\n')

    # gloatt = {}
    # for k in m['dataObj'].keys():
    #     fname = m['dataObj'][k]['name'].value[:m['dataObj'][k]['name'].value.rfind(".")]
    #     newDatasetId = 'icos'+cc.formatted(fname, sep='_')
    #     gloatt[newDatasetId] = truc(m,'dataObj',k)
    #     #gloatt[k] = truc(m,'dataObj',k)
    gloatt = {}
    gloatt['title'] = 'toto'
    gloatt['summay'] = 'tutu'

    print('gloatt\n', gloatt)

    print('\n---------------')
    # for node in list(root):
    #    if node is not None:
    for node in root.findall('dataset'):
        print('node :', node.tag, node.attrib)
        if 'datasetID' in node.attrib:
            for attrNode in node.findall('addAttributes'):
                print('attrNode :', attrNode.tag, attrNode.attrib)
                for att in attrNode.iter('att'):
                    print('att name:', att.get('name'), 'val:', att.text)
                    # if att.get('name') in gloatt[dsID]:
                    if att.get('name') in gloatt:
                        attrNode.remove(att)
                # for k,v in gloatt[dsID].items():
                for k, v in gloatt.items():
                    subnode = etree.SubElement(attrNode, 'att', name=k)
                    subnode.text = str(v)
            dsID = node.attrib.get('datasetID')
            if dsID in gloatt:
                print('dsID:', dsID)
                for attrNode in node.findall('addAttributes'):
                    print('attrNode :', attrNode.tag, attrNode.attrib)
                    for att in attrNode.iter('att'):
                        print('att name:', att.get('name'), 'val:', att.text)
                        # if att.get('name') in gloatt[dsID]:
                        if att.get('name') in gloatt:
                            attrNode.remove(att)
                    # for k, v in gloatt[dsID].items():
                    for k, v in gloatt.items():
                        subnode = etree.SubElement(attrNode, 'att', name=k)
                        subnode.text = str(v)
        etree.indent(node)

        #    for varNode in node.iter('dataVariable'):
        #        for attrNode in varNode.findall('addAttributes'):
        #            print('attrNode :', attrNode.tag, attrNode.attrib)
        #            for att in attrNode.iter('att'):
        #                if att.get('name') == varnam:
        #                    attrNode.remove(att)
        #            ET.SubElement(attrNode, 'att', name=varnam, type='string').text = str(varval)

    # write xml output
    print('input ', str(i))
    print('output', str(o))
    tree.write(str(o), encoding="ISO-8859-1", xml_declaration=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # d = Path('/home/jpa029/Data/ICOS2ERDDAP/dataset/58GS20190711_SOCAT_enhanced')
    # i = d / 'dataset.58GS20190711_SOCAT_enhanced.xml'
    # renameDatasetId(i, 'toto')

    # d = '/home/jpa029/PycharmProjects/ICOS2ERDDAP/data'
    d = Path('/home/jpa029/Data/ICOS2ERDDAP/dataset')
    i = d / 'datasets.xml'
    o = d / 'datasets.new.xml'
    # i = d / 'testcdata.xml'
    # o = d / 'testcdata.new.xml'
    m = {}
    changeAttr(i, o, m)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
