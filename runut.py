#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

import unittest
from test import test_doxygen_config

if __name__ == '__main__':
    SeTestSuite = unittest.defaultTestLoader.discover(start_dir='./')
    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(SeTestSuite))
