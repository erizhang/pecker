#!/usr/bin/python

from os import listdir
from os.path import isfile, join
import re
import json

import argparse

def get_hash(f):
    words = f.split("_");
    return words[-2];

def get_source_name(f):
    words = ['_' if x =='' else x for x in f.split('_')];
    print words
    extention = words[-3];
    print extention
    s = ['.' if x == '8' else x for x in list(extention)];
    extention = "".join(s);
    words[-3] = extention;

    del words[-2:];

    name = "".join(words);
    print name
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
def generate_report(app_config):
#    parser = argparse.ArgumentParser(description='Process the input path')
#    parser.add_argument('path', metavar='P', type=str, nargs='+', help='the path of dot files.')
#    args = parser.parse_args()
    path = app_config['dots_path']

    dotfiles = [f for f in listdir(path) if (isfile(join(path, f))and f.endswith(".dot"))];

    cgraphfiles = [f for f in dotfiles if "_cgraph" in f];
    nodes = [];
    links = [];
    print cgraphfiles

    for f in cgraphfiles:
        node = {};
        node["file"] = get_source_name(f);
        node["hash"] = get_hash(f);

        with open(join(path, f)) as fp:
            lines = fp.readlines();
            node["name"] = get_function_name(lines);
            targets = []
            targets = get_function_direct_calls(lines);
            node["fan-in"] = len(targets);
        fp.close();

        nodes.append(node);
        #nodes = nodes + targets;

    icgraphfiles = [f for f in dotfiles if "_icgraph" in f];
    print "------------------------"
    print icgraphfiles
    print "========================"
    for f in icgraphfiles:
        filename = get_source_name(f);
        hashcode = get_hash(f);
        fan_out = 0;

        with open(join(path, f)) as fp:
            lines = fp.readlines();
            targets = [];
            targets = get_function_direct_calls(lines);
            fan_out = len(targets);
            function_name = get_function_name(lines);
        fp.close();

        isFound = False;
        for node in nodes:
            if node["hash"] == hashcode:
                node["fan-out"] = fan_out;
                isFound = True;

        if isFound == False:
            new_node = {};
            new_node['file'] = filename
            new_node['hash'] = hashcode
            new_node['name'] = function_name
            new_node['fan-in'] = 0
            new_node['fan-out'] = fan_out
            nodes.append(new_node);
            
    nodes = make_unique(nodes);

    print json.JSONEncoder().encode({"nodes": nodes});
