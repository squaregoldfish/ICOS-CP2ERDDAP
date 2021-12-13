#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# checkOntology.py

# --- import -----------------------------------
# import from standard lib
import logging
from pprint import pformat

# import from other lib
# > conda forge
# import from my project
import icp2edd.setupcfg as setupcfg
import icp2edd.timing
from icp2edd.icpOnto import EddOnto, IcpOnto

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

# pour ecrire complement ontospy voir https://www.w3.org/TR/owl-ref/#equivalentClass-def
# https://stackoverflow.com/questions/21092246/sparql-query-subclass-or-equivalentto
# http://www.michelepasin.org/blog/2011/07/18/inspecting-an-ontology-with-rdflib/
# http://lambdamusic.github.io/Ontospy/


def _check_namespace(icp_, edd_):
    """check namespace between ICOS CP and icp2edd"""
    _status = 0
    # compare ICOS CP namespace to the ones of icp2edd
    for k, v in icp_.nsmap.items():
        if k in edd_.nsmap.keys():
            icp_url = v
            edd_url = edd_.nsmap[k]
            if icp_url != edd_url:
                _status = 1
                _logger.error(
                    f"value of -{k}- differ between ICOS CP -{icp_url}- and icp2edd -{edd_url}-"
                )
        else:
            help_msg = f"'{k}': '{v}'"
            _status = 1
            _logger.error(f"missing ICOS CP namespace -{help_msg}- in icp2edd.")

    # compare icp2edd namespace to the ones of ICOS CP
    for k, v in edd_.nsmap.items():
        # if present, value already check above
        if k not in icp_.nsmap.keys():
            _logger.warning(f"missing icp2edd namespace -{k}- in ICOS CP")

    return _status


def _check_class(icp_, edd_):
    """compare inheritance of each class, between ICOS CP and icp2edd"""
    _status = 0
    # initialise counter
    _miss = 0

    # rename
    key = edd_._to_ontospy_fmt("ICPObj")
    edd_.isSubClassOf["0"] = edd_.isSubClassOf.pop(key)
    # compare ICOS CP class to the ones of icp2edd
    for k, v in icp_.isSubClassOf.items():
        if k in edd_.isSubClassOf.keys():
            edd_class_list = edd_.isSubClassOf[k]
            for icp_class in sorted(v):
                if icp_class not in edd_class_list:
                    _status = 1
                    _logger.error(
                        f"subclass of -{k}- differ. "
                        f"\tICOS CP -{icp_class}- not found in icp2edd"
                    )
        else:
            _miss += 1
            _status = 1
            _logger.error(f"missing ICOS CP class -{k}- in icp2edd")

    if _miss:
        _logger.warning(f"{_miss} ICOS CP class are missing in icp2edd")

    # re-initialise counter
    _miss = 0
    # compare icp2edd class to the ones of ICOS CP
    for k, v in edd_.isSubClassOf.items():
        # if present, value already check above
        if k not in icp_.isSubClassOf.keys():
            _miss += 1
            _logger.warning(f"missing icp2edd class -{k}- in ICOS CP")

    if _miss:
        _logger.warning(f"{_miss} icp2edd class are missing in ICOS CP")

    return _status


def _check_property(icp_, edd_):
    """check property, between ICOS CP and icp2edd"""
    _status = 0
    # initialise counter
    _miss = 0
    # compare ICOS CP properties to the ones of icp2edd
    for k, v in icp_.isSubPropertyOf.items():
        if k in edd_.isSubPropertyOf.keys():
            edd_prop_list = edd_.isSubPropertyOf[k]
            for icp_prop in sorted(v):
                if icp_prop not in edd_prop_list:
                    if icp_prop in icp_.propFromClass:
                        help_msg = f"property -{icp_prop}- come from class -{icp_.propFromClass[icp_prop]}-"
                    else:
                        url, ns, attr = icp_._from_ontospy_fmt(icp_prop)
                        queryString = f"describe <{url}{attr}>"
                        help_msg = (
                            f"\nbase class of property -{icp_prop}- is unknown.\n "
                            f"To get a clue, try to run {queryString} "
                            f"in Carbon Portal SPARQL Endpoint "
                            f"-https://meta.icos-cp.eu/sparqlclient/?type=TSV%20or%20Turtle-\n"
                        )

                    _status = 1
                    _logger.error(
                        f"property of -{k}- differ. "
                        f"\tICOS CP -{icp_prop}- not found in icp2edd."
                        f"\t{help_msg}\n"
                    )
        else:
            _miss += 1
            _logger.error(f"missing ICOS CP property -{k}- in icp2edd")

    if _miss:
        _logger.warning(f"{_miss} ICOS CP property are missing in icp2edd")

    # re-initialise counter
    _miss = 0
    # compare icp2edd properties to the ones of ICOS CP
    for k, v in edd_.isSubPropertyOf.items():
        # if present, value already check above
        if k not in icp_.isSubPropertyOf.keys():
            _miss += 1
            _logger.warning(f"missing icp2edd property -{k}- in ICOS CP")

    if _miss:
        _logger.warning(f"{_miss} icp2edd property are missing in ICOS CP")

    return _status


