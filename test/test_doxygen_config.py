import unittest

from doxygen import config

class TestDoxygenConfig(unittest.TestCase):
    def test_config_update(self):
        self.assertTrue(True)

    def test_given_path_with_slash_when_convert_shall_with_backward_slash(self):
        path_value = '/home/name/workspace/pecker /home/name'
        formated = config.format_path_expr(path_value)
        self.assertEqual('\/home\/name\/workspace\/pecker \/home\/name', formated)
        
    def test_give_path_with_dot_convert_shall_with_backward_slash(self):
        path_value = '.'
        formated = config.format_path_expr(path_value)
        self.assertEqual('\.', formated)

        path_value = '..'
        formated = config.format_path_expr(path_value)
        self.assertEqual('\.\.', formated)

        path_value = '../name/'
        formated = config.format_path_expr(path_value)
        self.assertEqual('\.\.\/name\/', formated)
