
import os
import os.path

from src import shell

source_dirs = []

def isContainHeaderFile(files):
    for file in files:
        if file.endswith(".h") or file.endswith(".hpp"):
            return True
    return False

def isContainSrcFile(files):
    for file in files:
        if file.endswith(".cpp") or file.endswith(".cxx"):
            return True
    return False

def walking(dir, is_header):
    for root, dirs, files in os.walk(dir):
        if is_header and isContainHeaderFile(files):
            dirs_list.append(root)
        if !is_header and isContainSrcFile(files):
            dirs_list.append(root)
        

def list_header_files(config):
    walking(config['code_base'], True)
    return " ".join(dirs_list)

def list_cpp_files(config):
    walking(config['code_base'], False)
    return " ".join(dirs_list)
