#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# checkOntology.py

# --- import -----------------------------------
# import from standard lib
import logging
from pprint import pformat
import os
# import os as stdlib_os
# import from other lib
# > conda forge
import requests
from requests.exceptions import HTTPError
import lxml.etree as etree
from rdflib.graph import Graph
# import from my project
import icp2edd.setupcfg as setupcfg
from icp2edd.icpObj import ICPObj
# import all class from submodules in cpmeta
from icp2edd.cpmeta import *

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

global hasProperty, isSubClassOf, fromNamespace, nsmap


# ----------------------------------------------
def _show(what_='all', domain_='icp'):
    """print on standard output

    :param what_: ['all', 'nsmap', 'class', 'prop'], default = 'all'
    :param domain_: ['icp', 'edd']
    """
    output = Path(setupcfg.logPath) / f'show_{domain_}.txt'
    with open(output, 'w') as f:
        if what_ in ['all', 'nsmap']:
            f.write(f'\n----- nsmap[{domain_}]')
            f.write('\t'+pformat(nsmap[domain_]))
            if domain_ == 'icp':
                f.write(f'\n----- nsmap[icp*]')
                f.write('\t' + pformat(nsmap['icp*']))
        if what_ in ['all', 'prop']:
            if hasProperty[domain_]:
                f.write(f"\n----- {sum(map(len, hasProperty[domain_].values()))} properties[{domain_}]")
                f.write('\t' + pformat(hasProperty[domain_]))
        if what_ in ['all', 'class']:
            if isSubClassOf[domain_]:
                f.write(f"\n----- {sum(len(v) != 0 for x, v in isSubClassOf[domain_].items())} sub-class[{domain_}]")
                f.write('\t' + pformat(isSubClassOf[domain_]))
                # hasSubClass = reverseDic(isSubClassOf[domain_])
                # print(f'----- {sum(map(len, hasSubClass.values()))} has-sub-class')
                # print('\t' + pformat(hasSubClass))
            if domain_ in fromNamespace and fromNamespace[domain_]:
                f.write(f"\n----- object-namespace[{domain_}]")
                f.write('\t' + pformat(fromNamespace[domain_]))
        f.write(f'****')


def _get_property(class_, domain_, inherit_=False):
    """recursively get property of class

    :param class_:
    :param domain_:  ['icp', 'edd']
    :param inherit_: [True, False]
    """
    _ = []
    if class_ in hasProperty[domain_].keys():
        for p in hasProperty[domain_][class_]:
            for v, k in nsmap[domain_].items():
                if k in p:
                    p = p.replace(k, v + ':')
            if inherit_:
                p = '\t' + p
            _.append(p)

    if domain_ == 'icp' and class_ in isSubClassOf[domain_].keys():
        superClass = isSubClassOf[domain_][class_]
        if superClass:
            _ += _get_property(superClass[0], domain_, True)

    # remove duplicate value inherit or not
    for x in list(_):
        _.remove(x)
        if x not in _ and x.strip() not in _:
            _.append(x)

    return _


def _write(domain_):
    """write in a file namespace, class and their properties from domain_

    the output files help to compare differences between ICOS CP end icp2edd tree

    :param domain_: ['icp', 'edd']
    """
    if domain_ not in ['icp', 'edd']:
        _logger.error(f'Can not write cpmeta tree. Invalid domain -{domain_}-')

    output = Path(setupcfg.logPath) / f'cpmeta_{domain_}.txt'
    with open(output, 'w') as f:
        f.write(f"namespace:")
        for k, v in sorted(nsmap[domain_].items()):
            f.write(f'\n\t {k:10}:{v}')

        # force to use 'icp' dictionary 'order'
        for k in isSubClassOf['icp'].keys():
            if k in isSubClassOf[domain_].keys():
                v = isSubClassOf[domain_][k]
                f.write(f"\n\n<class '{k}'>\n-----")
                if v:
                    f.write(f"\n\t subClassOf: (<class '{v[0]}'>)")
                else:
                    f.write(f"\n\t subClassOf: (None)")

                f.write(f"\n\t properties:")
                for p in sorted(_get_property(k, domain_), key=lambda x: x.strip()):
                    f.write(f'\n\t\t{p}')

        if domain_ != 'icp':
            # add class not in 'icp' dictionary
            for k in isSubClassOf[domain_].keys():
                if k not in isSubClassOf['icp'].keys():
                    v = isSubClassOf[domain_][k]
                    f.write(f"\n\n<class '{k}'>\n-----")
                    if v:
                        f.write(f"\n\t subClassOf: (<class '{v[0]}'>)")
                    else:
                        f.write(f"\n\t subClassOf: (None)")

                    f.write(f"\n\t properties:")
                    for p in sorted(_get_property(k, domain_)):
                        f.write(f'\n\t\t{p}')


