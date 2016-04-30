import os
import json
import sys
import getopt

def execute_command(command):
    ret = os.system(command)
    return ret


def to_str(s):
    if bytes != str:
        if type(s) == bytes:
            return s.decode('utf-8')
    return s

def find_config():
    config_path = 'config.json'
    if os.path.exists(config_path):
        return config_path
    config_path = os.path.join(os.path.dirname(__file__), '../', 'config.json')
    if os.path.exists(config_path):
        return config_path
    return None


def get_config():
    shortopts = 'c:'
    longopts = ['help', 'code-base=', 'dots-path=', 'lizard-rep-file=','doxygen-config=', 'log-file=']

    try:
        config_path = find_config()
        optlist, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
        for key, value in optlist:
            if key == '-c':
                config_path = value

        if config_path:
            with open(config_path, 'rb') as f:
                try:
                    config = parse_json_in_str(f.read().decode('utf8'))
                except ValueError as e:
                    #TODO: log here
                    sys.exit(1)
        else:
            config = {}

        for key, value in optlist:
            if key == '--code-base':
                config['code_base'] = to_str(value)
            elif key == '--dots-path':
                config['dots_path'] = to_str(value)
            elif key == '--lizard-rep-file':
                config['complexity_file'] = to_str(value)
            elif key == '--doxygen-config':
                config['doxygen_config'] = to_str(value)
            elif key == '--log-file':
                config['log_file'] = to_str(value)


    except getopt.GetoptError as e:
        #print(e, file=sys.stderr)
        #TODO print help
        sys.exit(2)


    if not config:
        #logging.error('config not specified')
        #TODO print help
        sys.exit(2)
    
    return config


def _decode_list(data):
    rv = []
    for item in data:
        if hasattr(item, 'encode'):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.items():
        if hasattr(value, 'encode'):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv


def parse_json_in_str(data):
    # parse json and convert everything from unicode to str
    return json.loads(data, object_hook=_decode_dict)
