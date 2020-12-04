#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# setupcfg.py

# ----------------------------------------------
# import from standard lib
from pathlib import Path
import logging
import logging.config
import yaml
import pkgutil
import sys
import os
import warnings
import argparse
# import from other lib
import confuse  # Initialize config with your app
# import from my project
import icp2edd

# --- module's variable ------------------------
global erddapPath, erddapWebInfDir, erddapContentDir, datasetXmlPath, datasetCsvPath, logPath


def _chk_path_log(cfg_):
    """ check path to log files, and set up global variable

    path where log files will be stored
    """
    global logPath

    logPath = Path(cfg_['paths']['log'].get('string'))
    if not logPath.is_dir():
        logPath.mkdir(parents=True, exist_ok=True)
        warnings.warn('log path {} did not exist before.\n Check config file(s) {} and/or {}'.
                      format(logPath, cfg_.user_config_path(), cfg_.default_config_path))

    logging.debug(f'logPath: {logPath}')


def _chk_path_edd(cfg_):
    """ check path to ERDDAP, and set up global variables

    path where ERDDAP has been previously installed, as well as
    path where xml files will be stored
    """
    global erddapPath, erddapWebInfDir, erddapContentDir, datasetXmlPath

    erddapPath = Path(cfg_['paths']['erddap'].get('string'))
    if not erddapPath.is_dir():
        raise FileNotFoundError('can not find ERDDAP path {}.\n'
                                'Check config file(s) {} and/or {}'.format(erddapPath,
                                                                           cfg_.user_config_path(),
                                                                           cfg_.default_config_path))
    logging.debug(f'erddapPath: {erddapPath}')

    erddapWebInfDir = erddapPath / 'webapps' / 'erddap' / 'WEB-INF'
    if not erddapWebInfDir.is_dir():
        raise FileNotFoundError('can not find ERDDAP sub-directory {} \n'
                                'check ERDDAP installation. '.format(erddapWebInfDir))
    logging.debug(f'erddapWebInfDir: {erddapWebInfDir}')

    erddapContentDir = erddapPath / 'content' / 'erddap'
    if not erddapContentDir.is_dir():
        raise FileNotFoundError('can not find ERDDAP sub-directory {} \n'
                                'check ERDDAP installation'.format(erddapContentDir))
    logging.debug(f'erddapContentDir: {erddapContentDir}')

    datasetXmlPath = Path(cfg_['paths']['dataset']['xml'].as_filename())
    if not datasetXmlPath.is_dir():
        raise FileNotFoundError('can not find path where store dataset xml file {}.\n'
                                'Check config file(s) {} and/or {}'.format(datasetXmlPath,
                                                                           cfg_.user_config_path(),
                                                                           cfg_.default_config_path))
    logging.debug(f'datasetXmlPath: {datasetXmlPath}')


def _chk_path_csv(cfg_):
    """ check path to csv files, and set up global variable

    path where csv files will be stored
    """
    global datasetCsvPath

    datasetCsvPath = Path(cfg_['paths']['dataset']['csv'].as_filename())
    if not datasetCsvPath.is_dir():
        raise FileNotFoundError('Can not find path where store dataset csv file {}.\n'
                                'Check config file(s) {} and/or {}'.format(datasetCsvPath,
                                                                           cfg_.user_config_path(),
                                                                           cfg_.default_config_path))
    logging.debug(f'datasetCsvPath: {datasetCsvPath}')


def _chk_path(cfg_=None):
    """

    """
    if cfg_ is None:
        cfg_ = confuse.Configuration('icp2edd', modname=icp2edd.__pkg_cfg__)  # Get a value from your YAML file
        _ = Path(cfg_._package_path)
        cfg_.default_config_path = _ / confuse.DEFAULT_FILENAME

    try:
        _chk_path_edd(cfg_)
        _chk_path_csv(cfg_)
        _chk_path_log(cfg_)
    except Exception:
        logging.exception('Something goes wrong when checking paths')
        raise  # Throw exception again so calling code knows it happened


def _find_package_path(name):
    # function from https://github.com/beetbox/confuse/blob/master/confuse/util.py
    """Returns the path to the package containing the named module or
    None if the path could not be identified (e.g., if
    ``name == "__main__"``).
    """
    # Based on get_root_path from Flask by Armin Ronacher.
    loader = pkgutil.get_loader(name)
    if loader is None or name == '__main__':
        return None

    if hasattr(loader, 'get_filename'):
        filepath = loader.get_filename(name)
    else:
        # Fall back to importing the specified module.
        __import__(name)
        filepath = sys.modules[name].__file__

    return os.path.dirname(os.path.abspath(filepath))