def _check_class_property(class_):
    """check property of the class class_ between ICOS CP and icp2edd

    :param class_:
    """
    _status = 0
    # initialise counter
    _miss = 0
    # compare ICOS CP properties of class 'class_' to the ones of icp2edd
    for p in hasProperty['icp'][class_]:
        if p not in hasProperty['edd'][class_]:
            _status = 1
            _miss += 1
            _logger.error(f'missing property -{p}- in icp2edd for class -{class_}-')
    if _miss:
        _logger.warning(f'{_miss} properties are missing in icp2edd CP for class -{class_}-')

    # re-initialise counter
    _miss = 0
    # compare icp2edd properties of class 'class_' to the ones of ICOS CP
    for p in hasProperty['edd'][class_]:
        if p not in hasProperty['icp'][class_]:
            _miss += 1
            _logger.debug(f'unset property -{p}- in ICOS CP for class -{class_}-')
    if _miss:
        _logger.debug(f'{_miss} properties are unset in ICOS CP for class -{class_}-')

    return _status


def _check_property():
    """check property of each class, between ICOS CP and icp2edd
    """
    _status = 0
    # initialise counter
    _miss = 0
    # compare ICOS CP properties to the ones of icp2edd
    for k, v in hasProperty['icp'].items():
        if k in hasProperty['edd'].keys():
            _status += _check_class_property(k)
        else:
            _miss += 1
            if 'cpmeta' not in k:
                _logger.warning(f' missing class -{k}- in icp2edd')
            else:
                _status = 1
                _logger.error(f' missing class -{k}- in icp2edd')

    if _miss:
        _logger.warning(f'{_miss} ICOS CP properties are missing in icp2edd')

    # re-initialise counter
    _miss = 0
    # compare icp2edd properties to the ones of ICOS CP
    for k, v in hasProperty['edd'].items():
        if k not in hasProperty['icp'].keys():
            _miss += 1
            _logger.warning(f'missing class -{k}- in ICOS CP')

    if _miss:
        _logger.warning(f'{_miss} icp2edd class are missing in ICOS CP')

    return _status


def _check_subclass():
    """compare inheritance of each class, between ICOS CP and icp2edd
    """
    _status = 0
    # initialise counter
    _miss = 0
    # compare ICOS CP class to the ones of icp2edd
    for k, v in isSubClassOf['icp'].items():
        if k in isSubClassOf['edd'].keys():
            if isinstance(v, list) and v:
                icp = v[0]
            else:
                icp = 'None'
            edd = isSubClassOf['edd'][k][0]

            if icp != edd:
                if 'cpmeta' not in icp:
                    _logger.warning(f"subclass of -{k}- differ between ICOS CP -{icp}- and icp2edd -{edd}-")
                else:
                    _status = 1
                    _logger.error(f'subclass of -{k}- differ between ICOS CP -{icp}- and icp2edd -{edd}-')
        else:
            _miss += 1
            if 'cpmeta' not in k:
                _logger.warning(f'missing ICOS CP class -{k}- in icp2edd')
            else:
                _status = 1
                _logger.error(f'missing ICOS CP class -{k}- in icp2edd')

    if _miss:
        _logger.warning(f'{_miss} ICOS CP class are missing in icp2edd')

    # re-initialise counter
    _miss = 0
    # compare icp2edd class to the ones of ICOS CP
    for k, v in isSubClassOf['edd'].items():
        if k not in isSubClassOf['icp'].keys():
            _miss += 1
            _logger.warning(f'missing icp2edd class -{k}- in ICOS CP')

    if _miss:
        _logger.warning(f'{_miss} icp2edd class are missing in ICOS CP')

    return _status


