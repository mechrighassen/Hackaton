(function (d3) {
    'use strict';
    /* /* 
 * value accessor - returns the value to encode for a given data object.
 * scale - maps value to a visual display encoding, such as a pixel position.
 * map function - maps from data value to display value
 * axis - sets up axis
 */ 
 
    const svg = d3.select('svg');
  
    const width = +svg.attr('width');
    const height = +svg.attr('height');
  
    const render = data => {
      const title = 'Cars: Horsepower vs. Weight';
      
      const xValue = d => d.horsepower;
      const xAxisLabel = 'Horsepower';
      
      const yValue = d => d.weight;
      const circleRadius = 10;
      const yAxisLabel = 'Weight';
      
      // set the dimensions and margins of the graph
      const margin = { top: 60, right: 40, bottom: 88, left: 150 };
      const innerWidth = width - margin.left - margin.right;
      const innerHeight = height - margin.top - margin.bottom;

      // Add X axis
      const xScale = d3.scaleLinear()
        .domain(d3.extent(data, xValue))
        .range([0, innerWidth])
        .nice();

      // Add Y axis
      const yScale = d3.scaleLinear()
        .domain(d3.extent(data, yValue))
        .range([innerHeight, 0])
        .nice();
      // append the svg object to the body of the page
      const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);
      
      const xAxis = d3.axisBottom(xScale)
        .tickSize(-innerHeight)
        .tickPadding(15);
      
      const yAxis = d3.axisLeft(yScale)
        .tickSize(-innerWidth)
        .tickPadding(10);
      // y-axis
      const yAxisG = g.append('g').call(yAxis);
      yAxisG.selectAll('.domain').remove();
      
      yAxisG.append('text')
          .attr('class', 'axis-label')
          .attr('y', -93)
          .attr('x', -innerHeight / 2)
          .attr('fill', 'black')
          .attr('transform', `rotate(-90)`)
          .attr('text-anchor', 'middle')
          .text(yAxisLabel);
      // x-axis
      const xAxisG = g.append('g').call(xAxis)
        .attr('transform', `translate(0,${innerHeight})`);
      
      xAxisG.select('.domain').remove();
      
      xAxisG.append('text')
          .attr('class', 'axis-label')
          .attr('y', 75)
          .attr('x', innerWidth / 2)
          .attr('fill', 'black')
          .text(xAxisLabel);
       // Add circle
      g.selectAll('circle').data(data)
        .enter().append('circle')
          .attr('cy', d => yScale(yValue(d)))
          .attr('cx', d => xScale(xValue(d)))
          .attr('r', circleRadius);
      // draw legend text
      g.append('text')
          .attr('class', 'title')
          .attr('y', -10)
          .text(title);
    };
    //Read the data
    d3.csv('https://vizhub.com/curran/datasets/auto-mpg.csv')
      .then(data => {
        // change string (from CSV) into number format
        data.forEach(d => {
          d.mpg = +d.mpg;
          d.cylinders = +d.cylinders;
          d.displacement = +d.displacement;
          d.horsepower = +d.horsepower;
          d.weight = +d.weight;
          d.acceleration = +d.acceleration;
          d.year = +d.year;  
        });
        render(data);
      });
  
  }(d3));