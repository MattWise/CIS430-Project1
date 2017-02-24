
var svgWidth = 600;		// width of the svg element
var svgHeight = 10000;	// height of the svg element
var chartVMargin = 80;	// both vertical margins for the bar chart
var chartHMargin = 60;	// left horizontal margin for the bar chart

// text
var titleText = "Graph";
var yAxisTitleText = "Lift";
var xAxisTitleText = "Antecedent";

var chartWidth = svgWidth - chartHMargin;		// bar chart width

var antecedent = [];
var consequent = [];

var support = [];
var coverage = [];
var lift = [];
var confidence = [];
var leverage = [];

jsonarray.forEach(function(object, index, arr){

	antecedent.push(object["antecedent"]);
	consequent.push(object["consequent"]);
	
	support.push(object["supp"]);
	coverage.push(object["cove"]);
	lift.push(object["lift"]);
	confidence.push(object["conf"]);
	leverage.push(object["leve"]);
});


// create a d3 scale for the y axis

var results = confidence;
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
	.attr("x", (svgWidth + chartHMargin) / 2)
	.attr("y", chartVMargin / 1.5)
	.attr("text-anchor", "middle")
	.attr("font-size", 24)
	.text(titleText);
		
// create the y axis title
svg.append("text")
	.attr("class","yaxistitle")
	.attr("x", -svgHeight / 2)
	.attr("y", chartHMargin / 3)
	.attr("transform", "rotate(-90)")
	.attr("text-anchor", "middle")
	.attr("font-size", 16)
	.text(yAxisTitleText);
	
// create the x axis title
svg.append("text")
	.attr("class","xaxistitle")
	.attr("x", (svgWidth + chartHMargin) / 2)
	.attr("y", svgHeight - chartVMargin / 8)
	.attr("text-anchor", "middle")
	.attr("font-size", 16)
	.text(xAxisTitleText);
	
// create a chart container
var chartGroup = svg.append("g").attr("class","chart");

// create axes
var xAxisGroup = chartGroup.append("g").attr("class","xaxis");	// the x axis

// create the y axis
xAxisGroup.call(d3.axisTop()
	.scale(barScaler));
			
// string for translating the chart
var chartTranslate = "translate(" + chartHMargin + "," + chartVMargin + ")";

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