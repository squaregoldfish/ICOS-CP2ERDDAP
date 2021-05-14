#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# icpOnto.py

# --- import -----------------------------------
# import from standard lib
import logging
import re
import os
from pprint import pformat
# import from other lib
# > pip
import ontospy
# > conda forge
import requests
from requests.exceptions import HTTPError
# import from my project
import icp2edd.setupcfg as setupcfg
import icp2edd.cpmeta
from icp2edd.icpObj import ICPObj
# import all class from submodules in cpmeta
from icp2edd.cpmeta import *

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)


# pour ecrire complement ontospy voir https://www.w3.org/TR/owl-ref/#equivalentClass-def
# https://stackoverflow.com/questions/21092246/sparql-query-subclass-or-equivalentto
# http://www.michelepasin.org/blog/2011/07/18/inspecting-an-ontology-with-rdflib/
# http://lambdamusic.github.io/Ontospy/


class Onto(object):
    """ """

    def __init__(self, uri=None):
        """ initialise generic ICOS CP object (ICPObj).

        :param uri: ontology's uri ('http://meta.icos-cp.eu/ontologies/cpmeta/')
        """
        # set up class/instance variables
        self._uri = uri
        self._type = None
        self._model = None
        #
        self.nsmap = {}
        self.isSubClassOf = {}
        self.isSubPropertyOf = {}
        self.classHasProperty = {}
        #

    def _get_namespaces(self):
        """ namespaces """
        pass

    def _get_classes(self):
        """ classes """
        pass

    def _get_properties(self):
        """ properties """
        pass

    def _get_class_properties(self):
        """ class's properties """
        pass

    def get_ontology(self):
        """ """
        # namespaces
        self._get_namespaces()
        # classes
        self._get_classes()
        # properties
        self._get_properties()
        # class's properties
        self._get_class_properties()

    def _refmt_to_icp2edd(self, dict_):
        """ """
        return self._refmt_to(self._to_icp2edd_fmt, dict_)

    def _refmt_to_ontospy(self, dict_):
        """ """
        return self._refmt_to(self._to_ontospy_fmt, dict_)

    def _refmt_to(self, func_, dict_):
        """
        given dictionary
        return reformatted dictionary by function func_
        """
        _ = {}
        for k, v in dict_.items():
            if k not in ['0', 'base', 'inherit']:
                kk = func_(k)
            else:
                kk = k

            if isinstance(v, dict):
                vv = self._refmt_to(func_, v)
            elif isinstance(v, list):
                vv = [func_(x) for x in v]
            else:
                vv = str(v)
            #
            _[kk] = vv
        return _

    def _from_ontospy_fmt(self, text_):
        """
        given ontospy format ('<Class *http://.../cpmeta/IcosStation*>')
        return url, namespace, and class or property name

        text_ = '<Class *http://.../cpmeta/IcosStation*>'
        return 'http://.../cpmeta/','cpmeta','IcosStation'

        TODO: add alternative if ns already used
        """
        if not isinstance(text_, str):
            text_ = str(text_)

        try:
            # found = re.search('AAA(.+?)ZZZ', text).group(1)
            found = re.search('\*(.+?)\*', text_).group(1)
        except AttributeError:
            # AAA, ZZZ not found in the original string
            raise AttributeError(f'can not extract url, namespace and class name.\n'
                                 f'do not recognize ontospy format -{text_}-')

        urlmap = {str(v): k for k, v in self.nsmap.items()}

        if found.startswith('http'):
            # get namespace
            if '#' in found:
                head_tail = found.split('#')
                _ = head_tail[0]
                url = str(_) + '#'
                # ns = str(Path(_).stem)
                try:
                    ns = urlmap[url]
                except KeyError:
                    ns = Path(_).stem
                attr = head_tail[1]

            else:
                head_tail = os.path.split(found)
                _ = head_tail[0]
                url = str(_) + '/'
                # s3_tail = os.path.split(head_tail[0])
                # ns = s3_tail[1]
                try:
                    ns = urlmap[url]
                except KeyError:
                    ns = Path(_).stem
                attr = head_tail[1]
        else:
            raise AttributeError(f'can not extract namespace and class name.\n'
                                 f'do not recognize url -{found}-')

        return url, ns, attr

    def _to_ontospy_fmt(self, text_):
        """
        given icp2edd format ('cpmeta:IcosStation')
        return ontospy format ('<Class *http://.../cpmeta/IcosStation*>')
        """
        if ':' in text_:
            head_tail = text_.split(':')
            ns = head_tail[0]
            attr = head_tail[1]
        else:
            raise AttributeError(f'can not reformat to ontospy format.\n'
                                 f'do not recognize icp2edd format -{text_}-')

        url = self.nsmap[ns]

        try:
            _ = eval(attr)
            return f'<Class *{url}{attr}*>'
        except NameError:
            return f'<Property *{url}{attr}*>'

    def _to_icp2edd_fmt(self, text_):
        """
        given ontospy format ('<Class *http://.../cpmeta/IcosStation*>')
        return icp2edd format ('cpmeta:IcosStation')
        """
        url, ns, attr = self._from_ontospy_fmt(text_)

        return f'{ns}:{attr}'

    def as_icp2edd_fmt(self):
        """
        change key and value format in class dictionaries
        from ontospy output format
            {<Class *http://.../cpmeta/IcosStation*>: [<Property *http://.../cpmeta/hasLabelingDate*>,...],..}
        to icp2edd format
            {cpmeta:IcosStation: [cpmeta:hasLabelingDate,...],..}
        """
        self.isSubClassOf = self._refmt_to_icp2edd(self.isSubClassOf)
        self.isSubPropertyOf = self._refmt_to_icp2edd(self.isSubPropertyOf)
        self.classHasProperty = self._refmt_to_icp2edd(self.classHasProperty)

    def as_ontospy_fmt(self):
        """
        change key and value format in class dictionaries
        from icp2edd format
            {cpmeta:IcosStation: [cpmeta:hasLabelingDate,...],..}
        to ontospy output format
            {<Class *http://.../cpmeta/IcosStation*>: [<Property *http://.../cpmeta/hasLabelingDate*>,...],..}
        """
        self.isSubClassOf = self._refmt_to_ontospy(self.isSubClassOf)
        self.isSubPropertyOf = self._refmt_to_ontospy(self.isSubPropertyOf)
        self.classHasProperty = self._refmt_to_ontospy(self.classHasProperty)

    @staticmethod
    def _print_indent(f, k, level=0):
        """ """
        if level == 0:
            f.write(f"\n")
        f.write(f"\n{'-' * 3 * level}:{k:10}")

    def _print_dic(self, f, dic, level=0):
        """ """
        for k, v in sorted(dic.items()):
            self._print_indent(f, k, level=level)
            # what about pformat instead
            if isinstance(v, dict):
                self._print_dic(f, v, level=level + 1)
            elif isinstance(v, list):
                for kk in sorted(v):
                    self._print_indent(f, kk, level=level + 1)
            else:
                self._print_indent(f, v, level=level + 1)

    def print_ontology(self):
        """ """
        output = Path(setupcfg.logPath) / f'cpmeta_{self._type}_namespace.txt'
        with open(output, 'w') as f:
            f.write(f"\n\nnamespaces:")
            f.write(f"\n{'-' * 40}")
            self._print_dic(f, self.nsmap)

        output = Path(setupcfg.logPath) / f'cpmeta_{self._type}_classes.txt'
        with open(output, 'w') as f:
            f.write(f"\n\nclasses:")
            f.write(f"\n{'-' * 40}")
            self._print_dic(f, self.isSubClassOf)

        output = Path(setupcfg.logPath) / f'cpmeta_{self._type}_properties.txt'
        with open(output, 'w') as f:
            f.write(f"\n\nproperties:")
            f.write(f"\n{'-' * 40}")
            self._print_dic(f, self.isSubPropertyOf)

        output = Path(setupcfg.logPath) / f'cpmeta_{self._type}_classprop.txt'
        with open(output, 'w') as f:
            f.write(f"\n\nclass properties:")
            f.write(f"\n{'-' * 40}")
            self._print_dic(f, self.classHasProperty)


