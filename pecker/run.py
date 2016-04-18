#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from pecker import shell, walkinput
from doxygen import config

def main():
    app_config = shell.get_config()
    print config

    # step 1. wakl the code base, list out the header and source files path
    src = walkinput.headers(app_config)
    inc = walkinput.sources(app_config)

    # step 2. custimize the doxygen configuration
    doxygen_config = {'EXTRACT_ALL'    : 'YES',
                      'INPUT'          : src,
                      'INLINE_SOURCES' : 'YES',
                      'GENERATE_LATEX' : 'NO',
                      'INCLUDE_PATH'   : inc,
                      'HAVE_DOT'       : 'YES',
                      'CALL_GRAPH'     : 'YES',
                      'CALLER_GRAPH'   : 'YES',
                      'DOTFILE_DIRS'   : 'dotfile',
                      'DOT_CLEANUP'    : 'ON'}

    config.inject(doxygen_config, app_config)

    # step 3. generate the dots files of doxygen

    # step 4. generate the lizard report

    # step 5. generate the statistics raw json file

if __name__ == '__main__':
    main()
