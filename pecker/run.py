#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from pecker import shell, walkinput

def main():
    config = shell.get_config()
    print config

    # step 1. wakl the code base, list out the header and source files path
    print walkinput.headers(config)
    print walkinput.sources(config)

    # step 2. custimize the doxygen configuration

    # step 3. generate the dots files of doxygen

    # step 4. generate the lizard report

    # step 5. generate the statistics raw json file

if __name__ == '__main__':
    main()