def _onto2string(dict_):
    """
    given a dictionary with ontoClass instance element
    return a dictionary with string            element
    """
    _ = {}
    for k, v in dict_.items():
        if isinstance(v, list):
            vs = [str(x) for x in v]
        else:
            vs = str(v)
        _[str(k)] = vs
    return _


class IcpOnto(Onto):
    """ """
    def __init__(self, uri="http://meta.icos-cp.eu/ontologies/cpmeta/"):
        """
        initialise class with ontology from url,
        ontospy package is used to sort class and properties
        """
        super().__init__(uri)
        # set up class/instance variables
        self._type = 'icp'
        self._model = ontospy.Ontospy(self._uri)

    def _get_namespaces(self):
        """ namespaces

        namespace A has uri B
        nsmap[A] = B

        return namespace dictionary
        """
        for k, v in self._model.namespaces:
            self.nsmap[k] = str(v)

        # rename 'local' namespace
        try:
            self.nsmap['cpmeta'] = self.nsmap.pop('')
        except KeyError:
            pass

        # add extra namespaces
        urlmap = {str(v): k for k, v in self.nsmap.items()}
        for _ in self._model.all_classes:
            url, ns, attr = self._from_ontospy_fmt(_)
            if url not in urlmap:
                self.nsmap[ns] = url

        for _ in self._model.all_properties:
            url, ns, attr = self._from_ontospy_fmt(_)
            if url not in urlmap:
                self.nsmap[ns] = url

    def _get_classes(self):
        """ classes

        class B is sub class of class A
         isSubClassOf[A] = B

        return class dictionary
        """
        _ = self._model.ontologyClassTree()
        self.isSubClassOf = _onto2string(_)
        # model.all_classes
        # model.toplayer_classes
        # model.ontologyClassTree()
        # model.printClassTree()

        # add extra base class
        self._add_base_classes()

    def _add_base_classes(self):
        """ """
        _ = []
        for klass in self.isSubClassOf['0']:
            if 'cpmeta' not in klass:
                _ = [*_, *self.isSubClassOf[klass]]
            else:
                _ = [*_, klass]

        key = self._to_ontospy_fmt('cpmeta:ICPObj')
        self.isSubClassOf[key] = _

    def _get_properties(self):
        """ properties

        property B is sub property of property A
         isSubPropertyOf[A] = B

        return properties dictionary
        """
        # TODO find a way to handle subproperties
        _ = self._model.ontologyPropTree()
        self.isSubPropertyOf = _onto2string(_)
        # model.all_properties
        # model.toplayer_properties
        # model.ontologyPropTree()
        # model.printPropertyTree()

        # add extra base property
        self._add_base_properties()

    def _add_base_properties(self):
        """ """
        _ = []
        for klass in self.isSubPropertyOf['0']:
            if klass in self.isSubPropertyOf:
                _ = [*_, klass, *self.isSubPropertyOf[klass]]
            else:
                _ = [*_, klass]

        key = self._to_ontospy_fmt('cpmeta:ICPObj')
        self.isSubPropertyOf[key] = _

    def _get_class_properties(self):
        """ class's properties

        property B is a property of class A
         classHasProperty[A] = B

        return class properties dictionary
        """
        for c in self._model.all_classes:
            # c = model.get_class(uri=url+'DataObject')
            cs = str(c)
            _ = {'base':[], 'inherit':[]}
            # c.domain_of          # property own by the class
            # c.domain_of_inferred # also properties inherit
            for x in c.domain_of_inferred:
                xx = _onto2string(x)
                for k, v in xx.items():
                    # k : class from property inherited
                    # _[k] = v
                    if k == cs:
                        _['base'] = [*_['base'], *v]
                    else:
                        _['inherit'] = [*_['inherit'], *v]
            self.classHasProperty[cs] = _

    def download_rdf(self, filename='cpmeta.rdf'):
        """ download rdf ontology file """
        pid = ''
        cookies = dict(CpLicenseAcceptedFor=pid)
        fileout = setupcfg.logPath / filename

        # Use 'with' to ensure the session context is closed after use.
        with requests.Session() as s:
            try:
                r = s.get(str(self._uri), cookies=cookies, stream=True)
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
                _logger.info(f'download file {self._uri} on {fileout}')
                with open(fileout, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)