def _check_namespace():
    """ check namespace between ICOS CP and icp2edd
    """
    _status = 0
    # compare ICOS CP namespace to the ones of icp2edd
    for k, v in nsmap['icp'].items():
        if k in nsmap['edd'].keys():
            icp = v
            edd = nsmap['edd'][k]
            if icp != edd:
                _status = 1
                _logger.error(f'value of -{k}- differ between ICOS CP -{icp}- and icp2edd -{edd}-')
        else:
            _status = 1
            _logger.error(f'missing ICOS CP namespace -{k}- in icp2edd')

    # compare icp2edd namespace to the ones of ICOS CP
    for k, v in nsmap['edd'].items():
        if k not in nsmap['icp'].keys():
            _logger.warning(f'missing icp2edd namespace -{k}- in ICOS CP')

    return _status


def extract_namespace(list_):
    """extract namespace from each element of the list list_

    - 'extra' namespace found are store in 'nsmap['icp*']' dictionary
    - all class and property associated to one namespace 'ns' are stored in fromNamespace['icp'][ns] list
    """
    global nsmap, fromNamespace
    for k in list_:
        if k.startswith('http'):
            # get namespace
            if '#' in k:
                _ = k.split('#')[0]
                ns = str(Path(_).stem)
                url = str(_)+'#'

            else:
                head_tail = os.path.split(k)
                url = head_tail[0]+'/'
                s3_tail = os.path.split(head_tail[0])
                ns = s3_tail[1]

            if ns not in nsmap['icp'] and ns not in nsmap['icp*']:
                _logger.warning(f'missing namespace -{ns}: {url}- in ICOS CP')
                nsmap['icp*'][ns] = url

            o = k.replace(url, '')
            if ns in fromNamespace['icp'].keys():
                fromNamespace['icp'][ns] += [o]
            else:
                fromNamespace['icp'][ns] = [o]


def get_namespace(dict_):
    """ get all url namespace (listed or not) used in ICOS CP

    - 'extra' namespace found are store in 'nsmap['icp*']' dictionary
    - all class and property associated to one namespace 'ns' are stored in fromNamespace['icp'][ns] list
    """
    global nsmap, fromNamespace
    if 'icp*' not in nsmap:
        nsmap['icp*'] = {}
    if 'icp' not in fromNamespace:
        fromNamespace['icp'] = {}

    extract_namespace(dict_.keys())
    for k, v in dict_.items():
        extract_namespace(v)


def _replace_url_by_namespace(dict_):
    """replace, for each key and element value of dictionary dict_, the url by their namespace

    return dictionary
    """
    _ = _replace_from_nsmap(dict_, nsmap['icp'])
    if 'icp*' in nsmap.keys():
        _ = _replace_from_nsmap(_, nsmap['icp*'])
    if 'edd' in nsmap.keys():
        _ = _replace_from_nsmap(_, nsmap['edd'])

    return _


def _replace_from_nsmap(dict_, nsmap_):
    """replace, for each key and element value of dictionary dict_, the url by the namespace listed in nsmap_

    return dictionary
    """
    _ = {}
    for k, v in dict_.items():
        for ns, url in nsmap_.items():
            if url in k:
                k = k.replace(url, ns+':')
            for e in v:
                if url in e:
                    ee = e.replace(url, ns+':')
                    v = [x if x != e else ee for x in v]
        _[k] = v

    return _


def _clean_subclass(dict1_, list_):
    """remove element of list_ from dictionary dict_

    return dictionary
    """
    for k, v in dict1_.items():
        for elt in list_:
            if elt in v:
                v.remove(elt)
                dict1_[k] = v

    return dict1_


def _add_subproperty(dict1_, dict2_):
    """append subproperty to main property

    dict1_ = {
        c1 = [p1, p2]
    }
    dict2_ = {
        p1 = [p3, p4]
        p2 = [p5]
    }

    dict1_ = {
        c1 = [p1, p3, p4, p2, p5]
    }

    return dictionary
    """
    for k in list(dict1_.keys()):
        for elt in dict1_[k]:
            if elt in dict2_.keys():
                dict1_[k] += [x for x in dict2_[elt] if x not in dict1_[k]]

    return dict1_


