import os
import json
import sys
import getopt


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
    longopts = ['help', 'source-base=', 'dots-path=', 'lizard-rep-file=', 'log-file=']

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
            if key == '--source-base':
                config['code_base'] = to_str(value)
            elif key == '--dots-path':
                config['dots-path'] = to_str(value)
            elif key == '--lizard-rep-file':
                config['complexity-file'] = to_str(value)
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
