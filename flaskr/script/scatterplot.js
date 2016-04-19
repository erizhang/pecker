var legend_width = 30;

var margin = {
    top: 20,
    right: 20,
    bottom: 30,
    left: 40
  },
  width = 600 - margin.left - margin.right,
  height = 500 - margin.top - margin.bottom;

var x = d3.scale.linear()
  .range([0, width]);

var y = d3.scale.linear()
  .range([height, 0]);

var r = d3.scale.linear().range([5, 8]);
var offset = d3.scale.linear().range([5, 10]);

var color = d3.scale.category10();

var colorScale = d3.scale.linear()
  .range(["#6363FF", "#6373FF", "#63A3FF", "#63E3FF", "#63FFFB", "#63FFCB",
    "#63FF9B", "#63FF6B", "#7BFF63", "#BBFF63", "#DBFF63", "#FBFF63",
    "#FFD363", "#FFB363", "#FF8363", "#FF7363", "#FF6364"
  ])

.domain(d3.range(1, 257));

var myColor = d3.scale.linear().range(['red', 'blue']);



var xAxis = d3.svg.axis()
  .scale(x)
  .orient("bottom");

var yAxis = d3.svg.axis()
  .scale(y)
  .orient("left");


var tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {
    return "<strong>File:</strong> <span style='color:green'>" + d.file +
      "</span><br/><strong>Function:</strong> <span style='color:green'>" + d.name +
      "</span><br/><strong>Complexity:</strong> <span style='color:red'>" + d.ccn + "</span>";
  })


var svg = d3.select("body").append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg.call(tip);

d3.json("linux.json", function(data) {
  data = data.nodes;

  data.forEach(function(d) {
    d.fan_in = +d.fan_in;
    d.fan_out = +d.fan_out;
  });

  x.domain([d3.min(data, function(d) {
    return d.fan_in
  }), d3.max(data, function(d) {
    return d.fan_in
  })]);

  //x.domain(d3.extent(data, function(d) { return d.fan_in; })).nice();
  y.domain(d3.extent(data, function(d) {
    return d.fan_out;
  })).nice();

  r.domain([d3.min(data, function(d) {
      return d.ccn;
    }),
    d3.max(data, function(d) {
      return d.ccn;
    })
  ]);


  var quantize = d3.scale.quantile()
    .range(d3.range(1, 257))
    .domain([d3.min(data, function(d) {
        return d.ccn;
      }),
      d3.max(data, function(d) {
        return d.ccn;
      })
    ]);

  myColor.domain([d3.min(data, function(d) {
      return d.ccn;
    }),
    d3.max(data, function(d) {
      return d.ccn;
    })
  ]);


  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
    .append("text")
    .attr("class", "label")
    .attr("x", width)
    .attr("y", -6)
    .style("text-anchor", "end")
    .text("Fan In");

  svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text")
    .attr("class", "label")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Fan Out")

  svg.selectAll(".dot")
    .data(data)
    .enter().append("circle")
    .attr("class", "dot")
    .attr("r", function(d) {
      return r(d.ccn);
    })
    .attr("cx", function(d) {
      pos = x(d.fan_in) + Math.floor(Math.random() * d.ccn);
      if (pos > width - r(d.ccn)) {
        pos = width - r(d.ccn);
      }
      return pos;
    })
    .attr("cy", function(d) {
      pos = y(d.fan_out) - Math.floor(Math.random() * d.ccn);
      if (pos < r(d.ccn)) {
        pos = r(d.ccn);
      }
      return pos; //y(d.fan_out) - Math.floor(Math.random() * d.ccn);
    })
    .style("fill", function(d) {
      return colorScale(d.ccn);
    })
    .on('mouseover', tip.show)
    .on('mouseout', tip.hide);


  /*
    var legend = svg.selectAll(".legend")
        .data(color.domain())
      .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

    legend.append("rect")
        .attr("x", width - 18)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    legend.append("text")
        .attr("x", width - 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(function(d) { return d; }); */

});
