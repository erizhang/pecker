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
    extention = words[-3];
    s = ['.' if x == '8' else x for x in list(extention)];
    extention = "".join(s);
    words[-3] = extention;

    del words[-2:];

    name = "".join(words);
    return "".join(words);

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
            target_node["file"] = m.group(2).replace("_8", ".");
            target_node["hash"] = m.group(3);
            targets_nodes.append(target_node);

    return targets_nodes;

def make_unique(original_list):
    unique_list = [];
    map(lambda x: unique_list.append(x) if (x not in unique_list) else False, original_list)
    return unique_list

def read_call_tree(path):
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
            node['calls'] = get_function_direct_calls(lines);
        fp.close();

        nodes.append(node);
    nodes = make_unique(nodes);
    return nodes

def read_complexity_list(complexity_file):
    nodes = []
    with open(complexity_file) as fp:
        lines = fp.readlines();
        del lines[0:3]
        del lines[-4:]
        for line in lines:
            node = {};
            keys = [key for key in line.split(' ') if key]

            m = re.search(r'(.*)\@.*\@.*\/(.*)', keys[-1]);
            if (m == None):
                continue;
            node['name'] = m.group(1);
            node['file'] = m.group(2);
            node['nloc'] = keys[0];
            node['ccn'] = keys[1];

            nodes.append(node);
    fp.close();
    nodes = make_unique(nodes);
    return nodes


def calc_fan_out(node, call_tree):
    for n in call_tree:
        if node['file'] == n['file'] and node['name'] == n['name']:
            return len(n['calls']);
    return 0

def calc_fan_in(node, call_tree):
    return 0

if __name__ == '__main__':
    call_tree_nodes = read_call_tree("/home/erizhang/workspace/lab/html");
    nodes = read_complexity_list("./ctest");
    for node in nodes:
        node['fan-out'] = calc_fan_out(node, call_tree_nodes);
        node['fan-in'] = calc_fan_in(node, call_tree_nodes);

    print nodes
    print json.JSONEncoder().encode({"nodes": nodes});