def _spread_property(dict1_, dict2_):
    """dispatch property into all union subClass

     dict1_ = {
        c1: [p1]
        c2: [p2]
     }
     dict2_ = {
        c1: [c3, c2]
     }

     dict1_ = {
        c3: [p1]
        c2: [p2, p1]
     }

     return dictionary
     """
    for k, v in dict2_.items():
        if k in dict1_.keys():
            prop = dict1_.pop(k)
            for elt in v:
                if elt in dict1_.keys():
                    dict1_[elt] += prop
                else:
                    dict1_[elt] = prop

    return dict1_


def _rename(dict1_, dict2_):
    """rename the element 'elt' of the list value of dict1_[k], by the value of dict2_['elt]

    dict1_ = {
        a: [b, c, d]
    }
    dict2_ = {
        b: e
    }

    dict1_: {
        a: [e, c, d]
    }

    return dictionary
    """
    for k in list(dict1_.keys()):
        for elt in dict1_[k]:
            if elt in dict2_.keys():
                dict1_[k] = [dict2_[elt] if (x == elt) else x for x in dict1_[k]]

    return dict1_


def _unify(dict1_, dict2_):
    """replace dict1_'s element 'elt' by the value of dict2_['elt']

    dict1_ = {
        a: [b, c]
    }
    dict2_ = {
        b: [d, e]
        c: [f]
    }

    dict1_ = {
        a = [d, e, f]
    }

    return dictionary
    """
    for k, v in dict1_.items():
        for elt in v:
            if elt in dict2_.keys():
                dict1_[k] += dict2_[elt]

    return dict1_


def _agglomerate(dict1_):
    """replace elements of list which are link to another key,
    by the value of this key

    input:
    dict1_ = {
            a: [b, c]
            b: [d]
            c: [nil]
            e: [toto]
        }

    output:
    dict1_ = {
        a: [d]
        e: [toto]
        }

    return dictionary
    """
    for k in list(dict1_.keys()):
        # check if key still in dictionary
        if k in dict1_.keys():
            for elt in dict1_[k]:
                # check if element of the list is a key in dictionary
                if elt in dict1_.keys():
                    # replace link to another key, by value
                    _ = dict1_.pop(elt)
                    if not any("nil" in s for s in _):
                        dict1_[k] += _

    return dict1_


