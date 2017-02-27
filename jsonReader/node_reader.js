// See http://robballou.com/2013/creating-an-svg-file-with-d3-and-node-js for details on saving SVG files.
var fs=require('fs');
var d3=require('d3');
var jsdom = require("jsdom");

var xmldom = require('xmldom');
var argv = require('minimist')(process.argv.slice(2));
var jsonFile=argv["_"][0]; //Use bash if you want vectorization.

function cutoff(d) {
    return d["supp"]<0.5;
}

var data=require(jsonFile).filter(cutoff);
// var data=require(jsonFile);
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

var margin      = {top:100,bottom:100,left:100,right:20},
    true_width  =1800,
    true_height =900,
    width       = true_width-margin.left-margin.right,
    height      = true_height-margin.top-margin.bottom;

var x = d3.scaleBand()
    .rangeRound([0,width])
    .padding(0.1)
    .domain(data.map(xAccessor));

var y = d3.scaleLinear()
    .rangeRound([height,0])
    .domain(d3.extent(data,yAccessor));
jsdom.env({
    html:"<html><body><div id='graph'></div></body></html>",
    // html:'',
    features:{ QuerySelector:true },
    done:function(errors, window){


        window.d3 = d3.select(window.document); //get d3 into the dom
        console.log(window.d3);

        // var svg = window.document.createElementNS('http://www.w3.org/2000/svg', 'svg')
        // var svg = window.d3.select('body')
        var svg = window.d3.select('#graph')
            // .append('div').attr('class','container') //make a container div to ease the saving process
            .append('svg')
                .attr("width",true_width)
                .attr("height",true_height)
                // .attr("xmlns",'http://www.w3.org/2000/svg')
        console.log(svg);
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

        var svgGraph = d3.select('svg')
            .attr('xmlns', 'http://www.w3.org/2000/svg');
        var svgXML = (new xmldom.XMLSerializer()).serializeToString(svgGraph[0][0]);
        fs.writeFile(generateOutputPath(jsonFile), svgXML);
    }
});
