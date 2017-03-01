// See http://robballou.com/2013/creating-an-svg-file-with-d3-and-node-js for details on saving SVG files.
// var fs=require('fs');
// var d3=require('d3');
// var jsdom = require("jsdom");

// var xmldom = require('xmldom');
// var argv = require('minimist')(process.argv.slice(2));
// var jsonFile=argv["_"][0]; //Use bash if you want vectorization.

// jsonFile="./test.json";
// jsonFile="/media/Win/Data/Dropbox/School/CIS430/Project1/data/Images/output.json";

function cutoff(d) {
    return d["supp"]<0.5;
}

// var path = require(['path']);
// var root = path.dirname(require.main.filename);

// var data=require([jsonFile]);
// var data=require(['json!./test.json']);
// console.log(Object.keys(data[0]));

function yAccessor(d) {
    //Value we're putting on the Y axis
    return d.conf;
}

function sortedToString(arr) {
    return arr.map(function(d){d.toString()}).sort().toString;
}

function xAccessor(d) {
    var antecedent=sortedToString(d.antecedent);
    var consequent=sortedToString(d.consequent);
    return antecedent+"->"+consequent;
}

function generateOutputPath(inputPath) {
    // 'json' is 4 characters
    return inputPath.slice(0,-4)+"svg";
}

const margin    = {top:100,bottom:100,left:100,right:20},
    true_width  = 1800,
    true_height = 900,
    width       = true_width-margin.left-margin.right,
    height      = true_height-margin.top-margin.bottom;

function makeBarGraph(svg,rule,xAccessor,yAccessor,yLabel) {
    
    var x = d3.scaleBand()
        .rangeRound([0,width])
        .padding(0.1)
        .domain(rule,xAccessor);

    var y = d3.scaleLinear()
        .rangeRound([height,0])
        .domain(d3.extent(rule,yAccessor));

    var g = svg.append("g")
        .attr("transform","translate("+margin.left+","+margin.top+")");

    g.append("g")
        .attr("class", "xAxis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
            .selectAll("text")
            .attr("y", 0)
            .attr("x", 9)
            .attr("dy", ".35em")
            .attr("transform", "rotate(90)")
            .style("text-anchor", "start");

    g.append("g")
        .attr("class", "yAxis")
        .call(d3.axisLeft(y));

    // svg.append("text")
    //     .attr("class","chartTitle")
    //     .attr("x", true_width / 2)
    //     .attr("y", margin.top / 1.5)
    //     .attr("text-anchor", "middle")
    //     .attr("font-size", 24)
    //     .text(title);

    // svg.append("text")
    //     .attr("class","yLabel")
    //     .attr("transform","translate("+margin.left / 3+","+true_height / 2+") rotate(-90)")
    //     .attr("text-anchor", "middle")
    //     .attr("font-size", 16)
    //     .text(yLabel);

    // svg.append("text")
    //     .attr("class","xLabel")
    //     .attr("x", true_width / 2)
    //     .attr("y", true_height-margin.bottom / 9)
    //     .attr("text-anchor", "middle")
    //     .attr("font-size", 16)
    //     .text(xLabel);
}
// var svg = window.document.createElementNS('http://www.w3.org/2000/svg', 'svg')
// var svg = window.d3.select('body')
var artists = d3.select('body').selectAll("section.artist")
    .data(data)
    .enter().append("section")
        .attr("class","artist");
    
artists.append("h2")
    .text(d=>d.name);

var works = artists.selectAll("div.work")
    .data(d=>d.works)
    .enter().append("div")
        .attr("class","work");

works.selectAll("h4")
    .data(d=>d.path)
    .enter().append("h4")
        .text(d=>d);

// var graphs = works.selectAll("svg.graph")
//     .data=(d=>d.rule)
//     .enter().append('svg')
//         .attr("class","graph")
//         .attr("width",true_width)
//         .attr("height",true_height)
//         .each(p=>console.log(p));
        // .attr("xmlns",'http://www.w3.org/2000/svg')

// var svgGraph = d3.select('svg')
//     .attr('xmlns', 'http://www.w3.org/2000/svg');
// var svgXML = (new xmldom.XMLSerializer()).serializeToString(svgGraph[0][0]);
// fs.writeFile(generateOutputPath(jsonFile), svgXML);


