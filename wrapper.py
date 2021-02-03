#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# wrapper.py

# ----------------------------------------------
# import from standard lib
import time
# import from other lib
import schedule
# import from my project
import icp2edd
from icp2edd.__main__ import main
from icp2edd.checkOntology import main as check

if __name__ == '__main__':
    """ """
    print('module: {}'.format(icp2edd.__name__))
    print('package: {}'.format(icp2edd.__package__))
    print('version: {}'.format(icp2edd.__version__))

    # run icp2edd
    schedule.every().day.at("00:30:00").do(main)
    # check ontology ...
    # schedule.every().wednesday.at("01:30:00").do(check)

    while True:
        schedule.run_pending()
        time.sleep(1)

