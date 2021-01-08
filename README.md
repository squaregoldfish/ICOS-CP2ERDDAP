# ICOS-CP2ERDDAP

---
## To run 'module.__main__' from terminal
$ python3 -m icp2edd  
or  
$ python3 wrapper.py

### To get help/usage message
$ python3 -m icp2edd --help

# To run check of ICOS CP ontoloy
$ python3 -m icp2edd.checkOntology  
<!--
or  
$ python3 wrapper.py --check
-->

### To get help/usage message
$ python3 -m icp2edd.checkOntology --help

## Configuration file
put your own configuration file in
~/.config/icp2edd/config.yaml

```python
# This is the default config file for icp2edd
paths:
    # erddap: path of the main ERDDAP repository [tomcat]
    erddap: '/home/jpa029/Code/apache-tomcat-8.5.57'
    # dataset: path where store file from each dataset
    dataset:
        # path where store csv file from ICOS CP for each dataset
        csv: '/home/jpa029/Data/ICOS2ERDDAP'
        # path where store xml file from ICOS CP for each dataset
        xml: '/home/jpa029/Data/ICOS2ERDDAP/dataset'
    # log: path where store output log file
    log: '/home/jpa029/Data/ICOS2ERDDAP/log'

subm:
    # from: dataset submitted from [default: end date of last update]
    from: '2020-01-01T00:00:00.000Z'
    # until: dataset submitted until [default: today]
    until: '05-08-2020'
    # product: data 'type' selected
    product: 'icosOtcL2Product'
    # version: get only last version [default False]
    version: True

log:
    # filename: logger filename
    filename: 'debug.log'
    # below, apply only on standard output log
    # verbose: activate verbose mode [True|False]
    verbose: False
    # level: log level [NOTSET, DEBUG, INFO, WARN, ERROR, CRITICAL]
    level: 'INFO'
```

> **NOTE:** arguments overwrite value in configuration file.

## To run tests
see [here](tests/README.md)

## To install set up/update package library
see [PACKAGE.md](PACKAGE.md)
