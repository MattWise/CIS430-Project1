
// graph dimensions
var svgWidth = 600;		// width of the svg element
var svgHeight = 10000;	// height of the svg element

var margin = {top:80,left:120,bottom:40,right:20};

var chartWidth = svgWidth - margin.left - margin.right;		// bar chart width

// text
var ents = ["antecedent", "consequent" ];
var measures = ["supp", "cove", "lift", "conf", "leve"];

var titleText = "Graph";

var yAxisValue = measures[2];
var xAxisValue = ents[0];


jsonarray.sort(function(object, object2){
	return object2[yAxisValue] - object[yAxisValue];
});


// create a d3 scale for the y axis

var results = jsonarray.map(function(object) {
	return object[yAxisValue];
});
console.log(results);

var barScaler = d3.scaleLinear()
	.domain([0,d3.max(results)*1.1])
	.range([0,chartWidth]);
	
// add an svg element to the specified div
var svg = d3.select("#graph")
	.append("svg")
	.attr("width", svgWidth)
	.attr("height", svgHeight);
	
// create the chart title
svg.append("text")
	.attr("class","titletext")
	.attr("x", (svgWidth + margin.left - margin.right) / 2)
	.attr("y", margin.top / 3)
	.attr("text-anchor", "middle")
	.attr("font-size", 24)
	.text(titleText);
		
// create the horizontal axis title
svg.append("text")
	.attr("class","yaxistitle")
	.attr("x", (svgWidth + margin.left - margin.right) / 2)
	.attr("y", margin.top / 1.5)
	.attr("text-anchor", "middle")
	.attr("font-size", 16)
	.text(yAxisValue);
	
// create the vertical axis title
svg.append("text")
	.attr("class","xaxistitle")
	.attr("x", margin.left / 2)
	.attr("y", margin.top / 1.5)
	.attr("text-anchor", "middle")
	.attr("font-size", 16)
	.text(xAxisValue);
	
// create a chart container
var chartGroup = svg.append("g").attr("class","chart");

// create axes
var xAxisGroup = chartGroup.append("g").attr("class","xaxis");	// the x axis

// create the y axis
xAxisGroup.call(d3.axisTop()
	.scale(barScaler));
			
// string for translating the chart
var chartTranslate = "translate(" + margin.left + "," + margin.top + ")";

// translate the bar chart
chartGroup.attr("transform", chartTranslate);

// return a group to add chart into
var barGroup = chartGroup.append("g");

// store in data
var barData = barGroup
	.selectAll("rect")
	.data(results);

// create the bars
barData.enter().append("rect")
	.merge(barData)
	.attr("x", 0)
	.attr("y", function(d,i) { return i*20; })
	.attr("width", function(d) { return barScaler(d); })
	.attr("height", 16)
	.attr("fill", "steelblue")	