def _check_class_property(icp_, edd_):
    """check property of each class, between ICOS CP and icp2edd"""
    _status = 0
    # initialise counter
    _miss = 0
    # compare ICOS CP properties of each class to the ones of icp2edd
    for k, v in icp_.classHasProperty.items():
        if k in edd_.classHasProperty.keys():
            # Note: work only on key '0', as it is supposed to regroup all properties in use
            edd_prop_list = edd_.classHasProperty[k]["0"]
            for icp_prop in sorted(v["0"]):
                if icp_prop not in edd_prop_list:
                    _status = 1
                    _logger.error(
                        f"property of class -{k}- differ.\n"
                        f"\tICOS CP -{icp_prop}- not found in icp2edd"
                    )
        else:
            _miss += 1
            _status = 1
            _logger.error(f"missing ICOS CP class -{k}- in icp2edd")

    if _miss:
        _logger.warning(f"{_miss} ICOS CP class are missing in icp2edd classes")

    # re-initialise counter
    _miss = 0
    # compare icp2edd properties to the ones of ICOS CP
    for k, v in edd_.classHasProperty.items():
        # if present, value already check above
        if k not in icp_.classHasProperty.keys():
            _miss += 1
            _logger.warning(f"missing icp2edd class -{k}- in ICOS CP")

    if _miss:
        _logger.warning(f"{_miss} icp2edd class are missing in ICOS CP")

    return _status


def main():
    """check ICOS CP ontology versus the one use in icp2edd

    :param logfile_: log filename, force to change the default log filename when using checkOntology.py
    """
    print(f"Running {__file__} \n...")
    # choose output format
    # - ontospy: <Class *http://.../cpmeta/IcosStation*>
    # - icp2edd: cpmeta:IcosStation
    use_ontospy_fmt = True

    # set up logger, paths, ...
    setupcfg.main(checkOnto_=True)
    _logger = logging.getLogger(__name__)

    _logger.info(f"parse icp2edd class to set up cpmeta 'rdf'\n")
    edd = EddOnto()
    edd.get_ontology()
    if use_ontospy_fmt:
        edd.as_ontospy_fmt()

    _logger.info(f"parse ICOS CP ontology to set up cpmeta 'rdf'\n")
    icp = IcpOnto()
    icp.get_ontology()
    if not use_ontospy_fmt:
        icp.as_icp2edd_fmt()

    _logger.info(f"check namespace:\n")
    status = _check_namespace(icp, edd)
    _logger.info(f"check class:\n")
    status += _check_class(icp, edd)
    _logger.info(f"check property:\n")
    status += _check_property(icp, edd)
    _logger.info(f"check class's property:\n")
    status += _check_class_property(icp, edd)

    if setupcfg.downloadOnto:
        print(
            f"download rdf ontology file from ICOS CP in {setupcfg.logPath}/cpmeta.rdf"
        )
        icp.download_rdf()

    if setupcfg.writeOnto:
        print(
            f"write namespace, class, and property ontology tree for ICOS CP "
            f"and icp2edd scripts in {setupcfg.logPath}"
        )
        icp.print_ontology()
        edd.print_ontology()

    # store ending submitted date of current update
    setupcfg.add_last_subm()

    # True == 1
    # False == 0
    if status:
        _logger.critical(
            f"Change detected in ICOS CP, "
            f"Check output log for more details: {setupcfg.log_filename}"
        )
        print(f"Change detected in ICOS CP")
    else:
        print(f"No change detected in ICOS CP")


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Something goes wrong!!!")
        raise  # Throw exception again so calling code knows it happened

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
