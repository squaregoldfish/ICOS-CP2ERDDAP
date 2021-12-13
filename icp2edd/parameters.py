#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# parameters.py

# ----------------------------------------------
# import from standard lib
import logging
from pprint import pformat
from urllib.parse import urlparse

# import from other lib
import yaml

# import from my project
import icp2edd.setupcfg as setupcfg

# --- module's variable ------------------------
# load logger
_logger = logging.getLogger(__name__)

# TODO create class for parameters


# ----------------------------------------------
def _is_url(url_):
    """
    check if argument is an url

    :param url_: string of url to check

    :return: boolean
    """
    try:
        result = urlparse(url_)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def _get_list(list_=None):
    """get list from yaml file element"""
    if not isinstance(list_, list):
        if list_ is None:
            _ = []
        else:
            _ = [list_]
    else:
        _ = list_

    return _


def _check_param_attributes_keep(dict_=None):
    """ """
    # default 'keep' dictionary
    _ = {"icoscp": _get_list(), "erddap": _get_list()}

    if "icoscp" in dict_:
        _["icoscp"] = _get_list(dict_["icoscp"])
    if "erddap" in dict_:
        _["erddap"] = _get_list(dict_["erddap"])

    return _


def _check_param_attributes_convert(dict_=None):
    """ """
    if dict_ is None:
        return {}
    else:
        if not isinstance(dict_, dict):
            _logger.exception(
                f"Invalid convert type -{dict_}-. convert must be a dictionary."
                f"Check {setupcfg.extraParam}."
            )
            raise
        else:
            return dict_


def _check_param_attributes_sep(str_=None):
    """ """
    # default separator
    default_sep = "_"

    if str_ is None:
        return default_sep
    else:
        if not isinstance(str_, str):
            _logger.exception(
                f"Invalid separator type -{str_}-. Separator must be a single character."
                f"Check {setupcfg.extraParam}."
            )
            raise
        elif len(str_) != 1:
            _logger.exception(
                f"Invalid separator length -{str_}-. Separator must be a single character."
                f"Check {setupcfg.extraParam}."
            )
            raise
        else:
            return str_


def _check_param_attributes(dict_):
    """ """
    # default empty dictionary
    _ = {}

    # check separator
    if "sep" in dict_:
        _["sep"] = _check_param_attributes_sep(dict_["sep"])
    else:
        _["sep"] = _check_param_attributes_sep()

    # check convert
    if "convert" in dict_:
        _["convert"] = _check_param_attributes_convert(dict_["convert"])
    else:
        _["convert"] = _check_param_attributes_convert({})

    # check keep
    if "keep" in dict_:
        _["keep"] = _check_param_attributes_keep(dict_["keep"])
    else:
        _["keep"] = _check_param_attributes_keep({})

    return _


def _check_param(dict_):
    """
    check dictionary elements and reformat if need be

    :return: dictionary reformat
    """
    # default empty dictionary
    _ = {}

    if "attributes" in dict_:
        _["attributes"] = _check_param_attributes(dict_["attributes"])
    else:
        _["attributes"] = _check_param_attributes({})

    return _


def show(param_):
    """ """
    print(f"parameters:\n {pformat(param_)}")


def main():
    """ """
    try:
        # read parameters configuration file yaml
        with open(setupcfg.extraParam, "r") as stream:
            try:
                param = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        # check parameters file
        return _check_param(param)

    except Exception:
        _logger.exception(
            f"Something goes wrong when loading extra parameters file -{setupcfg.extraParam}-."
        )
        raise  # Throw exception again so calling code knows it happened


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Something goes wrong!!!")
        raise  # Throw exception again so calling code knows it happened

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
