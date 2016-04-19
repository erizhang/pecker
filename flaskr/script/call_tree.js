var width = 800,
  height = 600;

var color = d3.scale.category20();

var force = d3.layout.force()
  .charge(-40)
  .linkDistance(20)
  .size([width, height]);

var svg = d3.select("body").append("svg")
  .attr("width", width)
  .attr("height", height);

d3.json("nginx.json", function(error, graph) {
  var calls = _.countBy(graph.links, function(link) {
    return link.target;
  });
  
  var nodes = _.map(graph.nodes, function(d) {
    return {
      "name": d.name,
      "file": d.file,
      "hash": d.hash,
      "calls": calls[d.hash] === undefined ? 0 : calls[d.hash]
    };
  });
  
  console.log(nodes)
  nodes = _.uniq(nodes, function(d){
      return d.hash
  });
  nodes = _.forEach(nodes, function(node) {
    _.forEach(links, function(link){
      if (link.source === node.hash || link.target === node.hash) {
        return node;
      }
    });
  })
  
  console.log(nodes);
  
  var links = _.map(graph.links, function(d) {
    return {
      "source": _.findIndex(nodes, function(node) {
        return node.hash == d.source;
      }),
      "target": _.findIndex(nodes, function(node) {
        return node.hash == d.target;
      }),
      "value": 1
    };
  });


  force
    .nodes(nodes)
    .links(links)
    .start();
    
  var R = d3.scale.linear().range([5, 15]).domain([0, 16]);

  var link = svg.selectAll(".link")
    .data(links)
    .enter().append("line")
    .attr("class", "link")
    .style("stroke-width", 2/*function(d) {
      return Math.sqrt(d.value);
    }*/);

  var node = svg.selectAll(".node")
    .data(nodes)
    .enter().append("circle")
    .attr("class", "node")
    .attr("r", function(d){
      return R(d.calls);
    })
    .style("fill", function(d) {
      return color(d.file);
    })
    .call(force.drag);

  node.append("title")
    .text(function(d) {
      return d.file + ":" + d.name + ":" + d.calls;
    });

  force.on("tick", function() {
    link.attr("x1", function(d) {
        return d.source.x;
      })
      .attr("y1", function(d) {
        return d.source.y;
      })
      .attr("x2", function(d) {
        return d.target.x;
      })
      .attr("y2", function(d) {
        return d.target.y;
      });

    node.attr("cx", function(d) {
        return d.x;
      })
      .attr("cy", function(d) {
        return d.y;
      });
  });
});