class EddOnto(Onto):
    """ """
    def __init__(self):
        """
        initialise class with ontology from icp2edd scripts
        """
        super().__init__()
        # set up class/instance variables
        self._type = 'edd'

    def _get_namespaces(self):
        """ namespaces
        """
        _ = ICPObj()
        for k, v in _._ns.items():
            # if k is None:
            #     k = 'cpmeta'
            self.nsmap[k] = v

    def _get_classes(self):
        """ classes

        get subclass from icp2edd.cpmeta

         class B is sub class of class A
          isSubClassOf[A] = B
        """
        package = icp2edd.cpmeta

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
                        parent = attr.__bases__[0].__name__
                        if parent == 'object':
                            continue
                        parent = f'cpmeta:{parent}'
                        if parent not in self.isSubClassOf.keys():
                            self.isSubClassOf[parent] = []

                        # keep only uniq value : list(set(mylist))
                        self.isSubClassOf[parent] = list({*self.isSubClassOf[parent], f'cpmeta:{attr.__name__}'})

    def _get_properties(self):
        """ properties

        get all properties from icp2edd.cpmeta

        property B is sub property of property A
         isSubPropertyOf[A] = B
        """
        for k, v in self.isSubClassOf.items():
            self._add_properties(k)
            for kk in v:
                self._add_properties(kk)

    def _add_properties(self, k):
        """
        # TODO find a way to define sub properties
        """
        # main property
        key = 'cpmeta:ICPObj'
        if k not in self.isSubPropertyOf.keys():
            klass = eval(k.split(':')[1])
            _ = klass()
            for p in _.attr.keys():
                try:
                    if p in self.isSubPropertyOf[key]:
                        _logger.info(f'property {p} already in class {key}')
                    else:
                        self.isSubPropertyOf[key] += [p]
                except KeyError:
                    # method not from cpmeta
                    self.isSubPropertyOf[key] = [p]

    def _get_class_properties(self):
        """ class's properties

        get properties of each class from icp2edd.cpmeta

        property B is a property of class A
         classHasProperty[A] = B
        """
        for k, v in self.isSubClassOf.items():
            self._add_class_properties(k)
            for kk in v:
                self._add_class_properties(kk)

    def _add_class_properties(self, k_):
        """
        """
        # init
        _ = {'base': [], 'inherit': []}
        #
        klass = eval(k_.split(':')[1])
        inst = klass()

        _['base'] = [*_['base'], *inst._attr]
        _['inherit'] = [*_['inherit'], *inst._inherit]
        # if k_ in self.isSubClassOf:
        #     for kk in self.isSubClassOf[k_]:
        #         _['inherit'] = [*_['inherit'], *self._get_list_properties(kk)]

        self.classHasProperty[k_] = _

    @staticmethod
    def _get_list_properties(k_):
        """
        """
        klass = eval(k_.split(':')[1])
        _ = klass()
        return [str(x) for x in _.attr.keys()]

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
