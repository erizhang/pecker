
import os
import sys


def execute(command):
    print command
#    os.system(command)

def format_path_expr(value):
    if '/' in value:
        val_list = value.split('/')
        value = "\/".join(val_list)
    if '.' in value:
        value_list = value.split('.')
        value = "\.".join(value_list)

    return value


def inject(items, config):
    for key, value in items.iteritems():
        formated = format_path_expr(value)
        command = "sed -i 's/^\(" + key + "\s*=\s*\).*$/\1" + formated + "/'" + config['doxygen_config']
        execute(command)

