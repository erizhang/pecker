Pecker
--
[![Build Status](https://travis-ci.org/erizhang/pecker.svg?branch=master)](https://travis-ci.org/erizhang/pecker)

### 1. How does this tool to generate the fan-in/out information
#### Step 1. Generate the call graph dot files via `Doxygen`
We would like to generate the call graph dot files, we have to change the `Doxygen` configuration file as below:
```
EXTRACT_ALL            = YES
INPUT                  = # specify the source code relative path, split with whitespace
INLINE_SOURCES         = YES
GENERATE_LATEX         = NO
INCLUDE_PATH           = # specify the header file relative path, split with whitespace
HAVE_DOT               = YES
CALL_GRAPH             = YES
CALLER_GRAPH           = YES
DOTFILE_DIRS           = dotfile
DOT_CLEANUP            = NO
```
After execute the command `doxygen`, there will be generate the source code's index files and related inmediate files `*.dot`.

#### Step 2. Reading the `*.dot` file and analyze the call relationship between functions.
The `*_cgraph.dot` file's format likes this:
```
digraph "function_name"
{
  edge [the fone setting of edge];
  node [the font setting of node];
  rakedir="LR";
  Node1 [label="funtion_name", node's style setting]; //this is discribe itsself
  Node1 -> Node2 [Illustrate the relationship between Node1 and Node2]
  Node2 [label="function_name", ..., URL="$filename_8c.html#hashcode"];
  Node2 -> Node3 [Illustrate the relationship between Node2 and Node3]
  Node3 [label="function_name", ..., URL="$filename_8c.html#hashcode"];
  ...
}

```
tool `dot` generates the png pictures according to the `*.dot` file's definition. It's also give the clue to us for parsing the relationship between functions. If we know the relationship between function, we also create the relathionship between files/folders etc.

We program intent on generate a relationships, and output as specific format, e.g. `*.json`

**NOTE:** We shall carefully consider the template situation during parse C plus plus programming language source code.


## 2. Generate the complexity information

The [cyclomatic compelxity](https://en.wikipedia.org/wiki/Cyclomatic_complexity "complexity") could be generate by [lizard](https://github.com/terryyin/lizard "lizard") tool. Detailed information can read lizard's readme.

## 3. Visulize the functions relationship

For such relationship data, we can store the Neo4j such graph database, and the database offer the simple chart to illustrate the data element's relationship.

But we recommend use d3js to implement customized chart for these relationship visualization.





