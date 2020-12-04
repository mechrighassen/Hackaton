 // set the dimensions and margins of the graphe
var outerWidth = 300; 
var outerHeight = 250;
var circleRadius = 5; 
// set data
var data = 
     [
      {sepal_length:5.1,sepal_width:3.5,petal_length:1.4,petal_width:0.2},
      {sepal_length:4.9,sepal_width:3.0,petal_length:1.4,petal_width:0.2},
     {sepal_length:4.7,sepal_width:3.2,petal_length:1.3,petal_width:0.2},
      {sepal_length:4.6,sepal_width:3.1,petal_length:1.5,petal_width:0.2},
      {sepal_length:5.0,sepal_width:3.6,petal_length:1.4,petal_width:0.2},
      {sepal_length:5.4,sepal_width:3.9,petal_length:1.7,petal_width:0.4},
      {sepal_length:4.6,sepal_width:3.4,petal_length:1.4,petal_width:0.3},
     { sepal_length:5.0,sepal_width:3.4,petal_length:1.5,petal_width:0.2},
      {sepal_length:4.4,sepal_width:2.9,petal_length:1.4,petal_width:0.2},
      {sepal_length:4.9,sepal_width:3.1,petal_length:1.5,petal_width:0.1},
      {sepal_length:5.4,sepal_width:3.7,petal_length:1.5,petal_width:0.2}
     ];


// add the graph canvas to the body of the webpage
var svg = d3.select("body").append("svg")
.attr("width", outerWidth)
.attr("height", outerHeight);

// Add X axis
var xScale = d3.scale.linear().range([0, outerWidth]);
// Add Y axis
var yScale = d3.scale.linear().range([outerHeight, 0]);

function render(data){

 xScale.domain(d3.extent(data, function (d){ return d.sepal_length;}));
 yScale.domain(d3.extent(data, function (d){ return d.petal_length;}));
 // draw circles
 var circles = svg.selectAll("circle").data(data);

 circles.enter().append("circle")
    .attr("r",circleRadius);

 circles
    .attr("cx", function (d){   return xScale(d.sepal_length)})
    .attr("cy", function (d){   return yScale(d.petal_length)});

 circles.exit().remove();
}



//render(myArrayOfObjects);

function type(d){
 d.sepal_length=+d.sepal_length;
 d.sepal_width=+d.sepal_width;
 d.petal_length=+d.petal_length;
 d.petal_width=+d.petal_width;
 return d;
}

//d3.csv("http://mlr.cs.umass.edu/ml/machine-learning-databases/iris/iris.data", type,render);



     render(data);