def _parse_rdf(ds_):
    """parse xml file of ICOS CP ontology to extract class and their properties
    """
    global hasProperty, isSubClassOf, nsmap

    if not isinstance(ds_, Path):
        ds_ = Path(ds_)

    # keep CDATA as it is
    parser = etree.XMLParser(strip_cdata=False, encoding='ISO-8859-1')

    tree = etree.parse(str(ds_), parser)
    root = tree.getroot()

    # namespace
    nsmap['icp'] = root.nsmap
    try:
        nsmap['icp']['cpmeta'] = nsmap['icp'].pop(None)
    except KeyError:
        pass

    # print('Description')
    hasProperty['icp'] = {}
    isSubClassOf['icp'] = {}

    hasSubProperty = {}
    isSubPropertyOf = {}
    isUnionOf = {}
    first = {}
    rest = {}
    Restriction = []
    for node in root.findall("rdf:Description", namespaces=nsmap['icp']):
        fname = node.attrib.values()[0]
        domain = None
        subPropertyOf = None
        subClassOf = []
        classOf = None
        unionOf = []
        # intersectionOf = []
        oneOf = []
        isProp = False
        isClass = False
        for snode in node.findall("rdf:type", namespaces=nsmap['icp']):
            # print(f'\t {snode.tag} {snode.attrib.values()}')
            if any("Restriction" in s for s in snode.attrib.values()):
                Restriction.append(fname)
            if any("Property" in s for s in snode.attrib.values()):
                isProp = True
            elif any("Class" in s for s in snode.attrib.values()):
                isClass = True
                classOf = snode.attrib.values()[0]
            elif any("NamedIndividual" in s for s in snode.attrib.values()):
                isClass = False
            elif any("http://meta.icos-cp.eu/ontologies/cpmeta/" in s for s in snode.attrib.values()):
                subClassOf.append(snode.attrib.values()[0])

        # for snode in node.findall("owl:intersectionOf", namespaces=nsmap['icp']):
        #     intersectionOf.append(snode.attrib.values()[0])
        for snode in node.findall("owl:oneOf", namespaces=nsmap['icp']):
            oneOf.append(snode.attrib.values()[0])

        for snode in node.findall("rdf:first", namespaces=nsmap['icp']):
            if fname in first.keys():
                raise KeyError(f'key -{fname}- already exist')
            else:
                # print(f'snode: {snode.attrib.values()}')
                # print(f'first: {first}')
                # print(f'fname: {fname}')
                # print(f'snode: {snode.attrib}')
                if snode.attrib.values():
                    first[fname] = snode.attrib.values()[0]

        for snode in node.findall("rdf:rest", namespaces=nsmap['icp']):
            if fname in rest.keys():
                raise KeyError(f'key -{fname}- already exist')
            else:
                rest[fname] = [snode.attrib.values()[0]]

        for snode in node.findall("rdfs:domain", namespaces=nsmap['icp']):
            domain = snode.attrib.values()[0]
        for snode in node.findall("rdfs:subPropertyOf", namespaces=nsmap['icp']):
            subPropertyOf = snode.attrib.values()[0]
        for snode in node.findall("rdfs:subClassOf", namespaces=nsmap['icp']):
            subClassOf.append(snode.attrib.values()[0])
        for snode in node.findall("owl:unionOf", namespaces=nsmap['icp']):
            unionOf.append(snode.attrib.values()[0])

        if isClass:
            if subClassOf:
                if fname in isSubClassOf['icp'].keys():
                    isSubClassOf['icp'][fname] += subClassOf
                else:
                    isSubClassOf['icp'][fname] = subClassOf

            if unionOf:
                if fname in isUnionOf.keys():
                    isUnionOf[fname] += unionOf
                else:
                    isUnionOf[fname] = unionOf

            # if intersectionOf or oneOf:
            #     # ignore those class
            #     pass
            # elif not subClassOf and not unionOf:
            if not subClassOf and not unionOf:
                isSubClassOf['icp'][fname] = [classOf]

        if isProp:
            if domain is not None:
                if domain in hasProperty['icp'].keys():
                    hasProperty['icp'][domain] += [fname]
                else:
                    hasProperty['icp'][domain] = [fname]

            if subPropertyOf is not None:
                if fname in isSubPropertyOf.keys():
                    isSubPropertyOf[fname] += [subPropertyOf]
                else:
                    isSubPropertyOf[fname] = [subPropertyOf]

                if subPropertyOf in hasSubProperty.keys():
                    hasSubProperty[subPropertyOf] += [fname]
                else:
                    hasSubProperty[subPropertyOf] = [fname]

    rest = _agglomerate(rest)
    union = _unify(isUnionOf, rest)
    isUnionOf = _rename(union, first)

    hasProperty['icp'] = _spread_property(hasProperty['icp'], isUnionOf)
    hasProperty['icp'] = _add_subproperty(hasProperty['icp'], hasSubProperty)

    # get extra Namespace
    get_namespace(hasProperty['icp'])
    get_namespace(isSubClassOf['icp'])
    # TODO check Restriction stuff
    # remove useless Restriction subClass
    isSubClassOf['icp'] = _clean_subclass(isSubClassOf['icp'], Restriction)

    hasProperty['icp'] = _replace_url_by_namespace(hasProperty['icp'])
    isSubClassOf['icp'] = _replace_url_by_namespace(isSubClassOf['icp'])


def _convert_rdf(file):
    """convert ICOS CP ontology file from ttl to xml format
    """
    g = Graph()
    g.parse(str(file), format="turtle")

    g.serialize(str(file), format="xml")


def _download_rdf(o):
    """ download rdf ontology from ICOS CP
    """

    url = "http://meta.icos-cp.eu/ontologies/cpmeta/"
    pid = ''
    cookies = dict(CpLicenseAcceptedFor=pid)
    fileout = o

    # Use 'with' to ensure the session context is closed after use.
    with requests.Session() as s:
        try:
            r = s.get(str(url), cookies=cookies, stream=True)
            # If the response was successful, no Exception will be raised
            r.raise_for_status()
        except HTTPError:  # as http_err:
            # https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
            # raise HTTPError(f'HTTP error occurred: {http_err}')  # Python 3.6
            _logger.exception(f'HTTP error occurred:')
            raise  #
        except Exception:  # as err:
            # raise Exception(f'Other error occurred: {err}')  # Python 3.6
            _logger.exception(f'Other error occurred:')
            raise  #
        else:
            # Success!
            _logger.info(f'download file {url} on {fileout}')
            with open(fileout, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)


