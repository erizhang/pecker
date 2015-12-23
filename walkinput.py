
import os
import os.path

source_dirs = []

def isContainSourceFile(files):
    for file in files:
        if file.endswith(".c") or file.endswith(".cpp"):
            return True
    return False

def sources(dir):
    for root, dirs, files in os.walk(dir):
        if isContainSourceFile(files):
            source_dirs.append(root)

if __name__ == '__main__':
    sources('/home/erizhang/workspace/nginx/src/')
    print " ".join(source_dirs)
