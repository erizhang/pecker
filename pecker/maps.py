#!/usr/bin/python

from os import listdir
from os.path import isfile, join
import re
import json

import argparse

path = "../.tmp/dot" #specify the path where the dot files locate

def get_hash(f):
    words = f.split("_");
    return words[-2];

def get_source_name(f):
    words = ['_' if x =='' else x for x in f.split('_')];

    extention = words[-3];
    s = ['.' if x == '8' else x for x in list(extention)];
    extention = "".join(s);
    words[-3] = extention;

    del words[-2:];

    return "".join(words);

# { name: free_inode;
#   hash: aaa83f2a89dae6d03dfe15deae29f383a;
#   file: tty_ioctrl.c;
# }
def get_function_name(lines):
    func_name = lines[0].split(" ");
    return func_name[1][1:-2];
    
def get_function_direct_calls(lines):
    targets_nodes = [];
    target_node = {};
    target = "";
    for line in lines:
        words = line.lstrip().split(" ");
        
        if words[0] == "Node1" and words[1] == "->":
            target = words[2];
        if words[0] == target and words[1] != "->":
            m = re.search(r'.*label=\"(.*)\",height.*\$(.*)\.html\#(.*)\"', line);
            if (m == None):
                continue;
            target_node["name"] = m.group(1);
            target_node["file"] = m.group(2);
            target_node["hash"] = m.group(3);
            targets_nodes.append(target_node);
            

    return targets_nodes;

def make_unique(original_list):
    unique_list = [];
    map(lambda x: unique_list.append(x) if (x not in unique_list) else False, original_list)
    return unique_list

if __name__ == "__main__":
    
#    parser = argparse.ArgumentParser(description='Process the input path')
#    parser.add_argument('path', metavar='P', type=str, nargs='+', help='the path of dot files.')
#    args = parser.parse_args()

    dotfiles = [f for f in listdir(path) if (isfile(join(path, f))and f.endswith(".dot"))];

    cgraphfiles = [f for f in dotfiles if "_cgraph" in f];
    nodes = [];
    links = [];

    for f in cgraphfiles:
        node = {};
        node["file"] = get_source_name(f);
        node["hash"] = get_hash(f);

        with open(join(path, f)) as fp:
            lines = fp.readlines();
            node["name"] = get_function_name(lines);
            
            targets = get_function_direct_calls(lines);
        fp.close();

        for t in targets:
            link = {};
            link["source"] = node["hash"];
            link["target"] = t["hash"];
            links.append(link);

        nodes.append(node);
        nodes = nodes + targets;

    nodes = make_unique(nodes);
    links = make_unique(links);

    print json.JSONEncoder().encode({"nodes": nodes, "links": links});

#def seizing(nodes, links):
    
