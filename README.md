# ICOS-CP2ERDDAP

---
## To run 'package' from terminal
$ python3 -m icp2edd  

### To get help/usage message
$ python3 -m icp2edd --help

# To run check of ICOS CP ontoloy
$ python3 -m icp2edd.checkOntology  

### To get help/usage message
$ python3 -m icp2edd.checkOntology --help

## To run icp2edd and checkOntology inside a wrapper
$ python3 wrapper.py

## Configuration file
This file contains configuration parameters
> **NOTE:** arguments overwrite value in configuration file.

Put your own configuration file in `~/.config/icp2edd/config.yaml`

```python
# This is the default config file for icp2edd

paths:
    # erddap: path of the main ERDDAP repository [tomcat]
    erddap: '/home/jpa029/Code/apache-tomcat-8.5.57'
    # webinf: path to the 'WEB-INF' repository
    webinf: '/home/jpa029/Code/apache-tomcat-8.5.57/webapps/ROOT/WEB-INF'
    # dataset: path where store file from each dataset
    dataset:
        # path where store csv file from ICOS CP for each dataset
        csv: '/home/jpa029/Data/ICOS2ERDDAP/dataset/csv'
        # path where store xml file from ICOS CP for each dataset
        xml: '/home/jpa029/Data/ICOS2ERDDAP/dataset/xml'
    # log: path where store output log file
    log: '/home/jpa029/Data/ICOS2ERDDAP/log'

log:
    # filename: logger filename [default 'debug.log']
    filename:
    # Below, apply only on standard output log
    # verbose: activate verbose mode [True|False]
    verbose: False
    # level: log level [DEBUG, INFO, WARN, ERROR, CRITICAL]
    level: 'INFO'

authorised:
    # product: list of authorised product
    product: ['icosOtcL1Product_v2', 'icosOtcL2Product']

extra:
    # parameters: extra parameters configuration file for bcedd
    parameters: 'parameters.yaml'

product:
    # subm: submitted dates
    subm:
        # from: dataset submitted from [default: end date of last update]
        #   ex: '2020-01-01T00:00:00.000Z'
        from:
        # until: dataset submitted until [default: today]
        #   ex: '05-08-2020'
        until:
    # type: data 'type' selected
    type: 'icosOtcL2Product'
    # last: get only last version [default False]
    last: True
```

### Parameters files
This file contains parameters to run

```python
# This is the parameters file for icp2edd

# attributes' configuration
attributes:
    # sep: separator between object and attribute, use in origin attribute name
    #   ex: 'type' + sep + 'units' > 'type_units'
    sep: '_'
    # convert: attribute name(s) to convert
    #   origin_name: target_name
    convert:
        type_units: 'units'
    #
    keep:
        # keep attribute(s) from erddap (overwrite attribute(s) from icoscp)
        icoscp:
        # keep attribute(s) from icoscp (overwrite attribute(s) from erddap)
        erddap:
            - 'units'
```

## To run tests
see [HERE](tests/README.md)

## To install set up/update package library
see [PACKAGE.md](PACKAGE.md)

## Use cron to schedule job
$ crontab -e  
```bash
# crontab -e
SHELL=/bin/bash
MAILTO=jpa029@uib.no

# Example of job definition:
# m h dom mon dow   command

# * * * * *  command to execute
# ┬ ┬ ┬ ┬ ┬
# │ │ │ │ │
# │ │ │ │ │
# │ │ │ │ └───── day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# │ │ │ └────────── month (1 - 12)
# │ │ └─────────────── day of month (1 - 31)
# │ └──────────────────── hour (0 - 23)
# └───────────────────────── min (0 - 59)

# For details see man 4 crontabs

# daily update (at 00:30) of ICOS-CP data portal synchronisation with ICOS-CP ERDDAP server
30 00 * * * python3 -m icp2edd

# weekly check (every monday at 06:00) of ICOS-CP data portal ontology
00 06 * * 1 python3 -m icp2edd.checkOntology
```