def _setup_cfg():
    """set up from configuration file(s)

    read parameters from
    ~/.config/icp2edd/config.yaml
    otherwise from
    /path/to/package/cfg/config_default.yaml
    """
    # set up configuration file
    try:
        # Read configuration file
        config = confuse.LazyConfig('icp2edd',
                                    modname=icp2edd.__pkg_cfg__)  # Get a value from your YAML file

        # TODO check use of templates,
        #  cf examples in https://github.com/beetbox/confuse/tree/c244db70c6c2e92b001ce02951cf60e1c8793f75

        # set up default configuration file path
        pkg_path = Path(config._package_path)
        config.default_config_path = pkg_path / confuse.DEFAULT_FILENAME

        return config

    except Exception:
        logging.exception("Something goes wrong when loading config file.")
        raise  # Throw exception again so calling code knows it happened


def _parse():
    """set up parameter from command line arguments

    """
    # define parser
    parser = argparse.ArgumentParser(
        prog="icp2edd",
        description="blabla"
    )

    # positional arguments
    # parser.add_argument("name", type=str, help="file name")
    # optional arguments
    parser.add_argument("-q", "--quiet",
                        action="store_false",
                        help="do not print status messages to stdout",
                        dest='log.quiet'
                        )
    parser.add_argument("--log_level",
                        type=str,
                        choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help="logger level",
                        dest='log.level'
                        )
    parser.add_argument("--log_path",
                        type=str,
                        help="logger path, where log will be stored",
                        dest='paths.log'
                        )

    # parse arguments
    args = parser.parse_args()

    # TODO check and reformat args

    return args


def _setup_logger(config_):
    """set up logger

    set up logging parameters from command line arguments
    otherwise from configuration file(s)
    otherwise from logging configuration file: /path/to/package/cfg/logging.yaml

    > Level and When it’s used
    > ------------------------
    > DEBUG:
    > Detailed information, typically of interest only when diagnosing problems.
    >
    > INFO:
    > Confirmation that things are working as expected.
    >
    > WARNING:
    > An indication that something unexpected happened, or indicative of some problem in the near
    > future (e.g. ‘disk space low’). The software is still working as expected.
    >
    > ERROR:
    > Due to a more serious problem, the software has not been able to perform some function.
    >
    > CRITICAL:
    > A serious error, indicating that the program itself may be unable to continue running.
    """
    cfg_path = Path(_find_package_path(icp2edd.__pkg_cfg__))
    if not cfg_path.is_dir():
        logging.exception('Can not find configuration path')
        raise FileNotFoundError

    _logcfg = cfg_path / 'logging.yaml'
    try:
        with open(_logcfg, 'rt') as file:
            cfg_log = yaml.safe_load(file.read())

            # overwrite default with config or parser value
            if config_['log']['level'] is not None:
                cfg_log['handlers']['console']['level'] = str(config_['log']['level'])

            # if quiet activated, no output on console
            if config_['log']['quiet'] is not None:
                if config_['log']['quiet']:
                    # disable log on console
                    cfg_log['handlers'].pop('console')
                    cfg_log['root']['handlers'].remove('console')

            if config_['paths']['log'] is not None:
                log_path = Path(str(config_['paths']['log']))
            else:
                # read path to output log file
                log_path = Path(cfg_log['handlers']['file']['filename']).parent

            if not log_path.is_dir():
                log_path.mkdir(parents=True, exist_ok=True)
                warnings.warn('log path {} did not exist before.\n Check config file(s) {} and/or {}'.
                              format(log_path, config_.user_config_path(), config_.default_config_path))

            filename = cfg_log['handlers']['file']['filename']
            cfg_log['handlers']['file']['filename'] = str(log_path / filename)

            logging.config.dictConfig(cfg_log)

    except Exception:
        logging.exception('Error loading configuration file. Using default configs')
        raise  # Throw exception again so calling code knows it happened

    # add header to log file
    logging.info(f'-------------------')
    logging.info(f'package: {icp2edd.__name__}')
    logging.info(f'version: {icp2edd.__version__}')
    logging.info(f'-------------------')


def _default_logger():
    """creates default logger, before any setting up

    this default logger should only be used in case of any exception raised during setting up
    """
    logging.basicConfig(
        level=logging.INFO,
        style='{',
        format="{asctime} | {levelname:8} | {name} | {message}"
    )


def main():
    """set up icp2edd

    set up config file(s)
    set up logger
    """

    # init default
    _default_logger()

    # read configuration file(s)
    config = _setup_cfg()
    # read command line arguments
    args = _parse()

    # overwrite configuration file parameter with parser arguments
    config.set_args(args)

    # read logging configuration file
    _setup_logger(config)

    # check path from configuration file(s)
    _chk_path(config)


if __name__ == '__main__':
    main()

    _logger = logging.getLogger(__name__)
    _logger.debug('This message should go to the log file')
    _logger.info('So should this')
    _logger.warning('And this, too')
    _logger.error('\tAnd non-ASCII stuff, too, like Øresund and Malmö\n')
    _logger.critical('this is critical')
    # _logger.exception('raise en exception')