def _get_icp_oontology():
    """parse ICOS CP ontology to set up cpmeta 'rdf'
    """
    # TODO see tempfile
    tmp = Path('cpmeta.rdf')
    # download cpmeta ontology
    _download_rdf(tmp)
    # convert from turtle to xml
    _convert_rdf(tmp)
    # TODO use rdflib instead of parsing xml file
    _parse_rdf(tmp)
    #
    try:
        tmp.unlink()
    except OSError as e:
        print("Error: %s : %s" % (tmp, e.strerror))


def _add_namespace(dict_, ns_):
    """add namespace ns_ to all element of dict_ to help comparing with ICOS CP tree

    if element already use namespace, nothing add
    """
    _ = {}
    for k, v in dict_.items():
        if ':' not in k:
            k = ns_ + ':' + k

        for e in v:
            # check no namespace used
            if ':' not in e:
                ee = ns_ + ':' + e
                v = [x if x != e else ee for x in v]
        _[k] = v

    return _


def _get_edd_ontology():
    """parse icp2edd class to set up cpmeta 'rdf'
    """
    global hasProperty, isSubClassOf, nsmap

    # get namespace
    nsmap['edd'] = {}
    _ = ICPObj()
    for k, v in _._ns.items():
        if k is None:
            k = 'cpmeta'
        nsmap['edd'][k] = v

    # get subclass from icp2edd.cpmeta
    import icp2edd.cpmeta
    package = icp2edd.cpmeta

    isSubClassOf['edd'] = {}
    for importer, modname, ispkg in iter_modules(package.__path__):
        # print("Found submodule %s (is a package: %s)" % (modname, ispkg))
        # import the module and iterate through its attributes
        modul = import_module(f"{package.__name__}.{modname}")
        for attr_name in dir(modul):
            attr = getattr(modul, attr_name)
            if isclass(attr):
                # select only class with method '_query', see ICPObj
                if hasattr(attr, '_query'):
                    # print(f'attribute_name:{attr.__bases__[0].__name__} {attr}')
                    isSubClassOf['edd'][attr.__name__] = [attr.__bases__[0].__name__]

    # get properties of each class from icp2edd.cpmeta
    hasProperty['edd'] = {}
    for k in isSubClassOf['edd'].keys():
        clss = eval(k)
        _ = clss()
        for p in _._attr.keys():
            try:
                if p in hasProperty['edd'][k]:
                    _logger.error(f'property {p} already in {k}')
                else:
                    hasProperty['edd'][k] += [p]
            except KeyError:
                hasProperty['edd'][k] = [p]

    hasProperty['edd'] = _add_namespace(hasProperty['edd'], 'cpmeta')
    isSubClassOf['edd'] = _add_namespace(isSubClassOf['edd'], 'cpmeta')


def main(logfile_='check_ontology.log'):
    """check ICOS CP ontology versus the one use in icp2edd

    :param logfile_: log filename, force to change the default log filename when using checkOntology.py
    """
    print(f"Running {__file__} \n...")

    # set up logger, paths, ...
    setupcfg.main(logfile_)
    _logger = logging.getLogger(__name__)

    global hasProperty, isSubClassOf, nsmap, fromNamespace
    nsmap = {}
    isSubClassOf = {}
    hasProperty = {}
    fromNamespace = {}

    _logger.info(f"parse icp2edd class to set up cpmeta 'rdf'\n")
    _get_edd_ontology()
    _logger.info(f"parse ICOS CP ontology to set up cpmeta 'rdf'\n")
    _get_icp_oontology()

    # print tables
    _show(domain_='edd')
    _show(domain_='icp')

    _logger.info(f"check namespace:\n")
    status = _check_namespace()
    _logger.info(f"check subclass:\n")
    status += _check_subclass()
    _logger.info(f"check property:\n")
    status += _check_property()

    # True == 1
    # False == 0
    # status = 1
    if status:
        _write('icp')
        _write('edd')
        _logger.critical(f"Change detected in ICOS CP, "
                         f"check diff between 'cpmeta_icp.txt' and 'cpmeta_edd.txt' ")

    print(f"See output log for more details: {setupcfg.log_filename} ")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        main()
    except Exception:
        logging.exception('Something goes wrong!!!')
        raise  # Throw exception again so calling code knows it happened

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
