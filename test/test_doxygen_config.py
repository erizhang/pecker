import unittest

from doxygen import config

class TestDoxygen(unittest.TestCase):
    def config_update(self):
        self.assertTrue(True)

    def given_path_with_slash_when_convert_shall_with_backward_slash(self):
        path_value = '/home/name/workspace/pecker /home/name'
        formated = config.format_path_expr(path_value)
        self.assertEqual('\/home\/name\/workspace\/pecker \/home\/name', formated)





        
